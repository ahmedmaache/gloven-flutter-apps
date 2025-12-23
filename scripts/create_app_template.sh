#!/bin/bash
# Script to create a Flutter app template with org.gloven package

APP_NUMBER=$1
APP_NAME="app$(printf "%02d" $APP_NUMBER)"
PACKAGE_NAME="org.gloven.${APP_NAME}"
APP_DIR="apps/${APP_NAME}"

if [ -z "$APP_NUMBER" ]; then
    echo "Usage: $0 <app_number>"
    exit 1
fi

echo "Creating Flutter app: $APP_NAME with package: $PACKAGE_NAME"

# Create Flutter app
flutter create --org org.gloven --project-name $APP_NAME $APP_DIR

# Wait for files to be created
sleep 2

# Update pubspec.yaml - fix description
python3 -c "
import sys
file_path = '$APP_DIR/pubspec.yaml'
app_name = '${APP_NAME}'
app_number = '${APP_NUMBER}'
with open(file_path, 'r') as f:
    lines = f.readlines()
new_lines = []
seen_name = False
seen_desc = False
for line in lines:
    if line.startswith('name: ') and not seen_name:
        new_lines.append(f'name: {app_name}\n')
        seen_name = True
    elif line.startswith('description:') and not seen_desc:
        new_lines.append(f'description: Gloven App {app_number} - Flutter application for Google Play Store\n')
        seen_desc = True
    elif not (line.startswith('name: ') or (line.startswith('description:') and seen_desc)):
        new_lines.append(line)
with open(file_path, 'w') as f:
    f.writelines(new_lines)
"

# Update Android package name and signing in build.gradle.kts (Kotlin DSL)
if [ -f "$APP_DIR/android/app/build.gradle.kts" ]; then
    python3 "$(dirname $0)/update_build_gradle.py" "$APP_DIR/android/app/build.gradle.kts" "$PACKAGE_NAME"
fi

# Update AndroidManifest.xml package (if needed)
if [ -f "$APP_DIR/android/app/src/main/AndroidManifest.xml" ]; then
    # AndroidManifest doesn't need package attribute in newer Flutter versions, but we'll ensure it's correct
    sed -i "s/android:label=\"[^\"]*\"/android:label=\"Gloven App ${APP_NUMBER}\"/" $APP_DIR/android/app/src/main/AndroidManifest.xml
fi

# Update MainActivity.kt package
MAIN_ACTIVITY_PATH=$(find $APP_DIR/android/app/src/main/kotlin -name "MainActivity.kt" 2>/dev/null | head -1)
if [ -n "$MAIN_ACTIVITY_PATH" ]; then
    # Get the current package directory structure
    CURRENT_PACKAGE_DIR=$(dirname $MAIN_ACTIVITY_PATH)
    NEW_PACKAGE_DIR="$APP_DIR/android/app/src/main/kotlin/org/gloven/${APP_NAME}"
    
    # Create new directory structure
    mkdir -p "$NEW_PACKAGE_DIR"
    
    # Move MainActivity.kt if it's in a different location
    if [ "$CURRENT_PACKAGE_DIR" != "$NEW_PACKAGE_DIR" ]; then
        mv "$MAIN_ACTIVITY_PATH" "$NEW_PACKAGE_DIR/MainActivity.kt"
        MAIN_ACTIVITY_PATH="$NEW_PACKAGE_DIR/MainActivity.kt"
    fi
    
    # Update package name in MainActivity.kt
    sed -i "s/^package .*/package ${PACKAGE_NAME}/" "$MAIN_ACTIVITY_PATH"
fi

# Update lib/main.dart with app-specific content
cat > $APP_DIR/lib/main.dart << 'MAIN_DART'
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gloven App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Gloven App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
MAIN_DART

# Create key.properties template
cat > $APP_DIR/android/key.properties << 'KEY_PROPERTIES'
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=gloven-key
storeFile=gloven-keystore.jks
KEY_PROPERTIES

echo "App $APP_NAME created successfully with package $PACKAGE_NAME"
