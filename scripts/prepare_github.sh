#!/bin/bash
# Script to prepare repository for GitHub push

echo "Preparing repository for GitHub..."
echo ""

# Check if keystore exists
if [ ! -f "gloven-keystore.jks" ]; then
    echo "⚠️  Keystore not found. Generating..."
    ./scripts/setup_keystore.sh
fi

# Encode keystore
if [ ! -f "keystore_base64.txt" ]; then
    echo "Encoding keystore to base64..."
    base64 -i gloven-keystore.jks > keystore_base64.txt
    echo "✓ Keystore encoded"
fi

# Create GitHub Secrets helper file
cat > GITHUB_SECRETS_INSTRUCTIONS.txt << 'EOF'
GitHub Secrets Setup Instructions
==================================

Copy these values to GitHub Secrets at:
https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions

1. KEYSTORE_PASSWORD
   Value: changeit
   (Change this to your actual password!)

2. KEY_PASSWORD
   Value: changeit
   (Change this to your actual password!)

3. KEY_ALIAS
   Value: gloven-key

4. KEYSTORE_BASE64
   Copy the entire contents of: keystore_base64.txt
   Or run: cat keystore_base64.txt | pbcopy (macOS)
          cat keystore_base64.txt | xclip (Linux)

5. GCP_SA_KEY
   Your Google Play Service Account JSON
   Create at: https://console.cloud.google.com/iam-admin/serviceaccounts
   Download the JSON key file and paste entire contents here

6. GCP_PROJECT_ID
   Your Google Cloud Project ID

IMPORTANT: Change the default passwords (changeit) before production use!
EOF

echo "✓ Created GITHUB_SECRETS_INSTRUCTIONS.txt"
echo ""
echo "Next steps:"
echo "1. Review GITHUB_SECRETS_INSTRUCTIONS.txt"
echo "2. Set up GitHub Secrets (see instructions file)"
echo "3. Run: git add ."
echo "4. Run: git commit -m 'Add 100 Flutter apps'"
echo "5. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "6. Run: git push -u origin main"
echo ""
echo "Ready for GitHub push! 🚀"

