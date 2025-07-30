"""
LLM Provider interface for Nüm Agents SDK.

This module provides a unified interface for interacting with different LLM providers
such as OpenAI, Google (Gemini), Anthropic, etc.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    This class defines the interface that all LLM providers must implement.
    """
    
    def __init__(
        self, 
        model: str,
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1000
    ):
        """
        Initialize the LLM provider.
        
        Args:
            model: Model name to use
            api_key: API key for the provider (default: None, will use environment variable)
            temperature: Temperature for generation (default: 0.1)
            max_tokens: Maximum number of tokens to generate (default: 1000)
        """
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated text
        """
        pass
        
    @abstractmethod
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Generate JSON from a prompt.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated JSON as a dictionary
        """
        pass


class OpenAIProvider(LLMProvider):
    """
    LLM provider for OpenAI models (GPT-4, etc.).
    """
    
    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1000
    ):
        """
        Initialize the OpenAI provider.
        
        Args:
            model: Model name to use (default: "gpt-4o")
            api_key: API key for OpenAI (default: None, will use OPENAI_API_KEY environment variable)
            temperature: Temperature for generation (default: 0.1)
            max_tokens: Maximum number of tokens to generate (default: 1000)
        """
        super().__init__(model, api_key, temperature, max_tokens)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            self.logger.warning("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or pass api_key.")
        
    def generate(self, prompt: str) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated text
        """
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except ImportError:
            self.logger.error("OpenAI package not installed. Install with 'pip install openai'")
            return ""
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {e}")
            return ""
            
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Generate JSON using OpenAI API.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated JSON as a dictionary
        """
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except ImportError:
            self.logger.error("OpenAI package not installed. Install with 'pip install openai'")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Error parsing JSON from OpenAI response")
            return {}
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {e}")
            return {}


class GeminiProvider(LLMProvider):
    """
    LLM provider for Google Gemini models.
    """
    
    def __init__(
        self,
        model: str = "gemini-pro",
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1000
    ):
        """
        Initialize the Gemini provider.
        
        Args:
            model: Model name to use (default: "gemini-pro")
            api_key: API key for Google AI (default: None, will use GOOGLE_API_KEY environment variable)
            temperature: Temperature for generation (default: 0.1)
            max_tokens: Maximum number of tokens to generate (default: 1000)
        """
        super().__init__(model, api_key, temperature, max_tokens)
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            self.logger.warning("No Google API key provided. Set GOOGLE_API_KEY environment variable or pass api_key.")
        
    def generate(self, prompt: str) -> str:
        """
        Generate text using Google Gemini API.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated text
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens
                }
            )
            
            response = model.generate_content(prompt)
            return response.text
        except ImportError:
            self.logger.error("Google Generative AI package not installed. Install with 'pip install google-generativeai'")
            return ""
        except Exception as e:
            self.logger.error(f"Error calling Gemini API: {e}")
            return ""
            
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Generate JSON using Google Gemini API.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated JSON as a dictionary
        """
        # Add explicit instructions for JSON output
        json_prompt = f"{prompt}\n\nPlease respond with valid JSON only, no other text."
        
        try:
            response_text = self.generate(json_prompt)
            
            # Try to extract JSON if there's surrounding text
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Try to find JSON-like content in the response
                import re
                json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                else:
                    self.logger.error(f"Could not extract JSON from Gemini response")
                    return {}
        except Exception as e:
            self.logger.error(f"Error generating JSON with Gemini: {e}")
            return {}


class AnthropicProvider(LLMProvider):
    """
    LLM provider for Anthropic models (Claude, etc.).
    """
    
    def __init__(
        self,
        model: str = "claude-3-opus-20240229",
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1000
    ):
        """
        Initialize the Anthropic provider.
        
        Args:
            model: Model name to use (default: "claude-3-opus-20240229")
            api_key: API key for Anthropic (default: None, will use ANTHROPIC_API_KEY environment variable)
            temperature: Temperature for generation (default: 0.1)
            max_tokens: Maximum number of tokens to generate (default: 1000)
        """
        super().__init__(model, api_key, temperature, max_tokens)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            self.logger.warning("No Anthropic API key provided. Set ANTHROPIC_API_KEY environment variable or pass api_key.")
        
    def generate(self, prompt: str) -> str:
        """
        Generate text using Anthropic API.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated text
        """
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )
            return response.content[0].text
        except ImportError:
            self.logger.error("Anthropic package not installed. Install with 'pip install anthropic'")
            return ""
        except Exception as e:
            self.logger.error(f"Error calling Anthropic API: {e}")
            return ""
            
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Generate JSON using Anthropic API.
        
        Args:
            prompt: Prompt to generate from
            
        Returns:
            Generated JSON as a dictionary
        """
        # Add explicit instructions for JSON output
        json_prompt = f"{prompt}\n\nPlease respond with valid JSON only, no other text."
        
        try:
            response_text = self.generate(json_prompt)
            
            # Try to extract JSON if there's surrounding text
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Try to find JSON-like content in the response
                import re
                json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                else:
                    self.logger.error(f"Could not extract JSON from Anthropic response")
                    return {}
        except Exception as e:
            self.logger.error(f"Error generating JSON with Anthropic: {e}")
            return {}


class LLMProviderFactory:
    """
    Factory for creating LLM providers.
    """
    
    @staticmethod
    def create_provider(
        provider_name: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1000
    ) -> LLMProvider:
        """
        Create an LLM provider.
        
        Args:
            provider_name: Name of the provider (openai, gemini, anthropic)
            model: Model name to use (default: None, will use provider's default)
            api_key: API key for the provider (default: None, will use environment variable)
            temperature: Temperature for generation (default: 0.1)
            max_tokens: Maximum number of tokens to generate (default: 1000)
            
        Returns:
            LLM provider instance
            
        Raises:
            ValueError: If provider_name is not supported
        """
        provider_name = provider_name.lower()
        
        if provider_name == "openai":
            return OpenAIProvider(
                model=model or "gpt-4o",
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif provider_name == "gemini":
            return GeminiProvider(
                model=model or "gemini-pro",
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif provider_name == "anthropic":
            return AnthropicProvider(
                model=model or "claude-3-opus-20240229",
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")
