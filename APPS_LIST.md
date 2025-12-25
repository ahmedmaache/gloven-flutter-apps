# 100 Flutter Apps - Complete List

## Package Naming Convention

All apps use the format: `org.gloven.app{01-100}`

## Apps List

| App | Package Name | Icons | Status |
|-----|--------------|-------|--------|
| app01 | org.gloven.app01 | 5 sizes | ✅ Ready |
| app02 | org.gloven.app02 | 5 sizes | ✅ Ready |
| app03 | org.gloven.app03 | 5 sizes | ✅ Ready |
| ... | ... | ... | ... |
| app100 | org.gloven.app100 | 5 sizes | ✅ Ready |

## Icon Information

Each app includes default Flutter launcher icons in multiple sizes:
- **mipmap-mdpi**: 48x48 pixels
- **mipmap-hdpi**: 72x72 pixels  
- **mipmap-xhdpi**: 96x96 pixels
- **mipmap-xxhdpi**: 144x144 pixels
- **mipmap-xxxhdpi**: 192x192 pixels

Icon location: `apps/{app_name}/android/app/src/main/res/mipmap-*/ic_launcher.png`

## Customization

To customize icons for each app:
1. Replace icons in `apps/{app_name}/android/app/src/main/res/mipmap-*/ic_launcher.png`
2. Update app name in `pubspec.yaml`
3. Update app label in `AndroidManifest.xml`

## Full List

Run `python3 scripts/list_apps.py` to see the complete list with details.

