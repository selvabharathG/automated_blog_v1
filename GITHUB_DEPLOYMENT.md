# 🚀 GitHub Deployment Guide

Your automated blog agent is **fully tested and ready for GitHub deployment**!

## Prerequisites
- GitHub account (free)
- Git installed on your machine
- Groq API key (already in your `.env`)

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface
1. Go to https://github.com/new
2. **Repository name**: `automated-research-blog` (or your choice)
3. **Description**: "Automated daily research blog using AI"
4. **Visibility**: Public (for GitHub Pages)
5. Click **Create repository**

### Option B: Using Git CLI
```bash
cd c:\Users\Selvabharath\Documents\Selva\15_AI\1_Projects\1_Automated_Blog

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Automated research blog agent"

# Set your GitHub repo URL
git remote add origin https://github.com/YOUR_USERNAME/automated-research-blog.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 2: Add GitHub Secrets

GitHub Actions needs your Groq API key to run the workflow.

1. **Go to Your Repository Settings**
   - Navigate to: `https://github.com/YOUR_USERNAME/automated-research-blog/settings`

2. **Add Secret**
   - Left sidebar → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - **Name**: `GROQ_API_KEY`
   - **Value**: Copy your API key from `.env` (starts with `gsk_`)
   - Click **Add secret**

### Verify Secret is Set
```
✅ Secrets stored securely (cannot be viewed after creation)
✅ Workflow file will access via: ${{ secrets.GROQ_API_KEY }}
```

---

## Step 3: Enable GitHub Pages

GitHub Pages will host your blog publicly.

1. **Go to Repository Settings**
   - Navigate to: `https://github.com/YOUR_USERNAME/automated-research-blog/settings`

2. **Configure Pages**
   - Left sidebar → **Pages**
   - **Source**: "Deploy from a branch"
   - **Branch**: Select `main`
   - **Folder**: Select `/blog`
   - Click **Save**

3. **Verify Deployment**
   - Wait 1-2 minutes
   - Your blog will be live at: `https://YOUR_USERNAME.github.io/automated-research-blog/`

---

## Step 4: Verify GitHub Actions Workflow

The workflow is already configured in `.github/workflows/publish-blog.yml`

1. **View Workflow Status**
   - Go to: `https://github.com/YOUR_USERNAME/automated-research-blog/actions`

2. **Manual Trigger** (to test immediately)
   - Click on **publish-blog** workflow
   - Click **Run workflow** → **Run workflow**
   - Wait 30-60 seconds
   - Check logs to verify success

3. **Check Generated Posts**
   - After workflow completes, go to:
   - `https://github.com/YOUR_USERNAME/automated-research-blog/tree/main/blog/posts`
   - New `.md` files should appear here

---

## Step 5: Verify Daily Scheduling

The workflow runs automatically daily at **8 AM SGT** (12 AM UTC).

**Workflow Configuration** (`.github/workflows/publish-blog.yml`):
```yaml
schedule:
  - cron: '0 0 * * *'  # 12 AM UTC = 8 AM SGT
```

### How to Verify
1. **View Workflow Runs**
   - Go to: **Actions** tab in your GitHub repo
   - Check **publish-blog** workflow
   - Should show daily runs at scheduled time

2. **View Generated Posts**
   - Check `blog/posts/` directory
   - New files appear with format: `YYYY-MM-DD_*.md`

3. **View Blog Online**
   - Visit: `https://YOUR_USERNAME.github.io/automated-research-blog/blog/`
   - Should show your blog posts

---

## Step 6: Monitor & Troubleshoot

### View Latest Logs
1. Go to **Actions** tab
2. Click on latest **publish-blog** run
3. Expand **Run research agent** step
4. View full output

### Common Issues & Solutions

#### Issue: Workflow fails with "GROQ_API_KEY not found"
- **Solution**: 
  1. Verify secret is added in Settings → Secrets
  2. Secret name must be exactly `GROQ_API_KEY`
  3. Re-run workflow after adding secret

#### Issue: Blog not appearing on GitHub Pages
- **Solution**:
  1. Verify GitHub Pages enabled in Settings → Pages
  2. Source should be `main` branch, `/blog` folder
  3. Wait 1-2 minutes for initial deployment

#### Issue: Posts not generating
- **Solution**:
  1. Check workflow logs for errors
  2. Verify Groq API key is valid (test locally first)
  3. Check if Groq API has changed models (run `python` model list check)

---

## Step 7: Customize Your Blog

### Edit Blog Configuration
1. Edit `config/blog_config.yaml`:
   - Change blog title, description
   - Adjust topic weights
   - Modify scheduling time

2. Commit and push changes:
   ```bash
   git add config/blog_config.yaml
   git commit -m "Update blog configuration"
   git push
   ```

### Customize Blog Appearance
- Blog templates are in `blog/` directory
- CSS files in `blog/style.css`
- Modify to match your brand

---

## Step 8: Share Your Blog

Once live, share your blog:

### Social Media Template
```
🚀 I just launched my automated AI blog!
Generated daily using AI research & insights.
Every day at 8 AM SGT, new posts about tech trends.

Check it out: https://YOUR_USERNAME.github.io/automated-research-blog/

#AI #Blog #Automation #GitHub
```

### LinkedIn Post
```
Excited to share my automated research blog! 🤖
Built with Python, Groq LLM, and GitHub Actions
- Daily AI-generated posts
- Topics: AI/ML, Web Dev, Cloud, DevOps, Data Science
- Published automatically at 8 AM SGT
- Deployed to GitHub Pages

Live blog: [link]
GitHub repo: [link]
```

---

## Monitoring Checklist

- [ ] GitHub repo created and code pushed
- [ ] `GROQ_API_KEY` secret added to GitHub
- [ ] GitHub Pages enabled (using `/blog` folder)
- [ ] Manual workflow run successful
- [ ] First blog post generated and visible
- [ ] GitHub Pages URL shows blog correctly
- [ ] Scheduled workflow set for 8 AM SGT

---

## Support & Troubleshooting

### View Real-Time Logs
```bash
# SSH into a workflow run and debug
# Not recommended - use GitHub UI instead
```

### Test Locally Before Deploying
```bash
python main.py
# Check logs/app.log for any issues
# View generated post in blog/posts/
```

### Get Help
1. Check [Groq API Documentation](https://console.groq.com/docs)
2. Review [GitHub Actions Documentation](https://docs.github.com/en/actions)
3. Check [GitHub Pages Documentation](https://docs.github.com/en/pages)

---

## Final Notes

✅ **Your blog is ready to go live!**

- All dependencies installed ✅
- Configuration validated ✅
- Blog posts generating successfully ✅
- Logging system working ✅
- Error handling in place ✅
- GitHub Actions workflow ready ✅

**Next**: Push to GitHub and watch your daily blog grow! 🚀

---

Generated: 2026-06-17
