# Gloven Flutter Apps - Setup Guide

## Overview
This project contains 100 Flutter applications configured for Google Play Store publishing with package names under `org.gloven.*`.

## Quick Start

### 1. Generate All 100 Apps

```bash
# Option 1: Generate sequentially (slower but more reliable)
./scripts/generate_all_apps.sh

# Option 2: Generate in parallel (faster, uses multiprocessing)
python3 scripts/generate_apps_parallel.py
```

### 2. Set Up Keystore for Signing

```bash
# Generate keystore (run once)
./scripts/setup_keystore.sh

# Note: Update the passwords in the script or use the generated keystore
```

### 3. Configure GitHub Secrets

Before using GitHub Actions, set up the following secrets in your GitHub repository:

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

2. Add these secrets:
   - `KEYSTORE_PASSWORD` - Your keystore password
   - `KEY_PASSWORD` - Your key password  
   - `KEY_ALIAS` - Key alias (default: `gloven-key`)
   - `KEYSTORE_BASE64` - Base64 encoded keystore file
     ```bash
     base64 -i gloven-keystore.jks | pbcopy  # macOS
     base64 -i gloven-keystore.jks | xclip   # Linux
     ```
   - `GCP_SA_KEY` - Google Cloud Service Account JSON for Play Store API
   - `GCP_PROJECT_ID` - Google Cloud Project ID

Or use GitHub CLI:
```bash
gh secret set KEYSTORE_PASSWORD
gh secret set KEY_PASSWORD
gh secret set KEY_ALIAS
gh secret set KEYSTORE_BASE64 < <(base64 -i gloven-keystore.jks)
gh secret set GCP_SA_KEY < service-account.json
gh secret set GCP_PROJECT_ID
```

### 4. Build AAB Files

#### Using GitHub Actions (Recommended)

1. **Build All Apps**: Push to main branch triggers build for all 100 apps
2. **Build Single App**: Use workflow dispatch in GitHub Actions UI
3. **Build in Parallel**: The workflow builds up to 10 apps in parallel

#### Manual Build

```bash
cd apps/app01
flutter build appbundle --release
```

### 5. Publish to Play Store

#### Using GitHub Actions

1. Go to Actions tab
2. Select "Publish to Google Play Store" workflow
3. Click "Run workflow"
4. Select app number (1-100) or "all"
5. Select track (internal/alpha/beta/production)

#### Manual Publishing

Use Google Play Console or `fastlane` with your service account.

## Project Structure

```
.
├── apps/                    # All 100 Flutter apps
│   ├── app01/
│   ├── app02/
│   └── ...
├── scripts/                 # Automation scripts
│   ├── create_app_template.sh
│   ├── generate_all_apps.sh
│   ├── generate_apps_parallel.py
│   ├── setup_keystore.sh
│   └── setup_github_secrets.sh
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── build-all-apps.yml
│       ├── build-single-app.yml
│       └── publish-to-playstore.yml
└── README.md
```

## Package Naming

All apps use the format: `org.gloven.app{01-100}`

Examples:
- App 1: `org.gloven.app01`
- App 50: `org.gloven.app50`
- App 100: `org.gloven.app100`

## GitHub Resources Used

1. **GitHub Actions**: For CI/CD and building AAB files
2. **GitHub Codespaces**: For development environment (optional)
3. **GitHub Storage**: Artifacts stored for 90 days
4. **GitHub Releases**: AAB files uploaded as releases

## Next Steps

1. Generate all 100 apps
2. Customize each app's functionality
3. Set up Google Play Console accounts
4. Configure app store listings
5. Publish apps to Play Store

## Troubleshooting

### Build Failures
- Check Flutter version compatibility
- Verify keystore configuration
- Check GitHub Actions logs

### Signing Issues
- Ensure keystore file is properly encoded in GitHub Secrets
- Verify passwords match in key.properties and secrets

### Play Store Publishing
- Verify service account has correct permissions
- Check package names match Play Console entries
- Ensure apps are created in Play Console first

