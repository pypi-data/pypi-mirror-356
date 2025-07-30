"""
API Node for the Nüm Agents SDK.

This module provides a specialized node for making API calls to external services,
with support for different HTTP methods, authentication, and error handling.
"""

import json
import logging
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from num_agents.core import Node, SharedStore


class HTTPMethod(Enum):
    """Enum for different HTTP methods."""
    
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AuthType(Enum):
    """Enum for different authentication types."""
    
    NONE = "none"
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"


class APINode(Node):
    """
    A specialized node for making API calls to external services.
    
    This node provides a standardized interface for making HTTP requests
    to external APIs, with support for different authentication methods,
    request formats, and error handling.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        base_url: str,
        endpoint: str = "",
        method: Union[str, HTTPMethod] = HTTPMethod.GET,
        auth_type: Union[str, AuthType] = AuthType.NONE,
        auth_credentials: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data_key: Optional[str] = None,
        response_key: str = "api_response",
        timeout: float = 30.0,
        retry_attempts: int = 3,
        retry_backoff_factor: float = 0.5,
        retry_status_forcelist: Optional[List[int]] = None,
        verify_ssl: bool = True,
        parse_json: bool = True,
        **kwargs
    ) -> None:
        """
        Initialize an API node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            base_url: The base URL for the API
            endpoint: The specific endpoint to call (will be appended to base_url)
            method: The HTTP method to use for the request
            auth_type: The type of authentication to use
            auth_credentials: Credentials for authentication (format depends on auth_type)
            headers: Optional headers to include in the request
            params: Optional query parameters to include in the request
            data_key: Optional key in the shared store to use as request data
            response_key: The key in the shared store to store the response
            timeout: The timeout for the request in seconds
            retry_attempts: The number of retry attempts for failed requests
            retry_backoff_factor: The backoff factor for retries
            retry_status_forcelist: List of HTTP status codes to retry on
            verify_ssl: Whether to verify SSL certificates
            parse_json: Whether to parse the response as JSON
            **kwargs: Additional parameters to pass to the requests library
        """
        super().__init__(name, shared_store)
        
        self.base_url = base_url
        self.endpoint = endpoint
        
        # Convert method to enum if it's a string
        if isinstance(method, str):
            try:
                self.method = HTTPMethod(method.upper())
            except ValueError:
                raise ValueError(f"Invalid HTTP method: {method}")
        else:
            self.method = method
        
        # Convert auth_type to enum if it's a string
        if isinstance(auth_type, str):
            try:
                self.auth_type = AuthType(auth_type.lower())
            except ValueError:
                raise ValueError(f"Invalid authentication type: {auth_type}")
        else:
            self.auth_type = auth_type
        
        self.auth_credentials = auth_credentials or {}
        self.headers = headers or {}
        self.params = params or {}
        self.data_key = data_key
        self.response_key = response_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_backoff_factor = retry_backoff_factor
        self.retry_status_forcelist = retry_status_forcelist or [429, 500, 502, 503, 504]
        self.verify_ssl = verify_ssl
        self.parse_json = parse_json
        self.additional_params = kwargs
        
        # Set up a session with retry logic
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry logic.
        
        Returns:
            A configured requests session
        """
        session = requests.Session()
        
        # Configure retry logic
        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=self.retry_backoff_factor,
            status_forcelist=self.retry_status_forcelist,
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set verify SSL
        session.verify = self.verify_ssl
        
        return session
    
    def _get_full_url(self) -> str:
        """
        Get the full URL for the API call.
        
        Returns:
            The full URL for the API call
        """
        if not self.endpoint:
            return self.base_url
        
        # Ensure there's exactly one slash between base_url and endpoint
        base_url = self.base_url.rstrip("/")
        endpoint = self.endpoint.lstrip("/")
        
        return f"{base_url}/{endpoint}"
    
    def _get_request_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the request data from the shared store.
        
        Returns:
            The request data, or None if no data is found
        """
        if not self.data_key:
            return None
        
        # Check if the data key is an attribute of the shared store
        if hasattr(self.shared_store, self.data_key):
            data = getattr(self.shared_store, self.data_key)
            return data if isinstance(data, dict) else {"data": data}
        
        # Check if the shared store has a data dictionary
        if hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            if self.data_key in self.shared_store.data:
                data = self.shared_store.data[self.data_key]
                return data if isinstance(data, dict) else {"data": data}
        
        return None
    
    def _set_response(self, response: Any) -> None:
        """
        Set the response in the shared store.
        
        Args:
            response: The response from the API call
        """
        # Check if the response key is an attribute of the shared store
        if hasattr(self.shared_store, self.response_key):
            setattr(self.shared_store, self.response_key, response)
        
        # Check if the shared store has a data dictionary
        elif hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            self.shared_store.data[self.response_key] = response
    
    def _prepare_auth(self) -> Optional[Any]:
        """
        Prepare the authentication for the request.
        
        Returns:
            The authentication object for the request, or None if no authentication is needed
        """
        if self.auth_type == AuthType.NONE:
            return None
        
        elif self.auth_type == AuthType.BASIC:
            username = self.auth_credentials.get("username", "")
            password = self.auth_credentials.get("password", "")
            return requests.auth.HTTPBasicAuth(username, password)
        
        elif self.auth_type == AuthType.BEARER:
            token = self.auth_credentials.get("token", "")
            self.headers["Authorization"] = f"Bearer {token}"
            return None
        
        elif self.auth_type == AuthType.API_KEY:
            key = self.auth_credentials.get("key", "")
            key_name = self.auth_credentials.get("key_name", "api_key")
            key_in = self.auth_credentials.get("key_in", "header")
            
            if key_in == "header":
                self.headers[key_name] = key
            elif key_in == "query":
                self.params[key_name] = key
            
            return None
        
        elif self.auth_type == AuthType.OAUTH2:
            token = self.auth_credentials.get("token", "")
            self.headers["Authorization"] = f"Bearer {token}"
            return None
        
        elif self.auth_type == AuthType.CUSTOM:
            # For custom auth, the auth should be handled in a subclass
            return None
        
        return None
    
    def _process(self) -> None:
        """
        Process the node's logic.
        
        This method makes the API call and stores the response in the shared store.
        """
        try:
            # Make the API call
            response = self._make_api_call()
            
            # Store the response in the shared store
            self._set_response(response)
        
        except Exception as e:
            logging.error(f"Error making API call: {str(e)}")
            # Store the error in the shared store
            self._set_response({"error": str(e)})
    
    def _make_api_call(self) -> Any:
        """
        Make the API call.
        
        Returns:
            The response from the API call
        """
        # Get the full URL
        url = self._get_full_url()
        
        # Get the request data
        data = self._get_request_data()
        
        # Prepare authentication
        auth = self._prepare_auth()
        
        # Prepare the request parameters
        request_params = {
            "url": url,
            "headers": self.headers,
            "params": self.params,
            "timeout": self.timeout,
            "auth": auth,
            **self.additional_params
        }
        
        # Add data if available
        if data:
            if self.method in [HTTPMethod.GET, HTTPMethod.HEAD, HTTPMethod.OPTIONS]:
                # For GET, HEAD, and OPTIONS, add data as params
                request_params["params"].update(data)
            else:
                # For other methods, add data as JSON
                request_params["json"] = data
        
        # Make the request
        response = self.session.request(self.method.value, **request_params)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the response
        if self.parse_json:
            try:
                return response.json()
            except json.JSONDecodeError:
                # If the response is not valid JSON, return the text
                return response.text
        else:
            return response.text


class WebhookNode(APINode):
    """
    A specialized API node for handling webhooks.
    
    This node extends the base APINode to add support for webhook-specific
    functionality, such as signature verification and event handling.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        webhook_url: str,
        webhook_secret: Optional[str] = None,
        event_type_key: str = "event_type",
        payload_key: str = "webhook_payload",
        response_key: str = "webhook_response",
        **kwargs
    ) -> None:
        """
        Initialize a webhook node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            webhook_url: The URL to send the webhook to
            webhook_secret: Optional secret for signing the webhook payload
            event_type_key: The key in the shared store for the event type
            payload_key: The key in the shared store for the webhook payload
            response_key: The key in the shared store to store the response
            **kwargs: Additional parameters to pass to the APINode
        """
        super().__init__(
            name,
            shared_store,
            base_url=webhook_url,
            method=HTTPMethod.POST,
            data_key=payload_key,
            response_key=response_key,
            **kwargs
        )
        self.webhook_secret = webhook_secret
        self.event_type_key = event_type_key
    
    def _get_request_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the webhook payload from the shared store.
        
        This method extends the base method to add the event type to the payload.
        
        Returns:
            The webhook payload, or None if no payload is found
        """
        # Get the base payload
        payload = super()._get_request_data() or {}
        
        # Add the event type if available
        event_type = None
        
        # Check if the event type key is an attribute of the shared store
        if hasattr(self.shared_store, self.event_type_key):
            event_type = getattr(self.shared_store, self.event_type_key)
        
        # Check if the shared store has a data dictionary
        elif hasattr(self.shared_store, "data") and isinstance(self.shared_store.data, dict):
            if self.event_type_key in self.shared_store.data:
                event_type = self.shared_store.data[self.event_type_key]
        
        # Add the event type to the payload
        if event_type:
            if isinstance(payload, dict):
                payload["event_type"] = event_type
            else:
                payload = {"event_type": event_type, "data": payload}
        
        # Sign the payload if a secret is provided
        if self.webhook_secret and isinstance(payload, dict):
            payload = self._sign_payload(payload)
        
        return payload
    
    def _sign_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign the webhook payload.
        
        This method adds a signature to the payload using the webhook secret.
        
        Args:
            payload: The webhook payload to sign
            
        Returns:
            The signed payload
        """
        import hashlib
        import hmac
        import time
        
        # Add a timestamp to the payload
        payload["timestamp"] = int(time.time())
        
        # Convert the payload to a JSON string
        payload_str = json.dumps(payload, sort_keys=True)
        
        # Calculate the signature
        signature = hmac.new(
            self.webhook_secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Add the signature to the payload
        payload["signature"] = signature
        
        return payload
