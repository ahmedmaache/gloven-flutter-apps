# GitHub Actions Setup Prompt for Coding Agent

## Context & Project Overview

You are working on a Flutter project that contains **100 unique game applications**. Each game is located in `apps/app01` through `apps/app100`, with package names `org.gloven.app01` through `org.gloven.app100`.

### Project Structure
```
/home/maache/new-flutter-apps/
├── apps/
│   ├── app01/          # Number Slide Puzzle
│   ├── app02/          # Color Match Challenge
│   ├── ...
│   └── app100/         # Traffic Controller
├── .github/workflows/
│   ├── build-all-apps.yml
│   ├── build-single-app.yml
│   └── publish-to-playstore.yml
├── scripts/
│   ├── setup_keystore.sh
│   ├── update_build_gradle.py
│   └── ...
└── gloven-keystore.jks  # Android signing keystore (NOT in repo)
```

### Current Status
- ✅ 100 Flutter games created with unique implementations
- ✅ Each game has: dark mode, sound, vibration, difficulty levels, tutorials
- ✅ Android signing configuration in place
- ✅ GitHub repository exists
- ⏳ Need: GitHub Actions workflow to build signed AAB files
- ⏳ Need: GitHub storage for artifacts

## Task: Set Up GitHub Actions for Building Signed AAB Files

### Requirements

1. **Build all 100 apps in parallel** (or in batches)
2. **Generate signed AAB files** for each app
3. **Store artifacts** in GitHub Actions (90-day retention)
4. **Use GitHub storage** efficiently
5. **Handle signing** with keystore from GitHub Secrets

### Key Information

#### 1. Keystore Details
- **Keystore file**: `gloven-keystore.jks`
- **Location**: Root directory (NOT committed to git)
- **Base64 encoded**: Available in `keystore_base64.txt` (if exists)
- **Key properties file**: `key.properties` (per app, in `android/app/`)

#### 2. Required GitHub Secrets

Set these secrets in GitHub repository settings:

```
KEYSTORE_PASSWORD=<keystore_password>
KEY_PASSWORD=<key_password>
KEY_ALIAS=<key_alias>
KEYSTORE_BASE64=<base64_encoded_keystore>
```

**How to get KEYSTORE_BASE64:**
```bash
base64 -i gloven-keystore.jks > keystore_base64.txt
# Copy contents of keystore_base64.txt to GitHub Secret
```

#### 3. Package Names
All apps follow pattern: `org.gloven.app{01-100}`

#### 4. Build Configuration

Each app's `android/app/build.gradle.kts` has:
- Signing config named "release"
- References `key.properties` file
- Package name: `org.gloven.app{NN}`

#### 5. Key Properties File Structure

Each app needs `android/app/key.properties`:
```properties
storePassword=<KEYSTORE_PASSWORD>
keyPassword=<KEY_PASSWORD>
keyAlias=<KEY_ALIAS>
storeFile=gloven-keystore.jks
```

### GitHub Actions Workflow Requirements

#### Workflow File: `.github/workflows/build-all-apps.yml`

**Requirements:**
1. **Trigger**: On push to main branch, or manual workflow dispatch
2. **Matrix Strategy**: Build all 100 apps (app01-app100)
3. **Parallel Jobs**: Maximum 10 concurrent jobs (to avoid rate limits)
4. **Steps**:
   - Checkout code
   - Set up Java (JDK 17)
   - Set up Flutter
   - Decode keystore from secret
   - Create key.properties for each app
   - Install dependencies
   - Build signed AAB file
   - Upload artifact to GitHub Actions
   - Optional: Create GitHub Release with artifacts

#### Workflow Steps Detail

**Step 1: Checkout**
```yaml
- uses: actions/checkout@v4
```

**Step 2: Setup Java**
```yaml
- uses: actions/setup-java@v4
  with:
    distribution: 'temurin'
    java-version: '17'
```

**Step 3: Setup Flutter**
```yaml
- uses: subosito/flutter-action@v2
  with:
    flutter-version: '3.38.5'
    channel: 'stable'
```

**Step 4: Decode Keystore**
```yaml
- name: Decode keystore
  run: |
    echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > gloven-keystore.jks
    chmod 600 gloven-keystore.jks
```

**Step 5: Create key.properties**
```yaml
- name: Create key.properties
  run: |
    cd apps/app$(printf "%02d" ${{ matrix.app_number }})
    cat > android/app/key.properties << EOF
    storePassword=${{ secrets.KEYSTORE_PASSWORD }}
    keyPassword=${{ secrets.KEY_PASSWORD }}
    keyAlias=${{ secrets.KEY_ALIAS }}
    storeFile=../../gloven-keystore.jks
    EOF
```

**Step 6: Install Dependencies**
```yaml
- name: Install dependencies
  run: |
    cd apps/app$(printf "%02d" ${{ matrix.app_number }})
    flutter pub get
```

**Step 7: Build AAB**
```yaml
- name: Build AAB
  run: |
    cd apps/app$(printf "%02d" ${{ matrix.app_number }})
    flutter build appbundle --release
```

**Step 8: Upload Artifact**
```yaml
- name: Upload AAB
  uses: actions/upload-artifact@v4
  with:
    name: app$(printf "%02d" ${{ matrix.app_number }})-aab
    path: apps/app$(printf "%02d" ${{ matrix.app_number }})/build/app/outputs/bundle/release/app-release.aab
    retention-days: 90
```

### Matrix Strategy Configuration

