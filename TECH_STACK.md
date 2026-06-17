# Technology Stack & Architecture

## 🏗️ Complete Tech Stack

### Backend & Processing
- **Language**: Python 3.10+
- **Runtime**: CPython
- **Async**: aiohttp (for concurrent requests)

### LLM Integration (Primary)
- **Provider**: Groq
- **Model**: Mixtral 8x7B (32K context)
- **Cost**: FREE
- **Rate Limit**: 60 requests/minute, 5000/day
- **Response Time**: <100ms

### LLM Integration (Fallback)
- **Provider**: Anthropic Claude
- **Model**: Claude 3 Haiku (fastest)
- **Cost**: FREE (trial credits)
- **Status**: Optional

### Local LLM (Optional)
- **Provider**: Ollama
- **Models**: neural-chat, mistral, llama2
- **Cost**: FREE (runs locally)
- **Status**: Optional fallback

### Web Scraping & APIs
- **HTTP**: requests, aiohttp
- **HTML Parsing**: BeautifulSoup4
- **Feed Parsing**: feedparser
- **Social APIs**: tweepy (Twitter/X)

### Configuration Management
- **Config Format**: YAML (PyYAML)
- **Environment**: python-dotenv
- **Type Safety**: Type hints (Python 3.10+)

### Logging & Monitoring
- **Library**: loguru (production-grade)
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Output**: Console + File (async)
- **Rotation**: 500MB or daily
- **Retention**: 30 days app.log, 90 days errors.log

### Scheduling & Deployment
- **Scheduler**: GitHub Actions
- **Cron**: 0 0 * * * (8 AM SGT = 12 AM UTC)
- **Cost**: FREE (2000 min/month included)
- **Runtime**: ubuntu-latest

### Hosting & Storage
- **Static Hosting**: GitHub Pages
- **Cost**: FREE
- **Build**: None (markdown → static)
- **CDN**: GitHub's global CDN

### Version Control
- **VCS**: Git
- **Platform**: GitHub
- **Cost**: FREE (public repo)
- **Features**: Actions, Pages, Secrets

### Database (Optional)
- **Type**: SQLite (local file-based)
- **Cost**: FREE
- **Use**: Post metadata cache (optional)

### SEO Optimization
- **Keyword Analysis**: Custom Python implementation
- **Readability**: Flesch reading ease scoring
- **Meta Generation**: LLM-powered
- **Schema**: JSON-LD (optional)

### Testing
- **Framework**: pytest
- **Coverage**: pytest-cov
- **Linting**: flake8
- **Formatting**: black
- **Type Checking**: mypy

---

## 📊 Cost Breakdown

| Component | Service | Cost | Why Free |
|-----------|---------|------|----------|
| LLM API | Groq | $0 | Free tier available |
| Scheduling | GitHub Actions | $0 | 2000 min/month free |
| Hosting | GitHub Pages | $0 | Free service |
| Storage | GitHub | $0 | Included with repo |
| Version Control | GitHub | $0 | Free for public repos |
| Local LLM | Ollama | $0 | Open source |
| Logging | loguru | $0 | Open source |
| **TOTAL** | | **$0** | All free tier ✅ |

---

## 🚀 Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│           GitHub Actions (Scheduler)                │
│      Triggers daily at 8 AM SGT (0:00 UTC)          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              main.py (Entry Point)                  │
│  ┌─────────────────────────────────────────────┐   │
│  │ 1. Initialize Logger (loguru)               │   │
│  │ 2. Load Config (YAML + .env)                │   │
│  │ 3. Validate Environment                     │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          ResearchAgent Pipeline                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ Topic Selection (weighted random)           │   │
│  │ → Research Data Gathering                   │   │
│  │ → LLM Analysis (Groq API)                   │   │
│  │ → Blog Post Generation (LLM)                │   │
│  │ → Metadata Generation (SEO)                 │   │
│  │ → Markdown Compilation                      │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          Publishing Pipeline                       │
│  ┌─────────────────────────────────────────────┐   │
│  │ Save to blog/posts/*.md                     │   │
│  │ Git commit & push                           │   │
│  │ (Optional) Social media share               │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│    GitHub Pages Auto-Deployment                    │
│    Live blog: https://username.github.io/blog      │
└─────────────────────────────────────────────────────┘
```

---

## 💾 Data Flow

```
Input Sources
└─ Research Data (simulated/scraped)
   └─ LLM Analysis (Groq API)
      └─ Blog Content Generation
         └─ SEO Optimization
            └─ Markdown with Frontmatter
               └─ Git Commit
                  └─ GitHub Push
                     └─ GitHub Pages Build
                        └─ Live Blog Post
                           └─ Social Media Share (optional)
```

---

## 🔒 Security Features

- **API Keys**: Stored in .env (git ignored)
- **GitHub Secrets**: Safe credential storage
- **HTTPS**: GitHub Pages auto-HTTPS
- **Type Safety**: Python type hints
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Audit trail of all operations

---

## ⚡ Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| LLM Response Time | <100ms | Groq optimized |
| Blog Generation Time | ~30-60s | Depends on LLM |
| Total Pipeline | ~1-2 min | API + processing |
| GitHub Actions Run | ~3-5 min | Including checkout, setup |
| Post Publish Delay | ~1 min | Git push + Pages build |

---

## 🎯 Scalability

- **Posts per day**: 1 (scheduled)
- **Max posts generated**: Limited by API rate limits (60/min)
- **Storage capacity**: GitHub allows 100GB free
- **Concurrent runs**: 1 (GitHub Actions default)
- **Upgrade path**: Can scale to multiple topics/languages later

---

## 🔧 Maintenance

### Dependencies
```bash
# Check outdated packages
pip list --outdated

# Update
pip install --upgrade package_name
```

### Configuration
- Monthly: Review topic weights and sources
- Quarterly: Update LLM prompts based on quality feedback
- Annually: Audit entire technology stack

### Monitoring
- Check logs daily initially
- Set GitHub email notifications
- Monitor SEO metrics (optional)

---

## 📚 References

- [Python 3.10 Release](https://www.python.org/downloads/release/python-3100/)
- [Groq LLM Models](https://console.groq.com/docs/models)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Guide](https://pages.github.com)
- [loguru Documentation](https://loguru.readthedocs.io)
- [PyYAML Documentation](https://pyyaml.org)

---

## 🚀 Why This Stack?

1. **Free**: All components have free/open-source options
2. **Modern**: Latest Python (3.10+), async-first where needed
3. **Scalable**: Can grow from 1 post/day to thousands
4. **Maintainable**: Clear architecture, type hints, logging
5. **Reliable**: GitHub Actions + stable APIs
6. **Fast**: Groq LLM with <100ms response time
7. **Flexible**: Easy to swap LLM providers or add platforms

---

**Last Updated**: 2024-01-XX | Version: 1.0.0
