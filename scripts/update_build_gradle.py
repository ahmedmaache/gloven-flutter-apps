#!/usr/bin/env python3
"""Update build.gradle.kts with signing configuration"""

import re
import sys

def update_build_gradle(file_path, package_name):
    """Update build.gradle.kts with signing config"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if signing config already exists
    if 'signingConfigs {' in content or 'signingConfigs.create' in content:
        # Already configured, just update package name if needed
        if f'namespace = "{package_name}"' not in content:
            content = re.sub(r'namespace = "[^"]*"', f'namespace = "{package_name}"', content)
            content = re.sub(r'applicationId = "[^"]*"', f'applicationId = "{package_name}"', content)
            with open(file_path, 'w') as f:
                f.write(content)
        return
    
    # Add imports at the top if not present
    imports = '''import java.util.Properties
import java.io.FileInputStream

'''
    
    # Add keystore properties before android block
    keystore_props = '''val keystorePropertiesFile = rootProject.file("key.properties")
val keystoreProperties = Properties()
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

'''
    
    # Insert signing configs before buildTypes
    signing_config = '''    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String?
            keyPassword = keystoreProperties["keyPassword"] as String?
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String?
        }
    }

'''
    
    # Find buildTypes and insert signingConfigs before it
    buildtypes_match = re.search(r'(\s+)buildTypes \{', content)
    if buildtypes_match:
        indent = buildtypes_match.group(1)
        insert_pos = buildtypes_match.start()
        # Adjust signing config indentation
        signing_config_indented = re.sub(r'^    ', indent, signing_config, flags=re.MULTILINE)
        content = content[:insert_pos] + signing_config_indented + content[insert_pos:]
    else:
        # If buildTypes not found, insert before the closing brace of android block
        # Find the last } before flutter block
        flutter_match = re.search(r'\nflutter \{', content)
        if flutter_match:
            # Find the matching } for android {
            android_match = re.search(r'\nandroid \{', content)
            if android_match:
                # Count braces to find the end of android block
                pos = android_match.end()
                depth = 1
                while pos < len(content) and depth > 0:
                    if content[pos] == '{':
                        depth += 1
                    elif content[pos] == '}':
                        depth -= 1
                    pos += 1
                # Insert before the closing brace
                insert_pos = pos - 1
                signing_config_indented = re.sub(r'^    ', '    ', signing_config, flags=re.MULTILINE)
                content = content[:insert_pos] + signing_config_indented + content[insert_pos:]
    
    # Update signingConfig in buildTypes release
    content = re.sub(
        r'signingConfig = signingConfigs\.getByName\("debug"\)',
        'signingConfig = signingConfigs.getByName("release")',
        content
    )
    
    # Add imports if not present
    if 'import java.util.Properties' not in content:
        # Find where to insert (after plugins block)
        plugins_match = re.search(r'(plugins \{[^}]*\})', content, re.DOTALL)
        if plugins_match:
            insert_pos = plugins_match.end()
            content = content[:insert_pos] + '\n' + imports + content[insert_pos:]
    
    # Add keystore properties if not present (before android block)
    if 'keystorePropertiesFile' not in content:
        android_match = re.search(r'\nandroid \{', content)
        if android_match:
            content = content[:android_match.start()+1] + keystore_props + content[android_match.start()+1:]
    
    with open(file_path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: update_build_gradle.py <file_path> <package_name>")
        sys.exit(1)
    
    update_build_gradle(sys.argv[1], sys.argv[2])
