#!/bin/bash
# Script to create a Flutter game app with all required features

APP_NUMBER=$1
GAME_NAME=$2
GAME_TYPE=$3
PACKAGE_NAME="org.gloven.app$(printf "%02d" $APP_NUMBER)"
APP_DIR="apps/app$(printf "%02d" $APP_NUMBER)"

if [ -z "$APP_NUMBER" ] || [ -z "$GAME_NAME" ] || [ -z "$GAME_TYPE" ]; then
    echo "Usage: $0 <app_number> <game_name> <game_type>"
    exit 1
fi

echo "Creating game: $GAME_NAME ($GAME_TYPE) - $PACKAGE_NAME"

# Remove existing app if it exists
rm -rf $APP_DIR

# Create Flutter app
flutter create --org org.gloven --project-name app$(printf "%02d" $APP_NUMBER) $APP_DIR

# Wait for files
sleep 2

# Update pubspec.yaml with game dependencies
cat >> $APP_DIR/pubspec.yaml << 'DEPENDENCIES'

dependencies:
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  audioplayers: ^5.2.1
  vibration: ^1.8.4
DEPENDENCIES

# Update package name in build.gradle.kts
python3 scripts/update_build_gradle.py "$APP_DIR/android/app/build.gradle.kts" "$PACKAGE_NAME"

echo "Game template created: $GAME_NAME"
echo "Package: $PACKAGE_NAME"
echo "Type: $GAME_TYPE"

