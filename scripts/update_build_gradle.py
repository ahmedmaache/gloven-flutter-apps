#!/usr/bin/env python3
"""Update build.gradle.kts with signing configuration"""

import re
import sys

def update_build_gradle(file_path, package_name):
    """Update build.gradle.kts with signing config"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports at the top if needed
    imports_needed = '''import java.util.Properties
import java.io.FileInputStream

'''
    
    # Always update package name if needed
    if f'namespace = "{package_name}"' not in content:
        content = re.sub(r'namespace = "[^"]*"', f'namespace = "{package_name}"', content)
        content = re.sub(r'applicationId = "[^"]*"', f'applicationId = "{package_name}"', content)
    
    # Check if we need to add imports
    needs_imports = 'import java.util.Properties' not in content
    
    # Check if we need to update keystore properties code
    needs_keystore_update = 'keystorePropertiesFile' not in content or 'java.util.Properties()' in content
    
    # Check if signing config already exists
    has_signing_config = 'signingConfigs {' in content or 'signingConfigs.create' in content
    
    # Add keystore properties before android block (using imported classes)
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
    
    # Find buildTypes and insert signingConfigs before it (only if not already exists)
    if not has_signing_config:
        buildtypes_match = re.search(r'(\s+)buildTypes \{', content)
        if buildtypes_match:
            indent = buildtypes_match.group(1)
            insert_pos = buildtypes_match.start()
            # Adjust signing config indentation
            signing_config_indented = re.sub(r'^    ', indent, signing_config, flags=re.MULTILINE)
            content = content[:insert_pos] + signing_config_indented + content[insert_pos:]
    elif not has_signing_config:
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
    
    # Add imports if needed (after plugins block)
    if needs_imports:
        plugins_match = re.search(r'(plugins \{[^}]*\})', content, re.DOTALL)
        if plugins_match:
            insert_pos = plugins_match.end()
            content = content[:insert_pos] + '\n' + imports_needed + content[insert_pos:]
    
    # Update keystore properties code if needed
    if needs_keystore_update:
        # Remove old keystore properties code if it exists (more comprehensive pattern)
        patterns_to_remove = [
            r'val keystorePropertiesFile = rootProject\.file\("key\.properties"\)\n',
            r'val keystoreProperties = java\.util\.Properties\(\)\n',
            r'val keystoreProperties = Properties\(\)\n',
            r'if \(keystorePropertiesFile\.exists\(\)\) \{\s*\n\s*keystoreProperties\.load\([^)]+\)\s*\n\}\s*\n',
            r'keystoreProperties\.load\(java\.io\.FileInputStream\(keystorePropertiesFile\)\)',
            r'keystoreProperties\.load\(FileInputStream\(keystorePropertiesFile\)\)',
        ]
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Remove duplicate keystorePropertiesFile lines
        lines = content.split('\n')
        seen_keystore = False
        new_lines = []
        for line in lines:
            if 'val keystorePropertiesFile' in line:
                if not seen_keystore:
                    new_lines.append(line)
                    seen_keystore = True
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)
        
        # Add new keystore properties before android block (only if not already there)
        if 'val keystorePropertiesFile = rootProject.file("key.properties")' not in content:
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
