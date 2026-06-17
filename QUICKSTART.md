# ⚡ QUICK START GUIDE

## 🎯 Get Started in 5 Minutes

### Step 1: Get Groq API Key (2 minutes)
```
1. Visit https://console.groq.com
2. Sign up (free)
3. Go to API Keys
4. Copy your API key
```

### Step 2: Setup Local Environment (2 minutes)
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Groq key
# GROQ_API_KEY=sk_live_xxxxx
```

### Step 3: Install & Test (1 minute)
```bash
# Install dependencies
pip install -r requirements.txt

# Run blog generation
python main.py

# Check output
cat blog/posts/*.md
```

---

## 🚀 Deploy to GitHub (5 minutes)

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Name: `automated-blog`
3. Description: "Daily AI/ML blog with LLMs"
4. Click "Create repository"

### Step 2: Push Code
```bash
git init
git add .
git commit -m "Initial commit: Automated blog setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/automated-blog.git
git push -u origin main
```

### Step 3: Add GitHub Secrets
1. Go to GitHub repo
2. Settings → Secrets and variables → Actions
3. New repository secret:
   - Name: `GROQ_API_KEY`
   - Value: Your API key from Step 1
4. (Optional) Add `TWITTER_API_KEY` for social sharing

### Step 4: Enable GitHub Pages
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, folder: `/blog` or root
4. Save

### Step 5: Enable GitHub Actions
1. Actions → I understand my workflows, go ahead and run them
2. Your blog will auto-generate daily at 8 AM SGT!

---

## 📋 Customization (Optional)

### Change Blog Topics
Edit `config/blog_config.yaml`:
```yaml
topics:
  - name: "Your Topic"
    weight: 0.25
```

### Change Publishing Time
Edit `.github/workflows/publish-blog.yml`:
```yaml
- cron: '0 8 * * *'  # 8 AM UTC (change to your timezone)
```

### Enable Social Media Sharing
Add Twitter API keys to `.env`:
```
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
```

---

## 📊 Monitor Your Blog

### View Logs Locally
```bash
tail -f logs/app.log
```

### Monitor GitHub Actions
1. Go to GitHub repo
2. Click "Actions" tab
3. See daily runs at 8 AM SGT

### View Published Posts
- Local: `blog/posts/` directory
- GitHub Pages: `https://your-username.github.io/automated-blog`

---

## 🆘 Troubleshooting

### Blog not generating?
```bash
# Check API key
echo $GROQ_API_KEY

# Test locally
python main.py

# Check logs
tail -f logs/app.log
```

### GitHub Actions not running?
1. Check .github/workflows/publish-blog.yml syntax
2. Verify GROQ_API_KEY secret exists
3. Check Actions permissions in Settings

### Posts not publishing?
1. Check workflow logs in Actions tab
2. Verify `blog/` directory exists
3. Verify git config in workflow

---

## 📖 Full Documentation

- **Complete guide**: See [README.md](README.md)
- **Dev standards**: See [copilot-instructions.md](copilot-instructions.md)
- **Config reference**: See [config/](config/) directory

---

## 🎓 Learn More

- [Groq API Docs](https://console.groq.com/docs)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [GitHub Pages Setup](https://pages.github.com)

---

**Ready to launch? Start with Step 1 above! 🚀**
