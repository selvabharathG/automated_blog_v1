"""
Module: SEO Optimizer
Purpose: Optimize blog posts for search engines
Author: Research Team
"""

import re
from typing import Dict, List, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SEOOptimizer:
    """Optimize blog content for SEO"""
    
    def __init__(self):
        self.min_word_count = 1200
        self.max_word_count = 2000
        self.min_headings = 3
    
    def analyze(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze SEO metrics of blog post
        
        Args:
            content: Blog post markdown content
            metadata: Post metadata (title, description, tags)
        
        Returns:
            SEO analysis report
        """
        
        word_count = len(content.split())
        headings = self._count_headings(content)
        readability_score = self._calculate_readability(content)
        keyword_density = self._analyze_keywords(content, metadata.get("tags", []))
        
        score = self._calculate_seo_score(
            word_count,
            len(headings),
            readability_score,
            keyword_density
        )
        
        return {
            "word_count": word_count,
            "headings": len(headings),
            "readability_score": readability_score,
            "keyword_density": keyword_density,
            "seo_score": score,
            "issues": self._identify_issues(word_count, len(headings), readability_score)
        }
    
    def optimize_title(self, title: str, keywords: List[str]) -> str:
        """Optimize title for SEO"""
        # Add keyword if not present and has space
        if keywords and keywords[0] not in title.lower():
            title = f"{title} - {keywords[0].title()}"
        return title[:60]
    
    def generate_meta(self, title: str, content: str, keywords: List[str]) -> str:
        """Generate meta description"""
        # Extract first sentence
        sentences = re.split(r'[.!?]', content)
        first_sentence = sentences[0].strip()[:160]
        
        # Add keyword if space allows
        if keywords and keywords[0] not in first_sentence.lower():
            first_sentence = f"{keywords[0].title()} - {first_sentence}"[:160]
        
        return first_sentence
    
    @staticmethod
    def _count_headings(content: str) -> List[str]:
        """Extract headings from markdown"""
        return re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    
    @staticmethod
    def _calculate_readability(content: str) -> float:
        """Estimate Flesch reading ease score"""
        # Simplified calculation
        words = len(content.split())
        sentences = len(re.split(r'[.!?]', content))
        syllables = len(re.findall(r'[aeiouy]', content.lower())) + 1
        
        if sentences == 0 or words == 0:
            return 50
        
        score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
        return max(0, min(100, score))
    
    @staticmethod
    def _analyze_keywords(content: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density"""
        density = {}
        word_count = len(content.split())
        
        for keyword in keywords:
            count = len(re.findall(rf'\b{keyword}\b', content, re.IGNORECASE))
            density[keyword] = (count / word_count * 100) if word_count > 0 else 0
        
        return density
    
    @staticmethod
    def _calculate_seo_score(word_count: int, headings: int, readability: float, keywords: Dict[str, float]) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 0
        
        # Word count (30 points)
        if 1200 <= word_count <= 2000:
            score += 30
        elif 900 <= word_count <= 2500:
            score += 20
        elif word_count >= 500:
            score += 10
        
        # Headings (20 points)
        if headings >= 5:
            score += 20
        elif headings >= 3:
            score += 15
        elif headings >= 1:
            score += 10
        
        # Readability (20 points)
        if 60 <= readability <= 100:
            score += 20
        elif 40 <= readability < 60:
            score += 15
        elif readability >= 30:
            score += 10
        
        # Keywords (30 points)
        if keywords:
            score += 30
        
        return min(100, score)
    
    @staticmethod
    def _identify_issues(word_count: int, headings: int, readability: float) -> List[str]:
        """Identify SEO issues"""
        issues = []
        
        if word_count < 1200:
            issues.append(f"Content too short: {word_count} words (min: 1200)")
        elif word_count > 2000:
            issues.append(f"Content too long: {word_count} words (max: 2000)")
        
        if headings < 3:
            issues.append(f"Too few headings: {headings} (recommended: 3+)")
        
        if readability < 40:
            issues.append("Content may be too complex for general audience")
        
        return issues

def optimize_post(content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function"""
    optimizer = SEOOptimizer()
    return {
        "analysis": optimizer.analyze(content, metadata),
        "optimized_title": optimizer.optimize_title(metadata.get("title", ""), metadata.get("tags", [])),
        "meta_description": optimizer.generate_meta(metadata.get("title", ""), content, metadata.get("tags", []))
    }
