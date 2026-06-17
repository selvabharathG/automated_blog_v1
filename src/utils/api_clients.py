"""
Module: API Clients
Purpose: Unified interface for LLM API calls (Groq, Claude, Ollama)
Author: Research Team
"""

import time
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import os

from src.utils.logger import get_logger
from src.utils.config_manager import config

logger = get_logger(__name__)

class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate content from prompt"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if API is available"""
        pass

class GroqClient(LLMClient):
    """Groq API Client (Free tier, 60 requests/minute)"""
    
    # Fallback models to try if primary fails (currently available models)
    FALLBACK_MODELS = [
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b",
        "groq/compound"
    ]
    
    def __init__(self):
        try:
            from groq import Groq
            self.client = Groq(
                api_key=config.get_env("GROQ_API_KEY")
            )
            self.model = config.get("llm.groq.model", "mixtral-8x7b-32768")
            self.rate_limit = 60  # requests per minute
            self.last_request_time = 0
            self.available_model = None  # Will be set on first successful call
            logger.info(f"Groq client initialized with model: {self.model}")
        except ImportError:
            logger.error("Groq package not installed: pip install groq")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate content using Groq API with fallback models"""
        # If we've found a working model, use it
        if self.available_model:
            return self._generate_with_model(prompt, self.available_model, **kwargs)
        
        # Try primary model first
        models_to_try = [self.model] + self.FALLBACK_MODELS
        last_error = None
        
        for model in models_to_try:
            try:
                response = self._generate_with_model(prompt, model, **kwargs)
                self.available_model = model  # Cache working model
                if self.available_model != self.model:
                    logger.info(f"Using fallback model: {model}")
                return response
            except Exception as e:
                last_error = str(e)
                logger.debug(f"Model {model} failed: {e}")
                continue
        
        # All models failed
        logger.error(f"All Groq models failed. Last error: {last_error}")
        raise ValueError(f"No available Groq models. Last error: {last_error}")
    
    def _generate_with_model(self, prompt: str, model: str, **kwargs) -> str:
        """Generate content using specific model"""
        # Respect rate limits
        self._handle_rate_limit()
        
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 2000)
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful, expert content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=kwargs.get("top_p", 0.9)
        )
        
        self.last_request_time = time.time()
        return response.choices[0].message.content
    
    def _handle_rate_limit(self) -> None:
        """Enforce rate limiting"""
        min_interval = 60 / self.rate_limit  # seconds between requests
        elapsed = time.time() - self.last_request_time
        if elapsed < min_interval:
            sleep_time = min_interval - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
    
    def is_available(self) -> bool:
        """Check if Groq API is available"""
        try:
            api_key = config.get_env("GROQ_API_KEY")
            return api_key is not None and len(api_key) > 0
        except:
            return False

class ClaudeClient(LLMClient):
    """Anthropic Claude API Client"""
    
    def __init__(self):
        try:
            from anthropic import Anthropic
            self.client = Anthropic(
                api_key=config.get_env("ANTHROPIC_API_KEY")
            )
            self.model = "claude-3-haiku-20240307"
            logger.info(f"Claude client initialized with model: {self.model}")
        except ImportError:
            logger.error("Anthropic package not installed: pip install anthropic")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Claude client: {e}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate content using Claude API"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 2000),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Claude API is available"""
        try:
            api_key = config.get_env("ANTHROPIC_API_KEY")
            return api_key is not None and len(api_key) > 0
        except:
            return False

class OllamaClient(LLMClient):
    """Local Ollama API Client (Free, runs locally)"""
    
    def __init__(self):
        try:
            import requests
            self.requests = requests
            self.base_url = config.get("ollama.base_url", "http://localhost:11434")
            self.model = config.get("ollama.model", "neural-chat")
            
            # Test connection
            if not self._test_connection():
                raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}")
            
            logger.info(f"Ollama client initialized with model: {self.model}")
        
        except ImportError:
            logger.error("Requests package not installed: pip install requests")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {e}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate content using Ollama API"""
        try:
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": kwargs.get("temperature", 0.7)
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"]
        
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    def _test_connection(self) -> bool:
        """Test connection to Ollama server"""
        try:
            response = self.requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        return self._test_connection()

class LLMClientFactory:
    """Factory for creating appropriate LLM client"""
    
    _clients: Dict[str, LLMClient] = {}
    
    @staticmethod
    def create(provider: Optional[str] = None) -> LLMClient:
        """
        Create LLM client based on configuration.
        
        Args:
            provider: Specific provider to use (groq, claude, ollama)
                     If None, uses primary from config with fallback
        
        Returns:
            Initialized LLM client
        
        Raises:
            ValueError: If no working client can be created
        """
        providers_to_try = []
        
        if provider:
            providers_to_try.append(provider)
        else:
            # Use primary + fallback from config
            primary = config.get("llm.primary", "groq")
            fallback = config.get("llm.fallback", "ollama")
            providers_to_try = [primary, fallback]
        
        for prov in providers_to_try:
            try:
                if prov not in LLMClientFactory._clients:
                    logger.debug(f"Attempting to create {prov} client")
                    
                    if prov == "groq":
                        client = GroqClient()
                    elif prov == "claude":
                        client = ClaudeClient()
                    elif prov == "ollama":
                        client = OllamaClient()
                    else:
                        logger.warning(f"Unknown LLM provider: {prov}")
                        continue
                    
                    if client.is_available():
                        LLMClientFactory._clients[prov] = client
                        logger.info(f"Successfully created {prov} client")
                        return client
                    else:
                        logger.warning(f"{prov} client not available")
                else:
                    return LLMClientFactory._clients[prov]
            
            except Exception as e:
                logger.warning(f"Failed to create {prov} client: {e}")
                continue
        
        raise ValueError("No working LLM client available")

def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """Convenience function to get LLM client"""
    return LLMClientFactory.create(provider)
