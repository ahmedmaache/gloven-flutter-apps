# 🔐 Set GitHub Secrets - Required for Build

## ❌ Current Error

The workflow is failing with:
```
❌ Error: KEYSTORE_PASSWORD secret is not set
```

## ✅ Solution: Set 4 Secrets

### Step 1: Go to Secrets Page

**Direct Link**: https://github.com/ahmedmaache/gloven-flutter-apps/settings/secrets/actions

### Step 2: Add Each Secret

Click **"New repository secret"** for each of these:

#### Secret 1: KEYSTORE_PASSWORD
- **Name**: `KEYSTORE_PASSWORD`
- **Value**: `changeit`

#### Secret 2: KEY_PASSWORD
- **Name**: `KEY_PASSWORD`
- **Value**: `changeit`

#### Secret 3: KEY_ALIAS
- **Name**: `KEY_ALIAS`
- **Value**: `gloven-key`

#### Secret 4: KEYSTORE_BASE64
- **Name**: `KEYSTORE_BASE64`
- **Value**: Copy the entire contents from `keystore_base64.txt` file
  - It's a long single line (3721 characters)
  - Copy everything, including the beginning and end
  - No line breaks

### Step 3: Verify Secrets

After adding all 4 secrets, you should see them listed on the secrets page.

### Step 4: Re-run Workflow

1. Go to: https://github.com/ahmedmaache/gloven-flutter-apps/actions
2. Find **"🔨 Build Single App (Debug Mode)"**
3. Click **"Run workflow"** (top right)
4. Enter app number: `01`
5. Click **"Run workflow"** (green button)

## 📋 Quick Reference

| Secret Name | Value | Status |
|------------|-------|--------|
| KEYSTORE_PASSWORD | `changeit` | ⏳ Set this |
| KEY_PASSWORD | `changeit` | ⏳ Set this |
| KEY_ALIAS | `gloven-key` | ⏳ Set this |
| KEYSTORE_BASE64 | From `keystore_base64.txt` | ⏳ Set this |

## 🔗 Links

- **Secrets Page**: https://github.com/ahmedmaache/gloven-flutter-apps/settings/secrets/actions
- **Actions Page**: https://github.com/ahmedmaache/gloven-flutter-apps/actions
- **Workflow**: 🔨 Build Single App (Debug Mode)

