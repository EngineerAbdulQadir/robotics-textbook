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

## Deploying Backends to Railway.app

### Why Railway.app?
- ✅ Free tier available (500 hours/month)
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ Built-in PostgreSQL database
- ✅ Environment variables management

---

### Step 1: Deploy Auth Backend

#### 1.1 Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway to access your repositories

#### 1.2 Create New Project for Auth Backend
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `robotics-textbook`
4. Railway will detect your project

#### 1.3 Configure Auth Backend Service
1. Click **"Add Service"** → **"GitHub Repo"**
2. Select `robotics-textbook` repository
3. Configure:
   - **Service Name**: `auth-backend`
   - **Root Directory**: `auth-backend`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Watch Paths**: `auth-backend/**`

#### 1.4 Add PostgreSQL Database
1. In your Railway project, click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will automatically create a database
3. Copy the **DATABASE_URL** from the PostgreSQL service

#### 1.5 Add Environment Variables
Click on `auth-backend` service → **"Variables"** → Add these:

```env
DATABASE_URL=<copy from PostgreSQL service>
BETTER_AUTH_SECRET=your_secret_key_here
FRONTEND_URL=https://YOUR_USERNAME.github.io
NODE_ENV=production
PORT=3001

# Optional: OAuth credentials
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

#### 1.6 Deploy
1. Click **"Deploy"**
2. Wait for deployment to complete (2-3 minutes)
3. Copy your backend URL: `https://auth-backend-production-xxxx.up.railway.app`

---

### Step 2: Deploy Chatbot Backend

#### 2.1 Add Chatbot Service to Same Project
1. In the same Railway project, click **"New"** → **"GitHub Repo"**
2. Select `robotics-textbook` repository again
3. Configure:
   - **Service Name**: `chatbot-backend`
   - **Root Directory**: `chatbot-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Watch Paths**: `chatbot-backend/**`

#### 2.2 Add Environment Variables for Chatbot
Click on `chatbot-backend` service → **"Variables"** → Add these:

```env
DATABASE_URL=<same PostgreSQL URL from auth-backend>
GEMINI_API_KEY=your_gemini_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_url
NEON_API_KEY=your_neon_api_key
FRONTEND_URL=https://YOUR_USERNAME.github.io
PORT=8000
```

#### 2.3 Deploy
1. Click **"Deploy"**
2. Wait for deployment to complete
3. Copy your chatbot backend URL: `https://chatbot-backend-production-xxxx.up.railway.app`

---

### Step 3: Update Frontend with Backend URLs

Update `book/src/components/PersonalizeButton/PersonalizeButton.tsx`:

```typescript
const getApiUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  return window.location.hostname === 'localhost'
    ? 'http://localhost:3001'
    : 'https://auth-backend-production-xxxx.up.railway.app'; // Your Railway auth backend URL
};
```

Update `book/src/components/AuthModal.tsx` with the same URL.

For chatbot integration, update the chatbot API URL similarly.

---

### Step 4: Enable CORS on Backends

Make sure your backends allow requests from your GitHub Pages domain.

**In `auth-backend/src/index.ts`**, verify CORS is configured:
```typescript
app.use(cors({
  origin: [
    'http://localhost:3000',
    'https://YOUR_USERNAME.github.io'
  ],
  credentials: true
}));
```

**In `chatbot-backend/src/main.py`**, verify CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://YOUR_USERNAME.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Step 5: Push Changes and Redeploy

```powershell
git add .
git commit -m "Update backend URLs for Railway deployment"
git push
```

Railway will automatically redeploy when you push changes!

---

### Railway Dashboard Overview

Your Railway project will have:
- 🗄️ **PostgreSQL** - Shared database for both backends
- 🔐 **auth-backend** - Authentication service
- 🤖 **chatbot-backend** - RAG chatbot service

Each service will have its own URL and environment variables.

---

### Monitoring and Logs

1. Click on any service in Railway
2. Go to **"Deployments"** tab to see build logs
3. Go to **"Metrics"** to monitor usage
4. Check **"Logs"** for runtime errors

---

### Cost Management

Railway free tier includes:
- ✅ 500 execution hours/month
- ✅ Shared CPU and RAM
- ✅ Automatic SSL certificates
- ✅ Custom domains (optional)

If you exceed free tier, Railway will notify you.

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
