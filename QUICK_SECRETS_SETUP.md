# Quick GitHub Secrets Setup

## ✅ Already Configured
- KEYSTORE_PASSWORD ✓

## ⚡ Quick Setup (2 minutes)

### Option 1: Use GitHub Web UI (Easiest)

1. Go to: https://github.com/ahmedmaache/gloven-flutter-apps/settings/secrets/actions

2. Click "New repository secret" for each:

   **KEY_PASSWORD**
   - Name: `KEY_PASSWORD`
   - Value: `changeit`

   **KEY_ALIAS**
   - Name: `KEY_ALIAS`
   - Value: `gloven-key`

   **KEYSTORE_BASE64**
   - Name: `KEYSTORE_BASE64`
   - Value: Copy entire contents of `keystore_base64.txt`
   ```bash
   cat keystore_base64.txt
   # Copy the entire output
   ```

### Option 2: Use GitHub CLI (if available)

```bash
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
echo "$GITHUB_TOKEN" | gh auth login --with-token

echo "changeit" | gh secret set KEY_PASSWORD --repo ahmedmaache/gloven-flutter-apps
echo "gloven-key" | gh secret set KEY_ALIAS --repo ahmedmaache/gloven-flutter-apps
cat keystore_base64.txt | gh secret set KEYSTORE_BASE64 --repo ahmedmaache/gloven-flutter-apps
```

## Required Secrets Summary

| Secret Name | Value | Status |
|------------|-------|--------|
| KEYSTORE_PASSWORD | `changeit` | ✅ Set |
| KEY_PASSWORD | `changeit` | ⏳ Need to set |
| KEY_ALIAS | `gloven-key` | ⏳ Need to set |
| KEYSTORE_BASE64 | From `keystore_base64.txt` | ⏳ Need to set |
| GCP_SA_KEY | (Optional) Google Play SA JSON | ⏳ Optional |
| GCP_PROJECT_ID | (Optional) GCP Project ID | ⏳ Optional |

## After Setting Secrets

Once all 4 required secrets are set, GitHub Actions will automatically:
- ✅ Build all 100 apps
- ✅ Create signed AAB files
- ✅ Upload artifacts
- ✅ Create releases

**Trigger builds**: Push to main or manually trigger in Actions tab!

