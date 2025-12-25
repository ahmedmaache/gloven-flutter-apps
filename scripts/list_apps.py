#!/usr/bin/env python3
"""List all Flutter apps with package names and icon information"""

import os
from pathlib import Path
import json

def get_app_info(app_dir):
    """Get information about an app"""
    app_name = app_dir.name
    package_name = f"org.gloven.{app_name}"
    
    # Get package name from build.gradle.kts
    build_gradle = app_dir / "android" / "app" / "build.gradle.kts"
    if build_gradle.exists():
        with open(build_gradle, 'r') as f:
            content = f.read()
            # Extract namespace/applicationId
            import re
            namespace_match = re.search(r'namespace\s*=\s*"([^"]+)"', content)
            appid_match = re.search(r'applicationId\s*=\s*"([^"]+)"', content)
            if namespace_match:
                package_name = namespace_match.group(1)
            elif appid_match:
                package_name = appid_match.group(1)
    
    # Find icon files
    icon_paths = []
    icon_dir = app_dir / "android" / "app" / "src" / "main" / "res"
    if icon_dir.exists():
        for mipmap_dir in icon_dir.glob("mipmap-*/ic_launcher.png"):
            icon_paths.append(str(mipmap_dir.relative_to(app_dir)))
    
    # Get app name from pubspec.yaml
    pubspec = app_dir / "pubspec.yaml"
    app_title = app_name
    if pubspec.exists():
        with open(pubspec, 'r') as f:
            content = f.read()
            # Extract description
            import re
            desc_match = re.search(r'description:\s*(.+)', content)
            if desc_match:
                app_title = desc_match.group(1).strip()
    
    return {
        'app_name': app_name,
        'package_name': package_name,
        'app_title': app_title,
        'icon_count': len(icon_paths),
        'icon_paths': icon_paths
    }

def main():
    apps_dir = Path("apps")
    apps = sorted([d for d in apps_dir.iterdir() if d.is_dir() and d.name.startswith("app")])
    
    print("=" * 100)
    print(f"{'APP':<10} | {'PACKAGE NAME':<35} | {'ICONS':<15} | {'TITLE'}")
    print("=" * 100)
    
    for app_dir in apps:
        info = get_app_info(app_dir)
        icon_info = f"{info['icon_count']} sizes" if info['icon_count'] > 0 else "Default"
        title = info['app_title'][:40] if len(info['app_title']) > 40 else info['app_title']
        
        print(f"{info['app_name']:<10} | {info['package_name']:<35} | {icon_info:<15} | {title}")
    
    print("=" * 100)
    print(f"\nTotal: {len(apps)} apps")
    print(f"Package prefix: org.gloven.*")
    print(f"\nIcon locations: android/app/src/main/res/mipmap-*/ic_launcher.png")
    print(f"  - mipmap-mdpi: 48x48")
    print(f"  - mipmap-hdpi: 72x72")
    print(f"  - mipmap-xhdpi: 96x96")
    print(f"  - mipmap-xxhdpi: 144x144")
    print(f"  - mipmap-xxxhdpi: 192x192")

if __name__ == "__main__":
    main()

