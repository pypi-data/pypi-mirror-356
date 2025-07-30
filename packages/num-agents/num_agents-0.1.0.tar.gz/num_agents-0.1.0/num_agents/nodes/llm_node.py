"""
LLM Node for the Nüm Agents SDK.

This module provides a specialized node for interacting with Large Language Models (LLMs)
from different providers such as OpenAI, Anthropic, etc.
"""

import json
import logging
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from num_agents.core import Node, SharedStore


class LLMProvider(Enum):
    """Enum for different LLM providers."""
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"


class LLMNode(Node):
    """
    A specialized node for interacting with Large Language Models.
    
    This node provides a standardized interface for prompting LLMs from
    different providers and handling their responses.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        provider: Union[str, LLMProvider] = LLMProvider.OPENAI,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
        input_key: str = "llm_input",
        output_key: str = "llm_output",
        **kwargs
    ) -> None:
        """
        Initialize an LLM node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            provider: The LLM provider to use (e.g., "openai", "anthropic")
            model: The specific model to use (e.g., "gpt-4", "claude-3-opus")
            api_key: Optional API key for the provider
            temperature: The temperature parameter for the LLM
            max_tokens: The maximum number of tokens to generate
            system_prompt: An optional system prompt to use for all requests
            retry_attempts: The number of retry attempts for failed requests
            retry_delay: The delay between retry attempts in seconds
            input_key: The key in the shared store to use as input
            output_key: The key in the shared store to store the output
            **kwargs: Additional provider-specific parameters
        """
        super().__init__(name, shared_store)
        
        # Convert provider to enum if it's a string
        if isinstance(provider, str):
            try:
                self.provider = LLMProvider(provider.lower())
            except ValueError:
                self.provider = LLMProvider.CUSTOM
        else:
            self.provider = provider
        
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.input_key = input_key
        self.output_key = output_key
        self.additional_params = kwargs
        
        # Initialize the client
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """
        Initialize the appropriate client based on the provider.
        
        This method sets up the client for the specified LLM provider.
        """
        if self.provider == LLMProvider.OPENAI:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                logging.error("OpenAI package not installed. Please install it with 'pip install openai'.")
                raise
        
        elif self.provider == LLMProvider.ANTHROPIC:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logging.error("Anthropic package not installed. Please install it with 'pip install anthropic'.")
                raise
        
        elif self.provider == LLMProvider.COHERE:
            try:
                import cohere
                self.client = cohere.Client(api_key=self.api_key)
            except ImportError:
                logging.error("Cohere package not installed. Please install it with 'pip install cohere'.")
                raise
        
        elif self.provider == LLMProvider.HUGGINGFACE:
            try:
                from huggingface_hub import InferenceClient
                self.client = InferenceClient(token=self.api_key)
            except ImportError:
                logging.error("Hugging Face package not installed. Please install it with 'pip install huggingface_hub'.")
                raise
        
        elif self.provider == LLMProvider.CUSTOM:
            # For custom providers, the client should be set up in a subclass
            pass
    
    def _process(self) -> None:
        """
        Process the node's logic.
        
        This method retrieves the input from the shared store, sends it to the LLM,
        and stores the response in the shared store.
        """
        # Get input from the shared store
        input_text = self._get_input()
        
        if not input_text:
            logging.warning(f"No input found at key '{self.input_key}' in shared store.")
            return
        
        # Call the LLM
        response = self._call_llm(input_text)
        
        # Store the response in the shared store
        self._set_output(response)
    
    def _get_input(self) -> str:
        """
        Get the input text from the shared store.
        
        Returns:
            The input text to send to the LLM
        """
        # Check if the input key is an attribute of the shared store
        if hasattr(self.shared_store, self.input_key):
            return getattr(self.shared_store, self.input_key)
        
        # Check if the shared store has a data dictionary
        if hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            return self.shared_store.data.get(self.input_key, "")
        
        return ""
    
    def _set_output(self, output: str) -> None:
        """
        Set the output in the shared store.
        
        Args:
            output: The output text from the LLM
        """
        # Check if the output key is an attribute of the shared store
        if hasattr(self.shared_store, self.output_key):
            setattr(self.shared_store, self.output_key, output)
        
        # Check if the shared store has a data dictionary
        elif hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            self.shared_store.data[self.output_key] = output
    
    def _call_llm(self, input_text: str) -> str:
        """
        Call the LLM with the input text.
        
        This method handles the actual API call to the LLM provider,
        with retry logic for handling transient errors.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The response text from the LLM
        """
        for attempt in range(self.retry_attempts):
            try:
                if self.provider == LLMProvider.OPENAI:
                    return self._call_openai(input_text)
                
                elif self.provider == LLMProvider.ANTHROPIC:
                    return self._call_anthropic(input_text)
                
                elif self.provider == LLMProvider.COHERE:
                    return self._call_cohere(input_text)
                
                elif self.provider == LLMProvider.HUGGINGFACE:
                    return self._call_huggingface(input_text)
                
                elif self.provider == LLMProvider.CUSTOM:
                    return self._call_custom(input_text)
                
            except Exception as e:
                logging.error(f"Error calling LLM (attempt {attempt + 1}/{self.retry_attempts}): {str(e)}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
        
        # If all attempts fail, return an error message
        error_msg = f"Failed to call LLM after {self.retry_attempts} attempts."
        logging.error(error_msg)
        return f"ERROR: {error_msg}"
    
    def _call_openai(self, input_text: str) -> str:
        """
        Call the OpenAI API with the input text.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The response text from the LLM
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized.")
        
        messages = []
        
        # Add system prompt if provided
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        # Add user message
        messages.append({"role": "user", "content": input_text})
        
        # Prepare parameters
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        
        # Add max_tokens if provided
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens
        
        # Add any additional parameters
        params.update(self.additional_params)
        
        # Call the API
        response = self.client.chat.completions.create(**params)
        
        # Extract and return the response text
        return response.choices[0].message.content
    
    def _call_anthropic(self, input_text: str) -> str:
        """
        Call the Anthropic API with the input text.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The response text from the LLM
        """
        if not self.client:
            raise ValueError("Anthropic client not initialized.")
        
        # Prepare parameters
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens or 1024,
            "temperature": self.temperature,
        }
        
        # Add system prompt if provided
        if self.system_prompt:
            params["system"] = self.system_prompt
        
        # Add any additional parameters
        params.update(self.additional_params)
        
        # Call the API
        response = self.client.messages.create(
            **params,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        
        # Extract and return the response text
        return response.content[0].text
    
    def _call_cohere(self, input_text: str) -> str:
        """
        Call the Cohere API with the input text.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The response text from the LLM
        """
        if not self.client:
            raise ValueError("Cohere client not initialized.")
        
        # Prepare parameters
        params = {
            "model": self.model,
            "temperature": self.temperature,
        }
        
        # Add max_tokens if provided
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens
        
        # Add any additional parameters
        params.update(self.additional_params)
        
        # Call the API
        response = self.client.generate(
            prompt=input_text,
            **params
        )
        
        # Extract and return the response text
        return response.generations[0].text
    
    def _call_huggingface(self, input_text: str) -> str:
        """
        Call the Hugging Face API with the input text.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The response text from the LLM
        """
        if not self.client:
            raise ValueError("Hugging Face client not initialized.")
        
        # Prepare parameters
        params = {
            "temperature": self.temperature,
        }
        
        # Add max_tokens if provided
        if self.max_tokens:
            params["max_length"] = self.max_tokens
        
        # Add any additional parameters
        params.update(self.additional_params)
        
        # Call the API
        response = self.client.text_generation(
            prompt=input_text,
            model=self.model,
            **params
        )
        
        # Return the response text
        return response
    
    def _call_custom(self, input_text: str) -> str:
        """
        Call a custom LLM provider with the input text.
        
        This method should be overridden in a subclass for custom providers.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The response text from the LLM
        """
        raise NotImplementedError("Custom LLM provider not implemented. Please override this method in a subclass.")


class StreamingLLMNode(LLMNode):
    """
    A specialized LLM node that supports streaming responses.
    
    This node extends the base LLMNode to add support for streaming responses
    from LLMs that support it, such as OpenAI and Anthropic.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        provider: Union[str, LLMProvider] = LLMProvider.OPENAI,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
        input_key: str = "llm_input",
        output_key: str = "llm_output",
        stream_callback: Optional[callable] = None,
        **kwargs
    ) -> None:
        """
        Initialize a streaming LLM node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            provider: The LLM provider to use (e.g., "openai", "anthropic")
            model: The specific model to use (e.g., "gpt-4", "claude-3-opus")
            api_key: Optional API key for the provider
            temperature: The temperature parameter for the LLM
            max_tokens: The maximum number of tokens to generate
            system_prompt: An optional system prompt to use for all requests
            retry_attempts: The number of retry attempts for failed requests
            retry_delay: The delay between retry attempts in seconds
            input_key: The key in the shared store to use as input
            output_key: The key in the shared store to store the output
            stream_callback: A callback function to call with each chunk of the streaming response
            **kwargs: Additional provider-specific parameters
        """
        super().__init__(
            name,
            shared_store,
            provider,
            model,
            api_key,
            temperature,
            max_tokens,
            system_prompt,
            retry_attempts,
            retry_delay,
            input_key,
            output_key,
            **kwargs
        )
        self.stream_callback = stream_callback
    
    def _call_openai(self, input_text: str) -> str:
        """
        Call the OpenAI API with the input text, using streaming if a callback is provided.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The complete response text from the LLM
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized.")
        
        messages = []
        
        # Add system prompt if provided
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        # Add user message
        messages.append({"role": "user", "content": input_text})
        
        # Prepare parameters
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": self.stream_callback is not None,
        }
        
        # Add max_tokens if provided
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens
        
        # Add any additional parameters
        params.update(self.additional_params)
        
        # Call the API
        response = self.client.chat.completions.create(**params)
        
        # Handle streaming response
        if self.stream_callback:
            full_response = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    self.stream_callback(content)
            return full_response
        else:
            # Extract and return the response text for non-streaming response
            return response.choices[0].message.content
    
    def _call_anthropic(self, input_text: str) -> str:
        """
        Call the Anthropic API with the input text, using streaming if a callback is provided.
        
        Args:
            input_text: The input text to send to the LLM
            
        Returns:
            The complete response text from the LLM
        """
        if not self.client:
            raise ValueError("Anthropic client not initialized.")
        
        # Prepare parameters
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens or 1024,
            "temperature": self.temperature,
            "stream": self.stream_callback is not None,
        }
        
        # Add system prompt if provided
        if self.system_prompt:
            params["system"] = self.system_prompt
        
        # Add any additional parameters
        params.update(self.additional_params)
        
        # Call the API
        response = self.client.messages.create(
            **params,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )
        
        # Handle streaming response
        if self.stream_callback:
            full_response = ""
            for chunk in response:
                if chunk.type == "content_block_delta" and chunk.delta.text:
                    content = chunk.delta.text
                    full_response += content
                    self.stream_callback(content)
            return full_response
        else:
            # Extract and return the response text for non-streaming response
            return response.content[0].text
