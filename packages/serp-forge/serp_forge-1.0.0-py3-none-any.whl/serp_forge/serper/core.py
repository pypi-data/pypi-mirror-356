"""
Core scraping functionality for Serp Forge.
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Union

from ..config import config
from ..utils.logging import get_logger
from .client import SerperClient, AsyncSerperClient, SerperAPIError
from .models import SearchResult, ScrapedContent, SearchResponse, BatchSearchResponse
from .scraper import ContentScraper

logger = get_logger(__name__)


def _validate_query(query: str) -> None:
    """Validate search query."""
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")


def _validate_max_results(max_results: int) -> None:
    """Validate max_results parameter."""
    if max_results <= 0:
        raise ValueError("max_results must be greater than 0")
    if max_results > 100:
        raise ValueError("max_results cannot exceed 100")


def _validate_search_type(search_type: str) -> None:
    """Validate search type."""
    valid_types = ["web", "news", "images", "videos"]
    if search_type not in valid_types:
        raise ValueError(f"search_type must be one of {valid_types}")


def _validate_batch_queries(queries: List[str]) -> None:
    """Validate batch queries."""
    if not queries:
        raise ValueError("Queries list cannot be empty")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_queries = []
    for query in queries:
        if query not in seen:
            seen.add(query)
            unique_queries.append(query)
    
    if len(unique_queries) != len(queries):
        logger.warning("Duplicate queries removed from batch")
    
    return unique_queries


def scrape(
    query: str,
    search_type: str = "web",
    max_results: int = 10,
    include_content: bool = True,
    proxy_rotation: bool = True,
    extract_metadata: bool = True,
    **kwargs
) -> SearchResponse:
    """Main scraping function.
    
    Args:
        query: Search query
        search_type: Type of search (web, news, images, videos)
        max_results: Maximum number of results to return
        include_content: Whether to scrape content from URLs
        proxy_rotation: Whether to use proxy rotation
        extract_metadata: Whether to extract metadata
        **kwargs: Additional search parameters
        
    Returns:
        SearchResponse with scraped results
    """
    start_time = time.time()
    
    try:
        # Validate inputs
        _validate_query(query)
        _validate_max_results(max_results)
        _validate_search_type(search_type)
        
        # Initialize components
        client = SerperClient()
        scraper = ContentScraper() if include_content else None
        
        # Perform search
        logger.info(f"Starting search for: {query}")
        search_response = client.search(
            query=query,
            search_type=search_type,
            num=max_results,
            **kwargs
        )
        
        # Parse search results
        search_results = client.parse_search_results(search_response)
        
        # Scrape content if requested
        scraped_results = []
        failed_urls = []
        
        if include_content and scraper:
            logger.info(f"Scraping content from {len(search_results)} URLs")
            
            for result in search_results:
                try:
                    scraped_content = scraper.scrape_url(
                        url=str(result.url),
                        title=result.title,
                        source=result.source,
                        proxy_rotation=proxy_rotation
                    )
                    
                    if scraped_content:
                        scraped_results.append(scraped_content)
                    else:
                        failed_urls.append(str(result.url))
                        
                except Exception as e:
                    logger.error(f"Failed to scrape {result.url}: {e}")
                    failed_urls.append(str(result.url))
        
        # Create response
        execution_time = time.time() - start_time
        
        response = SearchResponse(
            success=True,
            query=query,
            total_results=len(search_results),
            scraped_successfully=len(scraped_results),
            execution_time=execution_time,
            results=scraped_results,
            failed_urls=failed_urls
        )
        
        logger.info(f"Search completed: {query} - {len(scraped_results)}/{len(search_results)} scraped successfully")
        
        return response
        
    except SerperAPIError as e:
        logger.error(f"Serper API error: {e}")
        return SearchResponse(
            success=False,
            query=query,
            error_message=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
        return SearchResponse(
            success=False,
            query=query,
            error_message=str(e)
        )
    finally:
        if 'client' in locals():
            client.close()


async def async_scrape(
    query: str,
    search_type: str = "web",
    max_results: int = 10,
    include_content: bool = True,
    proxy_rotation: bool = True,
    extract_metadata: bool = True,
    **kwargs
) -> SearchResponse:
    """Async version of the main scraping function.
    
    Args:
        query: Search query
        search_type: Type of search (web, news, images, videos)
        max_results: Maximum number of results to return
        include_content: Whether to scrape content from URLs
        proxy_rotation: Whether to use proxy rotation
        extract_metadata: Whether to extract metadata
        **kwargs: Additional search parameters
        
    Returns:
        SearchResponse with scraped results
    """
    start_time = time.time()
    
    try:
        # Validate inputs
        _validate_query(query)
        _validate_max_results(max_results)
        _validate_search_type(search_type)
        
        # Initialize components
        client = AsyncSerperClient()
        scraper = ContentScraper() if include_content else None
        
        # Perform search
        logger.info(f"Starting async search for: {query}")
        search_response = await client.search(
            query=query,
            search_type=search_type,
            num=max_results,
            **kwargs
        )
        
        # Parse search results
        search_results = await client.parse_search_results(search_response)
        
        # Scrape content if requested
        scraped_results = []
        failed_urls = []
        
        if include_content and scraper:
            logger.info(f"Scraping content from {len(search_results)} URLs")
            
            # Create scraping tasks
            scraping_tasks = []
            for result in search_results:
                task = asyncio.create_task(
                    _scrape_single_url_async(
                        scraper, result, proxy_rotation
                    )
                )
                scraping_tasks.append(task)
            
            # Execute all scraping tasks concurrently
            scraping_results = await asyncio.gather(*scraping_tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(scraping_results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to scrape {search_results[i].url}: {result}")
                    failed_urls.append(str(search_results[i].url))
                elif result:
                    scraped_results.append(result)
                else:
                    failed_urls.append(str(search_results[i].url))
        
        # Create response
        execution_time = time.time() - start_time
        
        response = SearchResponse(
            success=True,
            query=query,
            total_results=len(search_results),
            scraped_successfully=len(scraped_results),
            execution_time=execution_time,
            results=scraped_results,
            failed_urls=failed_urls
        )
        
        logger.info(f"Async search completed: {query} - {len(scraped_results)}/{len(search_results)} scraped successfully")
        
        return response
        
    except SerperAPIError as e:
        logger.error(f"Serper API error: {e}")
        return SearchResponse(
            success=False,
            query=query,
            error_message=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error during async scraping: {e}")
        return SearchResponse(
            success=False,
            query=query,
            error_message=str(e)
        )


async def _scrape_single_url_async(
    scraper: ContentScraper,
    search_result: SearchResult,
    proxy_rotation: bool
) -> Optional[ScrapedContent]:
    """Scrape a single URL asynchronously.
    
    Args:
        scraper: Content scraper instance
        search_result: Search result to scrape
        proxy_rotation: Whether to use proxy rotation
        
    Returns:
        Scraped content or None if failed
    """
    try:
        return scraper.scrape_url(
            url=str(search_result.url),
            title=search_result.title,
            source=search_result.source,
            proxy_rotation=proxy_rotation
        )
    except Exception as e:
        logger.error(f"Failed to scrape {search_result.url}: {e}")
        return None


def batch_scrape(
    queries: List[str],
    search_type: str = "web",
    max_results_per_query: int = 10,
    parallel: bool = True,
    save_to: Optional[str] = None,
    **kwargs
) -> BatchSearchResponse:
    """Perform batch scraping of multiple queries.
    
    Args:
        queries: List of search queries
        search_type: Type of search
        max_results_per_query: Maximum results per query
        parallel: Whether to run queries in parallel
        save_to: Optional file path to save results
        **kwargs: Additional parameters passed to scrape()
        
    Returns:
        BatchSearchResponse with results for all queries
    """
    start_time = time.time()
    
    try:
        # Validate inputs
        _validate_search_type(search_type)
        _validate_max_results(max_results_per_query)
        unique_queries = _validate_batch_queries(queries)
        
        if parallel:
            # Run queries in parallel using asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_batch():
                tasks = []
                for query in unique_queries:
                    task = async_scrape(
                        query=query,
                        search_type=search_type,
                        max_results=max_results_per_query,
                        **kwargs
                    )
                    tasks.append(task)
                
                return await asyncio.gather(*tasks)
            
            results = loop.run_until_complete(run_batch())
            loop.close()
        else:
            # Run queries sequentially
            results = []
            for query in unique_queries:
                result = scrape(
                    query=query,
                    search_type=search_type,
                    max_results=max_results_per_query,
                    **kwargs
                )
                results.append(result)
        
        # Aggregate results
        total_execution_time = time.time() - start_time
        successful_queries = sum(1 for r in results if r.success)
        failed_queries = len(unique_queries) - successful_queries
        
        total_results = sum(r.total_results for r in results)
        total_scraped = sum(r.scraped_successfully for r in results)
        
        # Create results dictionary
        results_by_query = {query: result for query, result in zip(unique_queries, results)}
        
        # Create batch response
        batch_response = BatchSearchResponse(
            success=successful_queries > 0,
            total_queries=len(unique_queries),
            successful_queries=successful_queries,
            failed_queries=failed_queries,
            total_execution_time=total_execution_time,
            results_by_query=results_by_query,
            total_results=total_results,
            total_scraped=total_scraped
        )
        
        # Save to file if requested
        if save_to:
            _save_batch_results(batch_response, save_to)
        
        logger.info(f"Batch scraping completed: {successful_queries}/{len(unique_queries)} queries successful")
        
        return batch_response
        
    except Exception as e:
        logger.error(f"Unexpected error during batch scraping: {e}")
        return BatchSearchResponse(
            success=False,
            total_queries=len(queries),
            error_message=str(e)
        )


def _save_batch_results(batch_response: BatchSearchResponse, file_path: str) -> None:
    """Save batch results to file.
    
    Args:
        batch_response: Batch search response
        file_path: File path to save results
    """
    try:
        import json
        from pathlib import Path
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict for JSON serialization
        data = batch_response.model_dump()
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Batch results saved to: {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to save batch results to {file_path}: {e}")


# Convenience functions for different search types
def search_news(
    query: str,
    max_results: int = 10,
    include_content: bool = True,
    **kwargs
) -> SearchResponse:
    """Search for news articles.
    
    Args:
        query: News search query
        max_results: Maximum number of results
        include_content: Whether to scrape content
        **kwargs: Additional parameters
        
    Returns:
        SearchResponse with news results
    """
    return scrape(
        query=query,
        search_type="news",
        max_results=max_results,
        include_content=include_content,
        **kwargs
    )


def search_images(
    query: str,
    max_results: int = 10,
    **kwargs
) -> SearchResponse:
    """Search for images.
    
    Args:
        query: Image search query
        max_results: Maximum number of results
        **kwargs: Additional parameters
        
    Returns:
        SearchResponse with image results
    """
    return scrape(
        query=query,
        search_type="images",
        max_results=max_results,
        include_content=False,  # No content scraping for images
        **kwargs
    )


def search_videos(
    query: str,
    max_results: int = 10,
    **kwargs
) -> SearchResponse:
    """Search for videos.
    
    Args:
        query: Video search query
        max_results: Maximum number of results
        **kwargs: Additional parameters
        
    Returns:
        SearchResponse with video results
    """
    return scrape(
        query=query,
        search_type="videos",
        max_results=max_results,
        include_content=False,  # No content scraping for videos
        **kwargs
    ) 