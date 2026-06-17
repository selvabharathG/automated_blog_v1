# Copilot Instructions - Automated Blog Research Agent

## Project Overview
Automated blog post generator that researches legitimate sources, drafts coherent blog posts with real-world examples, and publishes daily at 8 AM SGT using modern free tech stack.

---

## Project Structure Convention

```
1_Automated_Blog/
├── .github/
│   └── workflows/
│       └── publish-blog.yml          # GitHub Actions scheduling (8 AM SGT daily)
├── src/
│   ├── agents/
│   │   ├── research_agent.py         # Main research & content generation agent
│   │   └── publisher.py              # Publishing to platforms
│   ├── utils/
│   │   ├── logger.py                 # Industry-standard logging
│   │   ├── config_manager.py         # Configuration management
│   │   ├── api_clients.py            # LLM/API integrations
│   │   ├── seo_optimizer.py          # SEO optimization
│   │   └── social_media.py           # Social media sharing
├── blog/
│   ├── posts/                        # Generated markdown posts
│   ├── _config.yml                   # Jekyll/GitHub Pages config
│   └── index.md                      # Blog homepage
├── config/
│   ├── blog_config.yaml              # Blog topics, audience, sources
│   ├── llm_config.yaml               # LLM model configs
│   └── schedule_config.yaml          # Scheduling parameters
├── logs/
│   └── app.log                       # Centralized logging (gitignore)
├── tests/
│   ├── test_research_agent.py        # Unit tests
│   └── test_api_clients.py           # API integration tests
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
├── copilot-instructions.md           # This file
└── main.py                           # Entry point
```

---

## Dependency Tracking

### Version Management
- **Python**: 3.10+ (use `python --version`)
- **Package Management**: pip with `requirements.txt`
- **GitHub Actions Runtime**: ubuntu-latest (latest Python 3.11+)

### Core Dependencies
```
# requirements.txt structure
aiohttp==3.9.1              # Async HTTP client for web scraping
beautifulsoup4==4.12.2      # HTML parsing
requests==2.31.0            # HTTP library
python-dotenv==1.0.0        # Environment variables
pyyaml==6.0                 # Configuration files
groq==0.4.2                 # Groq LLM API (free)
anthropic==0.7.1            # Claude API (optional)
tweepy==4.14.0              # Twitter/X API
feedparser==6.0.10          # RSS feed parsing
python-dateutil==2.8.2      # Date/time utilities
pytz==2023.3                # Timezone handling
loguru==0.7.2               # Advanced logging

# Dev dependencies
pytest==7.4.2               # Testing framework
black==23.9.1               # Code formatting
flake8==6.0.0               # Linting
mypy==1.5.0                 # Type checking
```

### Dependency Update Strategy
- Run `pip list --outdated` monthly
- Use `pip-tools` for lock files in production
- Pin major versions, allow minor patches (e.g., `requests==2.31.*`)

---

## Industry-Standard Logging

### Logging Architecture
Uses **loguru** library for professional logging:

```python
# src/utils/logger.py
from loguru import logger
import sys
from datetime import datetime
import os

def setup_logger(log_level="INFO"):
    """Configure industry-standard logging"""
    
    # Remove default handler
    logger.remove()
    
    # File logging (daily rotation)
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logger.add(
        f"{log_dir}/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="500 MB",
        retention="30 days",
        level=log_level,
        enqueue=True  # Async logging for performance
    )
    
    # Console logging
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
        level=log_level
    )
    
    # Error file
    logger.add(
        f"{log_dir}/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        retention="90 days"
    )
    
    return logger

# Usage in modules
logger = setup_logger()
logger.info("Blog post generation started")
logger.warning("API rate limit approaching")
logger.error("Failed to fetch content", exc_info=True)
```

### Logging Standards
- **Format**: ISO 8601 timestamps, structured data
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Rotation**: 500 MB or daily
- **Retention**: 30 days for app.log, 90 days for errors.log
- **Performance**: Async queue (enqueue=True)

---

## Configuration Management

### Multi-Environment Configuration
Use YAML for human-readable configs + environment variables for secrets:

