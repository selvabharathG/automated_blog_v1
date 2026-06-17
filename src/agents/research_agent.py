"""
Module: Research Agent
Purpose: Main agent for research, analysis, and blog post generation
Author: Research Team
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import quote
import time

from src.utils.logger import get_logger
from src.utils.config_manager import config
from src.utils.api_clients import get_llm_client

logger = get_logger(__name__)

class ResearchAgent:
    """Main research and content generation agent"""
    
    def __init__(self):
        self.config = config
        self.llm = get_llm_client()
        self.topic_weights = config.get_topic_weights()
        logger.info("ResearchAgent initialized")
    
    def run(self) -> Dict[str, Any]:
        """Execute full research and blog generation pipeline"""
        try:
            logger.info("Starting research and blog generation pipeline")
            
            # Step 1: Select topic
            topic = self.select_topic()
            logger.info(f"Selected topic: {topic}")
            
            # Step 2: Research content
            research_data = self.research_topic(topic)
            logger.info(f"Collected research data for {topic}")
            
            # Step 3: Analyze research
            analysis = self.analyze_research(research_data, topic)
            logger.info("Research analysis completed")
            
            # Step 4: Generate blog post
            blog_post = self.generate_blog_post(topic, analysis)
            logger.info("Blog post generated")
            
            # Step 5: Generate metadata (title, description)
            metadata = self.generate_metadata(blog_post, topic)
            logger.info("Metadata generated")
            
            # Step 6: Compile final post
            final_post = self.compile_post(blog_post, metadata, topic)
            
            logger.info("Research pipeline completed successfully")
            return {
                "success": True,
                "topic": topic,
                "title": metadata.get("title"),
                "post": final_post,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Research pipeline failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def select_topic(self) -> str:
        """Select random topic based on weights"""
        topics = self.config.get_all_topics()
        
        if not topics:
            raise ValueError("No topics configured")
        
        topic_names = [t["name"] for t in topics]
        weights = [self.topic_weights.get(t, 1.0) for t in topic_names]
        
        selected_topic = random.choices(topic_names, weights=weights, k=1)[0]
        return selected_topic
    
    def research_topic(self, topic: str) -> Dict[str, Any]:
        """Research topic from multiple sources (simulated)"""
        # In production, this would scrape multiple sources
        # For now, we'll use LLM to generate research data
        
        topic_config = None
        for t in self.config.get_all_topics():
            if t["name"] == topic:
                topic_config = t
                break
        
        if not topic_config:
            raise ValueError(f"Topic not found: {topic}")
        
        keywords = ", ".join(topic_config.get("keywords", []))
        sources = ", ".join(topic_config.get("sources", []))
        
        logger.debug(f"Researching {topic} with keywords: {keywords}")
        
        return {
            "topic": topic,
            "keywords": topic_config.get("keywords", []),
            "sources": topic_config.get("sources", []),
            "research_date": datetime.now().isoformat(),
            "key_findings": [
                f"Latest developments in {topic}",
                f"Emerging trends and patterns",
                f"Real-world applications and use cases",
                f"Industry best practices"
            ]
        }
    
    def analyze_research(self, research_data: Dict[str, Any], topic: str) -> str:
        """Analyze research data using LLM"""
        
        prompt = f"""
        Based on the following research data about {topic}, provide a comprehensive analysis:
        
        Topic: {research_data['topic']}
        Keywords: {', '.join(research_data['keywords'])}
        Key Findings:
        {chr(10).join(f"- {finding}" for finding in research_data['key_findings'])}
        
        Please provide:
        1. Summary of key insights
        2. Current trends and patterns
        3. Real-world applications
        4. Industry implications
        5. Future outlook
        
        Format the response as a coherent analysis suitable for technical audience.
        """
        
        try:
            analysis = self.llm.generate(
                prompt,
                temperature=0.7,
                max_tokens=1000
            )
            return analysis
        except Exception as e:
            logger.error(f"Failed to analyze research: {e}")
            raise
    
    def generate_blog_post(self, topic: str, analysis: str) -> str:
        """Generate complete blog post from analysis"""
        
        audience_level = "Intermediate"
        word_count = self.config.get("blog.content.post_length.words_target", 1500)
        
        prompt = f"""
        Write a compelling blog post for {audience_level} developers about: {topic}
        
        Base the post on this research analysis:
        {analysis}
        
        Requirements:
        - Target word count: {word_count} words
        - Structure: Introduction → Key Concepts → Examples → Real-World Use Cases → Conclusion
        - Include practical examples and code snippets where relevant
        - Easy to understand and coherent
        - Professional tone but accessible
        - Include action items or takeaways
        
        Format as Markdown with:
        - Clear headers (##, ###)
        - Code blocks for examples
        - Bullet points for lists
        - Emphasis on important concepts
        
        Start with the content directly (no title, that comes separately).
        """
        
        try:
            blog_post = self.llm.generate(
                prompt,
                temperature=0.7,
                max_tokens=2000
            )
            return blog_post
        except Exception as e:
            logger.error(f"Failed to generate blog post: {e}")
            raise
    
    def generate_metadata(self, post: str, topic: str) -> Dict[str, str]:
        """Generate SEO metadata for the post"""
        
        # Truncate post for title/meta generation
        post_preview = post[:500]
        
        title_prompt = f"""
        Generate 3 SEO-friendly blog post titles for this {topic} post:
        
        Preview: {post_preview}
        
        Requirements:
        - Include main keyword naturally
        - 50-60 characters
        - Compelling and specific
        - Action-oriented when possible
        
        Return ONLY a JSON array: ["title1", "title2", "title3"]
        """
        
        meta_prompt = f"""
        Generate an SEO-friendly meta description (150-160 characters) for:
        
        Topic: {topic}
        Post preview: {post_preview}
        
        Requirements:
        - Include main keyword
        - Compelling
        - Exactly 150-160 characters
        
        Return ONLY the meta description text, nothing else.
        """
        
        try:
            # Generate titles
            titles_response = self.llm.generate(title_prompt, temperature=0.6, max_tokens=200)
            try:
                titles = json.loads(titles_response)
                title = titles[0] if titles else f"Exploring {topic}"
            except:
                title = f"Comprehensive Guide to {topic}"
            
            # Generate meta
            meta_description = self.llm.generate(meta_prompt, temperature=0.6, max_tokens=160)
            meta_description = meta_description[:160].strip()
            
            # Generate slug
            slug = self._generate_slug(title)
            
            # Generate tags
            tags = [topic] + [kw.split()[0] for kw in topic.split() if len(kw) > 3][:3]
            
            return {
                "title": title,
                "meta_description": meta_description,
                "slug": slug,
                "tags": tags,
                "topic": topic,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        
        except Exception as e:
            logger.error(f"Failed to generate metadata: {e}")
            return {
                "title": f"Comprehensive Guide to {topic}",
                "meta_description": f"Learn about {topic} - latest trends, best practices, and real-world examples.",
                "slug": self._generate_slug(topic),
                "tags": [topic],
                "topic": topic,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
    
    def compile_post(self, blog_post: str, metadata: Dict[str, str], topic: str) -> str:
        """Compile final markdown post with frontmatter"""
        
        frontmatter = f"""---
title: "{metadata['title']}"
description: "{metadata['meta_description']}"
date: {metadata['date']}
author: "Research Agent"
tags: {metadata['tags']}
topic: "{topic}"
slug: {metadata['slug']}
---

"""
        
        return frontmatter + blog_post
    
    @staticmethod
    def _generate_slug(text: str) -> str:
        """Generate URL-friendly slug from text"""
        slug = text.lower()
        slug = slug.replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        slug = "-".join(filter(None, slug.split("-")))
        return slug[:50]  # Limit to 50 chars

def run_research_agent() -> Dict[str, Any]:
    """Convenience function to run the research agent"""
    agent = ResearchAgent()
    return agent.run()
