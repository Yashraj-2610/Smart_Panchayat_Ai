# GitHub Setup Guide - Smart Panchayat AI

## Option 1: Using GitHub Desktop (Easiest)

1. **Download GitHub Desktop** (if not installed): https://desktop.github.com/
2. Open GitHub Desktop and sign in to your GitHub account
3. Click **File** → **Add Local Repository**
4. Browse to: `C:\Users\yashr\Downloads\AI\smart-panchayat-ai`
5. Click **Publish repository**
6. Repository name: `smart-panchayat-ai`
7. Description: "AI-Powered Panchayat Decision Support System - Minor Project"
8. Uncheck "Keep this code private" if you want it public
9. Click **Publish repository**

✅ Done! Your project is now on GitHub!

---

## Option 2: Using Git Command Line (Manual)

### Step 1: Configure Git (One-time setup)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 2: Initialize and Commit
```bash
cd "C:\Users\yashr\Downloads\AI\smart-panchayat-ai"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Smart Panchayat AI System"
```

### Step 3: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `smart-panchayat-ai`
3. Description: "AI-Powered Panchayat Decision Support System for Smart Village Development"
4. Choose Public or Private
5. **Don't initialize with README** (we already have one)
6. Click **Create repository**

### Step 4: Push to GitHub
GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smart-panchayat-ai.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 5: Enter Credentials
When prompted:
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your password)
  - Get token from: https://github.com/settings/tokens
  - Generate new token (classic)
  - Select `repo` scope
  - Copy and paste the token when asked for password

✅ Done! Your project is now on GitHub!

---

## Option 3: Using GitHub CLI (If installed)

```bash
cd "C:\Users\yashr\Downloads\AI\smart-panchayat-ai"

# Login to GitHub
gh auth login

# Add and commit files
git add .
git commit -m "Initial commit: Smart Panchayat AI System"

# Create repo and push
gh repo create smart-panchayat-ai --public --source=. --push
```

---

## After Pushing to GitHub

Your repository URL will be:
```
https://github.com/YOUR_USERNAME/smart-panchayat-ai
```

### Recommended: Add Topics/Tags
On GitHub repository page, click ⚙️ Settings → Topics:
- `ai`
- `machine-learning`
- `multi-agent-system`
- `panchayat`
- `smart-village`
- `fastapi`
- `streamlit`
- `rag`
- `explainable-ai`
- `multilingual`

### Recommended: Enable GitHub Pages (Optional)
1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/ (root)`
4. Save

---

## Repository Features to Enable

- ✅ Issues (for bug tracking)
- ✅ Discussions (for Q&A)
- ✅ Wiki (for extended documentation)
- ✅ Projects (for roadmap tracking)

---

## Sharing Your Project

After pushing, share:
```
🎯 Smart Panchayat AI - AI-Powered Decision Support System

GitHub: https://github.com/YOUR_USERNAME/smart-panchayat-ai

Features:
✅ Multi-Agent AI System
✅ RAG Knowledge Base
✅ Explainable Recommendations
✅ Multilingual (English, Hindi, Marathi)
✅ Real-time Analytics Dashboard

Tech: FastAPI, Streamlit, SQLAlchemy, Python
```

---

## Need Help?

If you encounter issues:
1. Make sure git is installed: `git --version`
2. Check your GitHub account access
3. For authentication issues, use Personal Access Token
4. GitHub Desktop is easiest for first-time users

---

**I recommend Option 1 (GitHub Desktop) - it's the simplest and most visual!**