```yaml
# config/blog_config.yaml
blog:
  name: "AI & Tech Insights"
  description: "Daily blog on AI/ML, Web Dev, Cloud Architecture, DevOps, Data Science"
  author: "Research Agent"
  
topics:
  - name: "AI/ML"
    weight: 0.25
    sources:
      - arxiv
      - huggingface_blog
  - name: "Web Development"
    weight: 0.20
  - name: "Cloud Architecture"
    weight: 0.20
  - name: "DevOps"
    weight: 0.15
  - name: "Data Science"
    weight: 0.20

audience:
  levels: ["Beginners", "Intermediate", "Enterprise"]
  
content:
  post_length_words: 1500
  include_examples: true
  include_code_snippets: true
  include_real_world_cases: true
  seo_enabled: true
  
scheduling:
  timezone: "Asia/Singapore"
  publish_time: "08:00"
  publish_days: "MON-SUN"

platforms:
  github_pages:
    enabled: true
  medium:
    enabled: false
  hashnode:
    enabled: false
```

```yaml
# config/llm_config.yaml
llm:
  primary: "groq"  # Free, fast tier
  fallback: "local_ollama"
  
groq:
  model: "mixtral-8x7b-32768"
  temperature: 0.7
  max_tokens: 2000
  api_rate_limit: 60  # requests per minute
  
ollama:
  model: "neural-chat"
  temperature: 0.7
  base_url: "http://localhost:11434"
```

```python
# src/utils/config_manager.py
import yaml
import os
from typing import Dict, Any
from loguru import logger

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.blog_config = self._load_yaml("blog_config.yaml")
        self.llm_config = self._load_yaml("llm_config.yaml")
        self.env = self._load_env()
        logger.info("Configuration loaded successfully")
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        try:
            with open(os.path.join(self.config_dir, filename), 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file {filename} not found")
            raise
    
    def _load_env(self) -> Dict[str, str]:
        """Load environment variables from .env"""
        from dotenv import dotenv_values
        return dotenv_values(".env")
    
    def get(self, key: str, default=None):
        """Get config value with dot notation"""
        keys = key.split('.')
        value = self.blog_config if keys[0] == 'blog' else self.llm_config
        for k in keys[1:]:
            value = value.get(k, default)
        return value

# Usage
config = ConfigManager()
publish_time = config.get("blog.scheduling.publish_time")
llm_model = config.get("llm.groq.model")
api_key = config.env.get("GROQ_API_KEY")
```

### Environment Variables (.env)
```
# .env.example (commit to repo, users copy to .env)
# LLM APIs
GROQ_API_KEY=your_groq_key_here
ANTHROPIC_API_KEY=your_claude_key_here

# Social Media
TWITTER_API_KEY=your_twitter_key
TWITTER_API_SECRET=your_twitter_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret

# GitHub Pages
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your_username/your_repo

# Monitoring
LOG_LEVEL=INFO
DEBUG_MODE=false

# Database (optional)
DATABASE_URL=sqlite:///./blog.db
```

---

## README.md Maintenance

### README Structure (Keep Updated)

```markdown
# 🤖 Automated Research Blog Agent

> Daily AI/ML, Web Dev, Cloud Architecture blog posts at 8 AM SGT using free tier APIs

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- GitHub account (for Actions & Pages)
- Free API keys: Groq, (optional) Anthropic

### Installation

\`\`\`bash
git clone <repo-url>
cd 1_Automated_Blog

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys
\`\`\`

## 📋 Configuration

See [config/](config/) directory for YAML configs:
- `blog_config.yaml`: Topics, audience, publishing settings
- `llm_config.yaml`: LLM models & parameters

## 🏗️ Architecture

### Components
- **Research Agent** (`src/agents/research_agent.py`): Web scraping, content research
- **Publisher** (`src/agents/publisher.py`): Publishing to platforms
- **Utils**: Logging, config, API clients, SEO, social media
- **GitHub Actions**: Daily scheduling at 8 AM SGT

### Data Flow
1. **Schedule Trigger** → GitHub Actions (8 AM SGT)
2. **Research** → Scrape sources, fetch trending content
3. **Generate** → LLM (Groq/Ollama) creates blog post
4. **Optimize** → Add SEO, examples, real-world cases
5. **Publish** → GitHub Pages, Medium, Twitter
6. **Monitor** → Logging, error tracking

## 🔄 Workflow

### Manual Run
\`\`\`bash
python main.py
\`\`\`

### Automated Deployment
Push to main branch → GitHub Actions triggers automatically

### Logs
\`\`\`bash
tail -f logs/app.log
\`\`\`

## 📊 Features

- ✅ Multi-source research (arXiv, GitHub, news, docs)
- ✅ LLM-powered content generation (Groq/Claude/Ollama)
- ✅ SEO optimization
- ✅ Social media auto-sharing
- ✅ Daily scheduling (8 AM SGT)
- ✅ Structured logging & monitoring
- ✅ Free tier compatible (GitHub Actions, Groq, GitHub Pages)

## 🧪 Testing

\`\`\`bash
pytest tests/ -v
\`\`\`

## 📝 Contributing

## 📄 License

---

**Keep this updated with new features, breaking changes, and setup instructions.**
```

