# GitHub Resources Setup for 100 Flutter Apps

## Overview
This project leverages GitHub's infrastructure to build, store, and publish 100 Flutter apps to Google Play Store.

## GitHub Resources Utilized

### 1. GitHub Actions
- **Build All Apps Workflow**: Automatically builds all 100 apps in parallel (10 at a time)
- **Build Single App Workflow**: Build individual apps on demand
- **Publish to Play Store**: Automated publishing workflow

### 2. GitHub Codespaces (Optional)
- Use GitHub Codespaces for cloud-based development
- Pre-configured with Flutter SDK
- Access from anywhere

### 3. GitHub Storage
- **Artifacts**: AAB files stored for 90 days
- **Releases**: AAB files attached to GitHub releases
- **Repository**: All source code stored in GitHub

### 4. GitHub Secrets
Store sensitive information securely:
- Keystore passwords
- Google Play Service Account credentials
- Signing keys

## Setup Instructions

### Step 1: Create GitHub Repository

```bash
# Initialize and push to GitHub
git add .
git commit -m "Initial commit: 100 Flutter apps setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gloven-flutter-apps.git
git push -u origin main
```

### Step 2: Configure GitHub Secrets

1. Navigate to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`
2. Add the following secrets:

#### Required Secrets:

**KEYSTORE_PASSWORD**
- Your keystore password

**KEY_PASSWORD**
- Your key password

**KEY_ALIAS**
- Key alias (default: `gloven-key`)

**KEYSTORE_BASE64**
- Base64 encoded keystore file
- Generate: `base64 -i gloven-keystore.jks`

**GCP_SA_KEY**
- Google Cloud Service Account JSON
- Required for Play Store API access
- Create at: https://console.cloud.google.com/iam-admin/serviceaccounts

**GCP_PROJECT_ID**
- Your Google Cloud Project ID

### Step 3: Generate Keystore

```bash
./scripts/setup_keystore.sh
```

Then encode it:
```bash
base64 -i gloven-keystore.jks | pbcopy  # macOS
base64 -i gloven-keystore.jks | xclip   # Linux
```

Paste the output into GitHub Secret `KEYSTORE_BASE64`.

### Step 4: Set Up Google Play Console

1. Create a Google Play Developer account
2. Create 100 app entries in Play Console (one for each package name)
3. Set up Service Account with Play Console API access
4. Download service account JSON
5. Add JSON content to GitHub Secret `GCP_SA_KEY`

### Step 5: Generate All 100 Apps

```bash
# This will take some time (30-60 minutes)
python3 scripts/generate_apps_parallel.py
```

Or generate sequentially:
```bash
./scripts/generate_all_apps.sh
```

### Step 6: Push to GitHub

```bash
git add .
git commit -m "Add 100 Flutter apps"
git push origin main
```

This will trigger the build workflow automatically!

## Workflow Usage

### Build All Apps
- Triggered automatically on push to main
- Builds all 100 apps in parallel (10 at a time)
- Uploads AAB files as artifacts
- Creates GitHub releases for each app

### Build Single App
1. Go to Actions tab
2. Select "Build Single Flutter App"
3. Click "Run workflow"
4. Enter app number (1-100)
5. Workflow builds and uploads AAB

### Publish to Play Store
1. Go to Actions tab
2. Select "Publish to Google Play Store"
3. Click "Run workflow"
4. Select:
   - App number (1-100) or "all"
   - Track (internal/alpha/beta/production)
5. Workflow publishes to Play Store

## Monitoring

### View Build Status
- Go to Actions tab to see all workflow runs
- Click on a run to see detailed logs
- Download AAB files from artifacts

### View Releases
- Go to Releases tab
- Each app has its own release with AAB file
- Tag format: `app{NN}-v{BUILD_NUMBER}`

## Cost Considerations

### GitHub Actions
- Free tier: 2,000 minutes/month
- Building 100 apps: ~10-15 minutes per app
- Total: ~1,000-1,500 minutes per full build
- **Recommendation**: Build in batches or use self-hosted runners

### GitHub Storage
- Artifacts: 90 days retention (free)
- Releases: Unlimited (free)
- Repository: 1GB free, then $0.008/GB/month

### Optimization Tips

1. **Build on Demand**: Use workflow_dispatch instead of automatic builds
2. **Batch Building**: Build apps in smaller batches (10-20 at a time)
3. **Self-Hosted Runners**: Use your own infrastructure for unlimited builds
4. **Conditional Builds**: Only build changed apps

## Troubleshooting

### Build Failures
- Check Actions logs for errors
- Verify Flutter version compatibility
- Ensure keystore is properly configured

### Signing Issues
- Verify keystore base64 encoding
- Check passwords match in secrets
- Ensure key.properties template is correct

### Play Store Publishing
- Verify service account permissions
- Check package names match Play Console
- Ensure apps exist in Play Console first

## Next Steps

1. ✅ Repository structure created
2. ✅ GitHub Actions workflows configured
3. ✅ Scripts for app generation ready
4. ⏳ Generate 100 apps (run script)
5. ⏳ Configure GitHub Secrets
6. ⏳ Set up Google Play Console
7. ⏳ Push to GitHub and trigger builds
8. ⏳ Publish to Play Store

## Support

For issues or questions:
- Check GitHub Actions logs
- Review SETUP.md for detailed instructions
- Verify all secrets are configured correctly

