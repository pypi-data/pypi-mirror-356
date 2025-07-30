"""HTTP client for making requests to NHL APIs."""

import httpx
from typing import Dict, Any, Optional


class HttpClient:
    """Base HTTP client for NHL API requests."""
    
    def __init__(self, user_agent: str = "EdgeworkClient/0.2.1"):
        """
        Initialize the HTTP client.
        
        Args:
            user_agent: User agent string for requests
        """
        self._user_agent = user_agent
        self._base_url = "https://api-web.nhle.com/v1/"
        self._stats_base_url = "https://api.nhle.com/stats/rest/en/"
        
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, web: bool = False) -> httpx.Response:
        """
        Make a GET request to an NHL API endpoint.
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Optional query parameters
            web: If True, use the web API base URL
            
        Returns:
            httpx.Response object
        """
        if web:
            url = f"{self._base_url}{endpoint}"
        else:
            url = f"{self._stats_base_url}{endpoint}"
            
        headers = {"User-Agent": self._user_agent}
        
        with httpx.Client() as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
    
    def get_raw(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        Make a GET request to a raw URL.
        
        Args:
            url: Full URL to request
            params: Optional query parameters
            
        Returns:
            httpx.Response object
        """
        headers = {"User-Agent": self._user_agent}
        
        with httpx.Client() as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response


class SyncHttpClient(HttpClient):
    """Synchronous HTTP client - alias for backward compatibility."""
    pass