```yaml
strategy:
  matrix:
    app_number: [1, 2, 3, ..., 100]  # All 100 apps
  max-parallel: 10  # Limit concurrent builds
```

### Complete Workflow Template

```yaml
name: Build All Apps

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-apps:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        app_number: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
      max-parallel: 10
      fail-fast: false

    steps:
      - uses: actions/checkout@v4

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.5'
          channel: 'stable'

      - name: Decode keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > gloven-keystore.jks
          chmod 600 gloven-keystore.jks

      - name: Create key.properties
        run: |
          cd apps/app$(printf "%02d" ${{ matrix.app_number }})
          cat > android/app/key.properties << EOF
          storePassword=${{ secrets.KEYSTORE_PASSWORD }}
          keyPassword=${{ secrets.KEY_PASSWORD }}
          keyAlias=${{ secrets.KEY_ALIAS }}
          storeFile=../../gloven-keystore.jks
          EOF

      - name: Install dependencies
        run: |
          cd apps/app$(printf "%02d" ${{ matrix.app_number }})
          flutter pub get

      - name: Build AAB
        run: |
          cd apps/app$(printf "%02d" ${{ matrix.app_number }})
          flutter build appbundle --release

      - name: Upload AAB artifact
        uses: actions/upload-artifact@v4
        with:
          name: app$(printf "%02d" ${{ matrix.app_number }})-aab
          path: apps/app$(printf "%02d" ${{ matrix.app_number }})/build/app/outputs/bundle/release/app-release.aab
          retention-days: 90
          if-no-files-found: error
```

### Important Notes

1. **Keystore Path**: The keystore is decoded to root directory, so `storeFile` in key.properties should be `../../gloven-keystore.jks` (relative from `android/app/`)

2. **Artifact Naming**: Use format `app{NN}-aab` for easy identification

3. **Retention**: 90 days is GitHub Actions default maximum

4. **Error Handling**: Set `fail-fast: false` in matrix strategy so one failure doesn't stop all builds

5. **Parallel Limits**: `max-parallel: 10` prevents overwhelming GitHub runners

6. **Flutter Version**: Use exact version `3.38.5` or latest stable

### Verification Steps

After workflow runs:
1. Check Actions tab for build status
2. Download artifacts to verify AAB files
3. Verify AAB files are signed (can use `jarsigner -verify`)
4. Check artifact storage (90-day retention)

### Troubleshooting

**Common Issues:**
1. **Keystore not found**: Check keystore path in key.properties
2. **Signing failed**: Verify all secrets are set correctly
3. **Build timeout**: Increase timeout or reduce max-parallel
4. **Out of storage**: GitHub Actions has storage limits per repository

### Additional Workflow: Single App Build

Create `.github/workflows/build-single-app.yml` for on-demand builds:

```yaml
name: Build Single App

on:
  workflow_dispatch:
    inputs:
      app_number:
        description: 'App number (1-100)'
        required: true
        type: number

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Same steps as above, but use ${{ github.event.inputs.app_number }}
```

### Storage Management

**GitHub Actions Storage Limits:**
- Free tier: 500 MB storage, 1 GB transfer/month
- Artifacts count toward storage
- 90-day retention maximum

**Optimization Tips:**
1. Only upload AAB files (not APK)
2. Use artifact compression
3. Clean up old artifacts manually if needed
4. Consider using GitHub Releases for long-term storage

### Next Steps After Setup

1. **Set GitHub Secrets**: Add all required secrets in repository settings
2. **Test Workflow**: Run workflow manually first
3. **Monitor Builds**: Check for any errors
4. **Download Artifacts**: Verify AAB files are correctly signed
5. **Publish to Play Store**: Use AAB files for Play Console upload

### Required Files to Check

Before running workflow, verify:
- ✅ `.github/workflows/build-all-apps.yml` exists
- ✅ All apps have `android/app/build.gradle.kts` with signing config
- ✅ GitHub Secrets are set (KEYSTORE_PASSWORD, KEY_PASSWORD, KEY_ALIAS, KEYSTORE_BASE64)
- ✅ Keystore file exists (for base64 encoding)

### Command Reference

**Encode keystore for GitHub Secret:**
```bash
base64 -i gloven-keystore.jks | pbcopy  # macOS
base64 -i gloven-keystore.jks | xclip   # Linux
```

**Verify AAB is signed:**
```bash
jarsigner -verify -verbose -certs app-release.aab
```

**Check workflow logs:**
- Go to GitHub repository → Actions tab
- Click on workflow run
- Check individual job logs

---

## Summary for Coding Agent

**Your task**: Create/update the GitHub Actions workflow file `.github/workflows/build-all-apps.yml` that:
1. Builds all 100 Flutter apps (app01-app100) as signed AAB files
2. Uses GitHub Secrets for keystore and signing credentials
3. Uploads artifacts to GitHub Actions storage (90-day retention)
4. Handles parallel builds efficiently (max 10 concurrent)
5. Includes proper error handling and logging

**Key files to modify:**
- `.github/workflows/build-all-apps.yml` (main workflow)
- Optionally: `.github/workflows/build-single-app.yml` (single app build)

**Prerequisites:**
- GitHub Secrets must be set: KEYSTORE_PASSWORD, KEY_PASSWORD, KEY_ALIAS, KEYSTORE_BASE64
- All apps must have proper Android signing configuration
- Flutter 3.38.5+ must be available in workflow

**Expected outcome:**
- Workflow runs successfully
- All 100 AAB files are built and signed
- Artifacts are available in GitHub Actions for 90 days
- Each artifact named: `app{NN}-aab`

