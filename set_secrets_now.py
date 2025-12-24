#!/usr/bin/env python3
"""Set GitHub secrets using the API with proper encryption"""

import os
import json
import base64
import urllib.request
import urllib.error
import sys

# Try to import from venv first, then system
try:
    from nacl import encoding, public
except ImportError:
    # Activate venv if available
    venv_path = os.path.join(os.path.dirname(__file__), 'venv_secrets')
    if os.path.exists(venv_path):
        sys.path.insert(0, os.path.join(venv_path, 'lib', 'python3.13', 'site-packages'))
        from nacl import encoding, public
    else:
        print("❌ PyNaCl not available. Please install it first.")
        sys.exit(1)

token = os.environ.get('GITHUB_TOKEN')
if not token:
    token = "YOUR_GITHUB_TOKEN"

repo = "ahmedmaache/gloven-flutter-apps"

def get_public_key():
    """Get GitHub repository public key for encryption"""
    url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return data['key_id'], data['key']
    except Exception as e:
        print(f"❌ Error getting public key: {e}")
        return None, None

def encrypt_secret(public_key_str, secret_value):
    """Encrypt secret using libsodium sealed box"""
    public_key_bytes = base64.b64decode(public_key_str)
    public_key = public.PublicKey(public_key_bytes)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def set_secret(secret_name, secret_value):
    """Set a GitHub secret"""
    print(f"Setting {secret_name}...")
    
    key_id, public_key = get_public_key()
    if not key_id or not public_key:
        print(f"❌ Failed to get public key for {secret_name}")
        return False
    
    encrypted_value = encrypt_secret(public_key, secret_value)
    
    url = f"https://api.github.com/repos/{repo}/actions/secrets/{secret_name}"
    data = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")
    req.get_method = lambda: 'PUT'
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [201, 204]:
                print(f"✅ {secret_name} set successfully")
                return True
            else:
                print(f"❌ Failed to set {secret_name}: HTTP {response.status}")
                return False
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"⚠️  {secret_name} may already exist or value is invalid")
            # Try to read error message
            try:
                error_data = json.loads(e.read().decode())
                print(f"   Error: {error_data.get('message', 'Unknown error')}")
            except:
                pass
        else:
            print(f"❌ Error setting {secret_name}: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"❌ Error setting {secret_name}: {e}")
        return False

def main():
    print("Setting up GitHub Secrets...")
    print("")
    
    # Set basic secrets
    secrets = {
        "KEY_PASSWORD": "changeit",
        "KEY_ALIAS": "gloven-key"
    }
    
    success_count = 0
    for name, value in secrets.items():
        if set_secret(name, value):
            success_count += 1
        print("")
    
    # Set KEYSTORE_BASE64
    keystore_file = "keystore_base64.txt"
    if os.path.exists(keystore_file):
        print(f"Setting KEYSTORE_BASE64 from {keystore_file}...")
        with open(keystore_file, "r") as f:
            keystore_b64 = f.read().strip()
        if set_secret("KEYSTORE_BASE64", keystore_b64):
            success_count += 1
    else:
        print(f"❌ {keystore_file} not found")
    
    print("")
    print(f"✅ {success_count}/3 secrets configured")
    print("")
    print("🔍 Verifying...")
    
    # Verify secrets
    url = f"https://api.github.com/repos/{repo}/actions/secrets"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            configured_secrets = [s['name'] for s in data.get('secrets', [])]
            required = ['KEYSTORE_PASSWORD', 'KEY_PASSWORD', 'KEY_ALIAS', 'KEYSTORE_BASE64']
            
            print("")
            for req_secret in required:
                status = '✅' if req_secret in configured_secrets else '❌'
                print(f"{status} {req_secret}")
            
            if all(s in configured_secrets for s in required):
                print("")
                print("🎉🎉🎉 ALL SECRETS CONFIGURED! 🎉🎉🎉")
                print("🚀 GitHub Actions is ready to build your 100 apps!")
    except Exception as e:
        print(f"Could not verify: {e}")

if __name__ == "__main__":
    main()

