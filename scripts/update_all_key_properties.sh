#!/bin/bash
# Update key.properties for all apps with actual passwords
# This is for local development. For CI/CD, use GitHub Secrets.

KEYSTORE_PASSWORD=${1:-"changeit"}
KEY_PASSWORD=${2:-"changeit"}
KEY_ALIAS=${3:-"gloven-key"}

echo "Updating key.properties for all 100 apps..."
echo "Using passwords from arguments or defaults"

for i in {1..100}; do
    APP_DIR="apps/app$(printf "%02d" $i)"
    if [ -d "$APP_DIR" ]; then
        cat > "$APP_DIR/android/key.properties" << KEYPROPS
storePassword=$KEYSTORE_PASSWORD
keyPassword=$KEY_PASSWORD
keyAlias=$KEY_ALIAS
storeFile=gloven-keystore.jks
KEYPROPS
        # Copy keystore to app directory for local builds
        cp gloven-keystore.jks "$APP_DIR/android/gloven-keystore.jks" 2>/dev/null || true
    fi
done

echo "✓ Updated key.properties for all apps"
echo "⚠️  Note: For GitHub Actions, use GitHub Secrets instead"

