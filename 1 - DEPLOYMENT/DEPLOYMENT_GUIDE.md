# 🚀 Deployment Guide - Your Own Deployment

## Overview

This guide will help you deploy your Physical AI Robotics textbook to your own GitHub Pages.

---

## Prerequisites

✅ GitHub account
✅ Git installed
✅ Node.js installed (v20+)
✅ Your project ready

---

## Step 1: Update Configuration

### 1.1 Update `docusaurus.config.ts`

Open `book/docusaurus.config.ts` and update these fields:

```typescript
const config: Config = {
  // Change to YOUR GitHub Pages URL
  url: 'https://YOUR_GITHUB_USERNAME.github.io',
  
  // Keep as is or change project name
  baseUrl: '/robotics/',
  
  // Change to YOUR GitHub username
  organizationName: 'YOUR_GITHUB_USERNAME',
  
  // Change to YOUR repository name
  projectName: 'YOUR_REPO_NAME',
  
  // ... rest of config
};
```

**Example:**
```typescript
url: 'https://AQI.github.io',
baseUrl: '/robotics/',
organizationName: 'AQI',
projectName: 'robotics-textbook',
```

---

## Step 2: Create GitHub Repository

### 2.1 Create New Repository

1. Go to https://github.com/new
2. Repository name: `robotics-textbook` (or your choice)
3. Make it **Public**
4. **Don't** initialize with README
5. Click "Create repository"

### 2.2 Push Your Code

```powershell
# Navigate to your project
cd C:\Users\AQI\OneDrive\Desktop\HACKATHON\physical-ai-textbook-main

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Robotics textbook with redesigned UI"

# Add remote (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

---

## Step 3: Enable GitHub Pages

### 3.1 Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Save

---

## Step 4: Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
          cache-dependency-path: book/package-lock.json
      
      - name: Install dependencies
        run: |
          cd book
          npm ci
      
      - name: Build website
        run: |
          cd book
          npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: book/build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Step 5: Deploy!

### 5.1 Create the workflow file

```powershell
# Create .github/workflows directory
mkdir -p .github/workflows

# Create the file (you can use notepad or VS Code)
notepad .github\workflows\deploy.yml
```

Paste the YAML content above and save.

### 5.2 Push to GitHub

```powershell
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push
```

### 5.3 Wait for Deployment

1. Go to your repository on GitHub
2. Click **Actions** tab
3. You'll see the deployment running
4. Wait for it to complete (usually 2-5 minutes)

---

## Step 6: Access Your Site

Your site will be available at:

```
https://YOUR_USERNAME.github.io/robotics/
```

Example:
```
https://AQI.github.io/robotics/
```

---

## Deploying Auth Backend (Optional)

### Option 1: Render.com (Recommended)

1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: robotics-auth-backend
   - **Root Directory**: `auth-backend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Environment Variables**:
     ```
     DATABASE_URL=your_postgres_url
     BETTER_AUTH_SECRET=your_secret
     FRONTEND_URL=https://YOUR_USERNAME.github.io
     PORT=3001
     ```
6. Click "Create Web Service"

### Option 2: Vercel

1. Go to https://vercel.com
2. Import your repository
3. Configure for `auth-backend` directory
4. Add environment variables
5. Deploy

---

## Troubleshooting

### Build Fails

**Check:**
- Node version is 20+
- All dependencies installed
- No TypeScript errors

**Fix:**
```powershell
cd book
npm ci
npm run build
```

### 404 Error

**Check:**
- `baseUrl` in config matches repository name
- GitHub Pages is enabled
- Deployment completed successfully

### Images Not Loading

**Check:**
- Images are in `book/static/img/`
- Paths use `/img/` not `./img/`

---

## Quick Reference

### Local Development
```powershell
cd book
npm start
```

### Build Locally
```powershell
cd book
npm run build
npm run serve
```

### Deploy Manually
```powershell
cd book
npm run deploy
```

---

## Your Configuration Summary

Update these in `book/docusaurus.config.ts`:

```typescript
url: 'https://YOUR_USERNAME.github.io',
baseUrl: '/YOUR_REPO_NAME/',
organizationName: 'YOUR_USERNAME',
projectName: 'YOUR_REPO_NAME',
```

---

## 🎉 Success!

Once deployed, your site will have:
- ✅ Modern blue and white UI
- ✅ Redesigned homepage
- ✅ Beautiful chat interface
- ✅ Clean navbar and footer
- ✅ Professional auth forms
- ✅ Responsive design

**Your URL**: `https://YOUR_USERNAME.github.io/robotics/`

---

## Need Help?

- GitHub Pages Docs: https://docs.github.com/pages
- Docusaurus Deployment: https://docusaurus.io/docs/deployment
- GitHub Actions: https://docs.github.com/actions

---

**Happy Deploying! 🚀**
