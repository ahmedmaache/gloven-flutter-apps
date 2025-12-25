
# 🔐 Setting up GitHub Secrets

To enable the automated build pipeline I created, you need to add these secrets to your GitHub Repository.

## 1. Get the Secret Values

Run this command to see your Keystore Base64 string (copy the whole output):
```bash
cat keystore_base64.txt
```

## 2. Go to GitHub
1.  Navigate to your repository on GitHub.
2.  Go to **Settings** -> **Secrets and variables** -> **Actions**.
3.  Click **New repository secret**.

## 3. Add These 4 Secrets

| Name | Value |
| :--- | :--- |
| **KEYSTORE_BASE64** | (Paste the long string from step 1) |
| **KEY_ALIAS** | `gloven` |
| **KEY_PASSWORD** | `gloven2024` |
| **STORE_PASSWORD** | `gloven2024` |

## 🚀 How to Run
Once secrets are added:
1.  Go to the **Actions** tab in GitHub.
2.  Select **Build and Release Flutter Apps** on the left.
3.  Click **Run workflow**.

The system will build all apps and produce a zip file called `signed-aabs` containing all your release bundles!