### README Best Practices
- Update whenever you add features or change setup
- Include quick start + full documentation
- Keep it under 500 lines (move details to wiki/docs)
- Add badges: build status, coverage, license, Python version

---

## Coding Standards & Conventions

### 1. File Naming
- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`

### 2. Code Structure
```python
# src/agents/research_agent.py

"""
Module: Research Agent
Purpose: Fetch and research content from multiple sources
Author: Research Team
Date: 2024-01-XX
"""

from typing import List, Dict, Any
from loguru import logger
from src.utils.config_manager import ConfigManager

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

class ResearchAgent:
    """Main research agent for content gathering"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = logger
    
    def research(self) -> Dict[str, Any]:
        """Execute research pipeline"""
        self.logger.info("Starting research phase")
        # Implementation...
```

### 3. Type Hints (Python 3.10+)
```python
def fetch_content(
    url: str,
    timeout: int = 30,
    retry: bool = True
) -> Dict[str, str]:
    """Fetch content with type hints"""
```

### 4. Docstrings (Google Style)
```python
def generate_post(topic: str, sources: List[str]) -> str:
    """Generate blog post from research data.
    
    Args:
        topic: Blog topic (e.g., "AI/ML")
        sources: List of source URLs
    
    Returns:
        Generated markdown blog post
    
    Raises:
        ValueError: If topic not found in config
        APIError: If LLM API fails
    
    Example:
        >>> post = generate_post("AI/ML", ["url1", "url2"])
        >>> len(post) > 1000
        True
    """
```

### 5. Error Handling
```python
try:
    response = api_client.fetch(url)
except APIError as e:
    logger.error(f"API call failed: {e}", exc_info=True)
    # Fallback logic
except Exception as e:
    logger.critical(f"Unexpected error: {e}", exc_info=True)
    raise
```

---

## Git & Version Control

### Branch Strategy
- `main`: Production code (protected branch)
- `develop`: Development (base for features)
- `feature/*`: Feature branches
- `hotfix/*`: Emergency fixes

### Commit Messages
```
feat: Add social media auto-sharing
fix: Resolve SEO optimization bug
docs: Update README with new features
refactor: Simplify research agent
test: Add unit tests for API clients
chore: Update dependencies
```

### Pre-commit Hooks
```bash
# Setup code quality checks
pip install pre-commit
pre-commit install

# Files: .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

---

## Maintenance Schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| Update dependencies | Monthly | DevOps |
| Review logs for errors | Weekly | Team |
| Update README | Per release | PM/Dev |
| Security audit | Quarterly | Security |
| Performance review | Monthly | DevOps |
| Backup configurations | Monthly | DevOps |

---

## Key References

- [Groq API Docs](https://console.groq.com) - Free LLM
- [GitHub Actions](https://docs.github.com/en/actions) - Scheduling
- [GitHub Pages](https://pages.github.com) - Static hosting
- [loguru](https://loguru.readthedocs.io) - Logging
- [Python Type Hints](https://peps.python.org/pep-0484/) - Type safety

---

**Last Updated**: 2024-01-XX | **Version**: 1.0.0
