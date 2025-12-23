#!/bin/bash
# Script to generate keystore for signing AAB files
# This should be run once and the keystore should be stored securely

KEYSTORE_PATH="gloven-keystore.jks"
KEY_ALIAS="gloven-key"

if [ -f "$KEYSTORE_PATH" ]; then
    echo "Keystore already exists. Skipping generation."
    exit 0
fi

echo "Generating keystore for signing AAB files..."
echo "You will be prompted for passwords. Store them securely!"

keytool -genkey -v -keystore $KEYSTORE_PATH \
    -alias $KEY_ALIAS \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -storepass changeit \
    -keypass changeit \
    -dname "CN=Gloven Apps, OU=Development, O=Gloven, L=City, ST=State, C=US"

echo "Keystore generated at: $KEYSTORE_PATH"
echo "IMPORTANT: Update passwords in key.properties files and store keystore securely!"
echo "For production, use GitHub Secrets to store keystore and passwords."

