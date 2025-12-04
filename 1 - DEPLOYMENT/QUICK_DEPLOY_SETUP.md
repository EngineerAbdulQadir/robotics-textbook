# 🚀 Quick Deployment Setup

## Step-by-Step Instructions

### 1. Update Your Configuration (5 minutes)

Open `book/docusaurus.config.ts` and change these lines:

**Current (someone else's):**
```typescript
url: 'https://92Bilal26.github.io',
organizationName: '92Bilal26',
projectName: 'physical-ai-textbook',
```

**Change to YOUR details:**
```typescript
url: 'https://YOUR_GITHUB_USERNAME.github.io',
organizationName: 'YOUR_GITHUB_USERNAME',
projectName: 'YOUR_REPO_NAME',
```

**Example (if your GitHub username is "AQI"):**
```typescript
url: 'https://AQI.github.io',
organizationName: 'AQI',
projectName: 'robotics-textbook',
```

---

### 2. Create GitHub Repository (2 minutes)

1. Go to: https://github.com/new
2. Repository name: `robotics-textbook` (or your choice)
3. Make it **Public**
4. **Don't** check "Add README"
5. Click **"Create repository"**

---

### 3. Push Your Code (3 minutes)

Open PowerShell in your project folder and run:

```powershell
# Navigate to project
cd C:\Users\AQI\OneDrive\Desktop\HACKATHON\physical-ai-textbook-main

# Check if git is initialized
git status

# If not initialized, run:
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Redesigned robotics textbook"

# Add your repository (REPLACE WITH YOUR URL!)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Or if remote already exists, update it:
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

---

### 4. Enable GitHub Pages (1 minute)

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Source: Select **"GitHub Actions"**
5. That's it! No need to save, it's automatic

---

### 5. Wait for Deployment (2-5 minutes)

1. Go to your repository
2. Click **Actions** tab (top)
3. You'll see "Deploy to GitHub Pages" running
4. Wait for green checkmark ✅

---

### 6. Access Your Site! 🎉

Your site will be live at:

```
https://YOUR_USERNAME.github.io/robotics/
```

Example:
```
https://AQI.github.io/robotics/
```

---

## Quick Commands Reference

### Test Build Locally First
```powershell
cd book
npm install
npm run build
npm run serve
```

Then open: http://localhost:3000/robotics/

### Update and Redeploy
```powershell
git add .
git commit -m "Update content"
git push
```

GitHub Actions will automatically rebuild and deploy!

---

## Troubleshooting

### "Repository not found"
- Check you're using YOUR GitHub username
- Check repository name matches

### "Permission denied"
- You may need to authenticate with GitHub
- Use GitHub Desktop or set up SSH keys

### Build fails
```powershell
cd book
npm install
npm run build
```
Fix any errors shown

### 404 on deployed site
- Check `baseUrl` in config matches `/robotics/`
- Wait 5 minutes for DNS propagation
- Try clearing browser cache

---

## What You're Deploying

✅ **Modern UI** - Blue and white theme
✅ **Redesigned Homepage** - Hero, features, navbar, footer
✅ **Chat Interface** - Beautiful, composed design
✅ **Auth Forms** - Modern sign-in/sign-up
✅ **Responsive** - Works on all devices

---

## Need the Full Guide?

See `DEPLOYMENT_GUIDE.md` for:
- Deploying auth backend
- Custom domains
- Advanced configuration
- Troubleshooting details

---

## Summary Checklist

- [ ] Update `docusaurus.config.ts` with YOUR details
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Enable GitHub Pages (Actions)
- [ ] Wait for deployment
- [ ] Visit your site!

---

**Time needed: ~15 minutes total**

**Your site URL**: `https://YOUR_USERNAME.github.io/robotics/`

🚀 **Happy Deploying!**
