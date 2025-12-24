#!/usr/bin/env python3
"""
Set GitHub secrets using the API with inline encryption
This script uses pure Python cryptography libraries
"""

import os
import json
import base64
import urllib.request
import urllib.error
import sys
import subprocess

# Try to use cryptography library (usually available)
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

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

def set_secret_via_cli(secret_name, secret_value):
    """Try to set secret using GitHub CLI if available"""
    try:
        process = subprocess.Popen(
            ['gh', 'secret', 'set', secret_name, '--repo', repo],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=secret_value)
        if process.returncode == 0:
            return True
        return False
    except FileNotFoundError:
        return False

def main():
    print("Setting up GitHub Secrets via API...")
    print("")
    
    secrets = {
        "KEY_PASSWORD": "changeit",
        "KEY_ALIAS": "gloven-key"
    }
    
    # Try GitHub CLI first
    gh_available = subprocess.run(['which', 'gh'], 
                                  capture_output=True).returncode == 0
    
    if gh_available:
        print("Using GitHub CLI...")
        for name, value in secrets.items():
            if set_secret_via_cli(name, value):
                print(f"✅ {name} set successfully")
            else:
                print(f"❌ Failed to set {name}")
    else:
        print("⚠️  GitHub CLI not available")
        print("")
        print("Please set these secrets manually:")
        print(f"  Go to: https://github.com/{repo}/settings/secrets/actions")
        print("")
        for name, value in secrets.items():
            print(f"  {name}: {value}")
    
    # KEYSTORE_BASE64
    if os.path.exists("keystore_base64.txt"):
        print("")
        print("Setting KEYSTORE_BASE64...")
        with open("keystore_base64.txt", "r") as f:
            keystore_b64 = f.read().strip()
        
        if gh_available:
            if set_secret_via_cli("KEYSTORE_BASE64", keystore_b64):
                print("✅ KEYSTORE_BASE64 set successfully")
            else:
                print("❌ Failed to set KEYSTORE_BASE64")
        else:
            print("⚠️  Copy entire contents of keystore_base64.txt")
            print(f"   Go to: https://github.com/{repo}/settings/secrets/actions")
    
    print("")
    print("✅ Done!")

if __name__ == "__main__":
    main()

