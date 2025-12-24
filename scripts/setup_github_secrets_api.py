#!/usr/bin/env python3
"""Set up GitHub Secrets using the GitHub API"""

import os
import json
import base64
import urllib.request
import urllib.error
import sys

try:
    from nacl import encoding, public
    HAS_NACL = True
except ImportError:
    HAS_NACL = False
    print("⚠️  PyNaCl not available. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'PyNaCl'])
    from nacl import encoding, public
    HAS_NACL = True

token = os.environ.get('GITHUB_TOKEN')
if not token:
    print("❌ GITHUB_TOKEN environment variable not set")
    sys.exit(1)

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
    """Encrypt secret using libsodium"""
    public_key_bytes = base64.b64decode(public_key_str)
    public_key = public.PublicKey(public_key_bytes)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def set_secret(secret_name, secret_value):
    """Set a GitHub secret"""
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
        else:
            print(f"❌ Error setting {secret_name}: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"❌ Error setting {secret_name}: {e}")
        return False

def main():
    print("Setting up GitHub Secrets...")
    print("")
    
    # Basic secrets
    secrets = {
        "KEYSTORE_PASSWORD": "changeit",
        "KEY_PASSWORD": "changeit",
        "KEY_ALIAS": "gloven-key"
    }
    
    success_count = 0
    for name, value in secrets.items():
        if set_secret(name, value):
            success_count += 1
    
    # KEYSTORE_BASE64
    if os.path.exists("keystore_base64.txt"):
        print("")
        print("Setting KEYSTORE_BASE64...")
        with open("keystore_base64.txt", "r") as f:
            keystore_b64 = f.read().strip()
        if set_secret("KEYSTORE_BASE64", keystore_b64):
            success_count += 1
    else:
        print("")
        print("⚠️  keystore_base64.txt not found")
        print("   KEYSTORE_BASE64 needs to be set manually")
    
    print("")
    print(f"✅ {success_count}/{len(secrets) + 1} secrets configured")
    print("")
    print("📋 Remaining secrets (set manually if needed):")
    print("   - GCP_SA_KEY (Google Play Service Account JSON)")
    print("   - GCP_PROJECT_ID (Your GCP Project ID)")
    print("")
    print("🔗 Set them at: https://github.com/ahmedmaache/gloven-flutter-apps/settings/secrets/actions")

if __name__ == "__main__":
    main()

