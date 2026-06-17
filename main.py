#!/usr/bin/env python3
"""
Main Entry Point: Automated Research Blog Agent
Purpose: Orchestrate research, blog generation, and publishing
Author: Research Team
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logger import Logger, get_logger
from src.utils.config_manager import ConfigManager, config
from src.agents.research_agent import run_research_agent
from src.utils.api_clients import get_llm_client

logger = get_logger(__name__)

def initialize_environment() -> bool:
    """Initialize application environment"""
    try:
        # Setup logging
        log_level = os.getenv("LOG_LEVEL", "INFO")
        Logger.setup(log_level=log_level)
        logger.info("=" * 60)
        logger.info("AUTOMATED RESEARCH BLOG AGENT")
        logger.info("=" * 60)
        
        # Validate configuration
        if not config.validate_config():
            logger.error("Configuration validation failed")
            return False
        
        logger.info("Environment initialized successfully")
        return True
    
    except Exception as e:
        logger.error(f"Environment initialization failed: {e}", exc_info=True)
        return False

def publish_blog_post(result: Dict[str, Any]) -> bool:
    """Publish generated blog post to platforms"""
    try:
        if not result.get("success"):
            logger.error("Cannot publish failed blog generation")
            return False
        
        # Save to blog directory
        blog_dir = Path("blog/posts")
        blog_dir.mkdir(parents=True, exist_ok=True)
        
        metadata = result.get("metadata", {})
        slug = metadata.get("slug", "blog-post")
        date = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        filename = f"{date}_{slug}.md"
        filepath = blog_dir / filename
        
        # Write post
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result["post"])
        
        logger.info(f"Blog post published: {filepath}")
        
        # Optional: Share on social media
        if config.is_feature_enabled("social_media"):
            share_social_media(result)
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to publish blog post: {e}", exc_info=True)
        return False

def share_social_media(result: Dict[str, Any]) -> bool:
    """Share blog post on social media (optional)"""
    try:
        if not config.get_env("TWITTER_API_KEY"):
            logger.info("Twitter API not configured, skipping social share")
            return False
        
        metadata = result.get("metadata", {})
        title = metadata.get("title", "New Blog Post")
        slug = metadata.get("slug", "blog")
        
        blog_url = config.get("blog.url", "https://username.github.io/blog")
        post_url = f"{blog_url}/posts/{slug}"
        
        # Tweet template
        hashtags = ", ".join(config.get("social_media.platforms.twitter.hashtags", []))
        tweet = f"🚀 New post: {title}\n\n{post_url}\n\n{hashtags}"
        
        # Optional: Actually post (requires tweepy setup)
        logger.info(f"Social share template: {tweet}")
        
        return True
    
    except Exception as e:
        logger.warning(f"Social media sharing failed: {e}")
        return False

def generate_index() -> bool:
    """Generate blog index page"""
    try:
        blog_dir = Path("blog/posts")
        posts = sorted(blog_dir.glob("*.md"), reverse=True)
        
        if not posts:
            logger.warning("No blog posts found")
            return False
        
        # Create index
        index_content = "# Blog Posts\n\n"
        for post in posts:
            # Extract title from frontmatter
            with open(post, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple extraction (in production, use proper YAML parsing)
                title = post.stem.replace("_", " ").title()
                index_content += f"- [{title}](posts/{post.name})\n"
        
        index_path = Path("blog/index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        
        logger.info("Blog index updated")
        return True
    
    except Exception as e:
        logger.warning(f"Failed to generate index: {e}")
        return False

def main() -> int:
    """Main execution function"""
    try:
        # Initialize
        if not initialize_environment():
            logger.error("Failed to initialize environment")
            return 1
        
        # Validate LLM availability
        try:
            llm = get_llm_client()
            logger.info(f"LLM client ready: {llm.__class__.__name__}")
        except Exception as e:
            logger.error(f"No LLM client available: {e}")
            return 1
        
        # Run research and blog generation
        logger.info("Starting research agent...")
        result = run_research_agent()
        
        if not result.get("success"):
            logger.error(f"Research agent failed: {result.get('error')}")
            return 1
        
        logger.info(f"Research completed for topic: {result.get('topic')}")
        logger.info(f"Generated title: {result.get('title')}")
        
        # Publish blog post
        logger.info("Publishing blog post...")
        if not publish_blog_post(result):
            logger.error("Failed to publish blog post")
            return 1
        
        # Update index
        generate_index()
        
        logger.info("=" * 60)
        logger.info("✅ BLOG POST GENERATION COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        return 0
    
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        return 1
    
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
