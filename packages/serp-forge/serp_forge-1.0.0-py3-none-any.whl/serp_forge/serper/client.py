"""
Serper API client for Serp Forge.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional

import aiohttp
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import config
from ..utils.logging import get_logger
from .models import SearchResult

logger = get_logger(__name__)


class SerperAPIError(Exception):
    """Exception raised for Serper API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class SerperClient:
    """Client for interacting with Serper API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Serper client.
        
        Args:
            api_key: Serper API key. If not provided, uses config.
        """
        self.api_key = api_key if api_key is not None else config.serper.api_key
        self.base_url = config.serper.base_url
        self.timeout = config.serper.timeout
        self.max_requests_per_minute = config.serper.max_requests_per_minute
        
        # Rate limiting
        self.last_request_time = 0
        self.min_interval = 60.0 / self.max_requests_per_minute
        
        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        })
        
        logger.info(f"Initialized Serper client with rate limit: {self.max_requests_per_minute} req/min")
    
    @property
    def headers(self):
        return self.session.headers
    
    def _rate_limit(self) -> None:
        """Apply rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def search(self, query: str, search_type: str = "web", **kwargs) -> Dict[str, Any]:
        """Perform a search using Serper API.
        
        Args:
            query: Search query
            search_type: Type of search (web, news, images, videos)
            **kwargs: Additional search parameters
            
        Returns:
            Search results from Serper API
            
        Raises:
            SerperAPIError: If API request fails
        """
        self._rate_limit()
        
        # Prepare request payload
        payload = {
            "q": query,
            "type": search_type,
            **kwargs
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        logger.info(f"Searching for: {query} (type: {search_type})")
        
        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                error_msg = f"Serper API error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('message', 'Unknown error')}"
                except:
                    error_msg += f" - {response.text}"
                
                raise SerperAPIError(error_msg, response.status_code, response.json() if response.content else None)
            
            result = response.json()
            logger.info(f"Search completed: {query} - Found {len(result.get('organic', []))} results")
            
            return result
            
        except requests.exceptions.Timeout:
            raise SerperAPIError(f"Request timeout for query: {query}")
        except requests.exceptions.RequestException as e:
            raise SerperAPIError(f"Request failed for query {query}: {str(e)}")
        except json.JSONDecodeError as e:
            raise SerperAPIError(f"Invalid JSON response for query {query}: {str(e)}")
    
    def parse_search_results(self, response: Dict[str, Any]) -> List[SearchResult]:
        """Parse Serper API response into SearchResult objects.
        
        Args:
            response: Raw response from Serper API
            
        Returns:
            List of parsed SearchResult objects
        """
        results = []
        
        # Parse organic results
        organic_results = response.get("organic", [])
        for i, result in enumerate(organic_results):
            try:
                search_result = SearchResult(
                    title=result.get("title", ""),
                    url=result.get("link", ""),
                    snippet=result.get("snippet", ""),
                    position=i + 1,
                    source=result.get("displayLink", ""),
                    image_url=result.get("imageUrl"),
                    sitelinks=result.get("sitelinks"),
                    date=result.get("date")
                )
                results.append(search_result)
            except Exception as e:
                logger.warning(f"Failed to parse search result {i}: {e}")
                continue
        
        # Parse news results if present
        news_results = response.get("news", [])
        for i, result in enumerate(news_results):
            try:
                search_result = SearchResult(
                    title=result.get("title", ""),
                    url=result.get("link", ""),
                    snippet=result.get("snippet", ""),
                    position=len(results) + i + 1,
                    source=result.get("source", ""),
                    image_url=result.get("imageUrl"),
                    date=result.get("date")
                )
                results.append(search_result)
            except Exception as e:
                logger.warning(f"Failed to parse news result {i}: {e}")
                continue
        
        logger.info(f"Parsed {len(results)} search results")
        return results
    
    def close(self) -> None:
        """Close the client session."""
        if hasattr(self, 'session'):
            self.session.close()


class AsyncSerperClient:
    """Async client for interacting with Serper API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize async Serper client.
        
        Args:
            api_key: Serper API key. If not provided, uses config.
        """
        self.api_key = api_key or config.serper.api_key
        self.base_url = config.serper.base_url
        self.timeout = aiohttp.ClientTimeout(total=config.serper.timeout)
        self.max_requests_per_minute = config.serper.max_requests_per_minute
        
        # Rate limiting
        self.last_request_time = 0
        self.min_interval = 60.0 / self.max_requests_per_minute
        
        # Headers
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        
        logger.info(f"Initialized async Serper client with rate limit: {self.max_requests_per_minute} req/min")
    
    async def _rate_limit(self) -> None:
        """Apply rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def search(self, query: str, search_type: str = "web", **kwargs) -> Dict[str, Any]:
        """Perform an async search using Serper API.
        
        Args:
            query: Search query
            search_type: Type of search (web, news, images, videos)
            **kwargs: Additional search parameters
            
        Returns:
            Search results from Serper API
            
        Raises:
            SerperAPIError: If API request fails
        """
        await self._rate_limit()
        
        # Prepare request payload
        payload = {
            "q": query,
            "type": search_type,
            **kwargs
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        logger.info(f"Async searching for: {query} (type: {search_type})")
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=self.headers
                ) as response:
                    
                    if response.status != 200:
                        error_msg = f"Serper API error: {response.status}"
                        try:
                            error_data = await response.json()
                            error_msg += f" - {error_data.get('message', 'Unknown error')}"
                        except:
                            error_text = await response.text()
                            error_msg += f" - {error_text}"
                        
                        raise SerperAPIError(error_msg, response.status, error_data if 'error_data' in locals() else None)
                    
                    result = await response.json()
                    logger.info(f"Async search completed: {query} - Found {len(result.get('organic', []))} results")
                    
                    return result
                    
        except asyncio.TimeoutError:
            raise SerperAPIError(f"Request timeout for query: {query}")
        except aiohttp.ClientError as e:
            raise SerperAPIError(f"Request failed for query {query}: {str(e)}")
        except json.JSONDecodeError as e:
            raise SerperAPIError(f"Invalid JSON response for query {query}: {str(e)}")
    
    async def parse_search_results(self, response: Dict[str, Any]) -> List[SearchResult]:
        """Parse Serper API response into SearchResult objects.
        
        Args:
            response: Raw response from Serper API
            
        Returns:
            List of parsed SearchResult objects
        """
        results = []
        
        # Parse organic results
        organic_results = response.get("organic", [])
        for i, result in enumerate(organic_results):
            try:
                search_result = SearchResult(
                    title=result.get("title", ""),
                    url=result.get("link", ""),
                    snippet=result.get("snippet", ""),
                    position=i + 1,
                    source=result.get("displayLink", ""),
                    image_url=result.get("imageUrl"),
                    sitelinks=result.get("sitelinks"),
                    date=result.get("date")
                )
                results.append(search_result)
            except Exception as e:
                logger.warning(f"Failed to parse search result {i}: {e}")
                continue
        
        # Parse news results if present
        news_results = response.get("news", [])
        for i, result in enumerate(news_results):
            try:
                search_result = SearchResult(
                    title=result.get("title", ""),
                    url=result.get("link", ""),
                    snippet=result.get("snippet", ""),
                    position=len(results) + i + 1,
                    source=result.get("source", ""),
                    image_url=result.get("imageUrl"),
                    date=result.get("date")
                )
                results.append(search_result)
            except Exception as e:
                logger.warning(f"Failed to parse news result {i}: {e}")
                continue
        
        logger.info(f"Parsed {len(results)} search results")
        return results 