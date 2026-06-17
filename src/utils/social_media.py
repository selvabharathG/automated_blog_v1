"""
Module: Social Media Publisher
Purpose: Handle automatic sharing to social platforms
Author: Research Team
"""

from typing import Dict, Any, Optional
from src.utils.logger import get_logger
from src.utils.config_manager import config

logger = get_logger(__name__)

class SocialMediaPublisher:
    """Publish blog posts to social media platforms"""
    
    def __init__(self):
        self.twitter_enabled = config.get_env("TWITTER_API_KEY") is not None
        self.linkedin_enabled = config.get_env("LINKEDIN_API_KEY") is not None
    
    def publish(self, post_metadata: Dict[str, Any], post_url: str) -> Dict[str, bool]:
        """
        Publish to enabled social platforms
        
        Args:
            post_metadata: Post title, description, tags
            post_url: URL to published blog post
        
        Returns:
            Status for each platform
        """
        results = {}
        
        if self.twitter_enabled:
            results["twitter"] = self._publish_twitter(post_metadata, post_url)
        
        if self.linkedin_enabled:
            results["linkedin"] = self._publish_linkedin(post_metadata, post_url)
        
        return results
    
    def _publish_twitter(self, metadata: Dict[str, Any], url: str) -> bool:
        """Publish to Twitter/X"""
        try:
            title = metadata.get("title", "New Blog Post")
            tags = metadata.get("tags", [])
            hashtags = " ".join([f"#{tag}" for tag in tags[:3]])
            
            # Tweet template
            tweet = f"📝 {title}\n\n{url}\n\n{hashtags}"
            
            # Truncate if needed (280 characters)
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            # TODO: Implement actual Twitter API call
            # from tweepy import Client
            # client = Client(...)
            # client.create_tweet(text=tweet)
            
            logger.info(f"Tweet (simulated): {tweet}")
            return True
        
        except Exception as e:
            logger.error(f"Twitter publish failed: {e}")
            return False
    
    def _publish_linkedin(self, metadata: Dict[str, Any], url: str) -> bool:
        """Publish to LinkedIn"""
        try:
            title = metadata.get("title", "New Blog Post")
            description = metadata.get("meta_description", "")
            
            post = f"{title}\n\n{description}\n\n{url}"
            
            # TODO: Implement actual LinkedIn API call
            
            logger.info(f"LinkedIn post (simulated): {post}")
            return True
        
        except Exception as e:
            logger.error(f"LinkedIn publish failed: {e}")
            return False
    
    @staticmethod
    def generate_social_snippet(title: str, description: str, url: str, platform: str = "twitter") -> str:
        """
        Generate platform-specific social media post
        
        Args:
            title: Post title
            description: Post description/excerpt
            url: Post URL
            platform: Social platform (twitter, linkedin, etc.)
        
        Returns:
            Formatted social media post
        """
        if platform == "twitter":
            # 280 character limit
            snippet = f"📝 {title}\n\n{description}\n\n{url}"
            return snippet[:280]
        
        elif platform == "linkedin":
            # More formal, longer format
            snippet = f"**{title}**\n\n{description}\n\nRead full article: {url}"
            return snippet
        
        else:
            return f"{title} - {url}"

def publish_to_social(metadata: Dict[str, Any], url: str) -> Dict[str, bool]:
    """Convenience function"""
    publisher = SocialMediaPublisher()
    return publisher.publish(metadata, url)
