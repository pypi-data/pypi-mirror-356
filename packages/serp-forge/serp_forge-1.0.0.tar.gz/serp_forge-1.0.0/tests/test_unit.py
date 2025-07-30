"""
Unit tests for Serp Forge.

These tests focus on individual components, methods, and edge cases.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import json
import os

from serp_forge.config import (
    Config, SerperConfig, ScrapingConfig, AntiDetectionConfig, 
    ProxyConfig, ContentExtractionConfig, OutputConfig
)
from serp_forge.serper.models import (
    SearchResult, ScrapedContent, SearchResponse, SearchRequest,
    BatchSearchRequest, BatchSearchResponse
)
from serp_forge.serper.client import SerperClient, SerperAPIError
from serp_forge.serper.core import scrape, batch_scrape
from serp_forge.serper.scraper import ContentScraper


class TestUnitConfig:
    """Unit tests for configuration classes."""
    
    def test_serper_config_defaults(self):
        """Test SerperConfig default values."""
        config = SerperConfig()
        
        assert config.api_key is None
        assert config.base_url == "https://google.serper.dev"
        assert config.timeout == 30
        assert config.max_requests_per_minute == 60
    
    def test_serper_config_with_api_key(self):
        """Test SerperConfig with API key."""
        config = SerperConfig(api_key="test_key")
        
        assert config.api_key == "test_key"
        assert config.base_url == "https://google.serper.dev"
    
    def test_scraping_config_validation(self):
        """Test ScrapingConfig field validation."""
        # Valid retry delay
        config = ScrapingConfig(retry_delay=[1, 3, 5])
        assert config.retry_delay == [1, 3, 5]
        
        # Invalid retry delay - should raise ValueError
        with pytest.raises(ValueError):
            ScrapingConfig(retry_delay=[])
        
        with pytest.raises(ValueError):
            ScrapingConfig(retry_delay=[-1, 2, 3])
    
    def test_anti_detection_config_validation(self):
        """Test AntiDetectionConfig field validation."""
        # Valid random delays
        config = AntiDetectionConfig(random_delays=[1, 4])
        assert config.random_delays == [1, 4]
        
        # Invalid random delays
        with pytest.raises(ValueError):
            AntiDetectionConfig(random_delays=[1])  # Wrong length
        
        with pytest.raises(ValueError):
            AntiDetectionConfig(random_delays=[5, 2])  # Min > Max
    
    def test_proxy_config_validation(self):
        """Test ProxyConfig field validation."""
        # Valid rotation strategy
        config = ProxyConfig(rotation_strategy="round_robin")
        assert config.rotation_strategy == "round_robin"
        
        # Invalid rotation strategy
        with pytest.raises(ValueError):
            ProxyConfig(rotation_strategy="invalid")
    
    def test_output_config_validation(self):
        """Test OutputConfig field validation."""
        # Valid format
        config = OutputConfig(format="json")
        assert config.format == "json"
        
        # Invalid format
        with pytest.raises(ValueError):
            OutputConfig(format="invalid")
    
    def test_config_proxy_list_loading(self):
        """Test Config proxy list loading from environment."""
        # Set environment variable
        os.environ["SERP_FORGE_PROXY_LIST"] = "proxy1.com:8080,proxy2.com:8080"
        
        config = Config()
        
        assert len(config.proxy.residential_proxies) == 2
        assert "proxy1.com:8080" in config.proxy.residential_proxies
        assert "proxy2.com:8080" in config.proxy.residential_proxies
        
        # Clean up
        del os.environ["SERP_FORGE_PROXY_LIST"]
    
    def test_config_user_agents_loading(self, tmp_path):
        """Test Config user agents loading from file."""
        # Create user agents file
        user_agents_file = tmp_path / "user_agents.txt"
        with open(user_agents_file, "w") as f:
            f.write("Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n")
            f.write("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\n")
        
        # Set environment variable
        os.environ["SERP_FORGE_USER_AGENTS"] = str(user_agents_file)
        
        config = Config()
        
        user_agents = config.get_custom_user_agents()
        assert len(user_agents) == 2
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" in user_agents
        assert "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" in user_agents
        
        # Clean up
        del os.environ["SERP_FORGE_USER_AGENTS"]


class TestUnitModels:
    """Unit tests for data models."""
    
    def test_search_result_creation(self):
        """Test SearchResult model creation."""
        result = SearchResult(
            title="Test Title",
            url="https://example.com",
            snippet="Test snippet",
            position=1,
            source="example.com"
        )
        
        assert result.title == "Test Title"
        assert str(result.url).rstrip("/") == "https://example.com"
        assert result.snippet == "Test snippet"
        assert result.position == 1
        assert result.source == "example.com"
        assert result.image_url is None
        assert result.sitelinks is None
        assert result.date is None
    
    def test_search_result_with_optional_fields(self):
        """Test SearchResult with optional fields."""
        result = SearchResult(
            title="Test Title",
            url="https://example.com",
            snippet="Test snippet",
            position=1,
            source="example.com",
            image_url="https://example.com/image.jpg",
            sitelinks=[{"title": "Link 1", "link": "https://example.com/link1"}],
            date="2023-01-01"
        )
        
        assert result.image_url is not None
        assert result.sitelinks is not None
        assert result.date == "2023-01-01"
    
    def test_scraped_content_word_count(self):
        """Test ScrapedContent word count calculation."""
        # Empty content
        content = ScrapedContent(
            title="Test",
            url="https://example.com",
            source="example.com",
            content=""
        )
        assert content.word_count == 0
        
        # Single word
        content = ScrapedContent(
            title="Test",
            url="https://example.com",
            source="example.com",
            content="Hello"
        )
        assert content.word_count == 1
        
        # Multiple words
        content = ScrapedContent(
            title="Test",
            url="https://example.com",
            source="example.com",
            content="Hello world this is a test"
        )
        assert content.word_count == 6
        
        # With extra whitespace
        content = ScrapedContent(
            title="Test",
            url="https://example.com",
            source="example.com",
            content="  Hello   world  "
        )
        assert content.word_count == 2
    
    def test_scraped_content_with_metadata(self):
        """Test ScrapedContent with metadata."""
        content = ScrapedContent(
            title="Test Article",
            url="https://example.com/article",
            source="example.com",
            content="Test content",
            author="John Doe",
            publish_date=datetime(2023, 1, 1),
            sentiment="positive",
            sentiment_score=0.8,
            keywords=["test", "article"],
            summary="This is a test article",
            language="en",
            quality_score=0.9
        )
        
        assert content.author == "John Doe"
        assert content.publish_date == datetime(2023, 1, 1)
        assert content.sentiment == "positive"
        assert content.sentiment_score == 0.8
        assert content.keywords == ["test", "article"]
        assert content.summary == "This is a test article"
        assert content.language == "en"
        assert content.quality_score == 0.9
    
    def test_search_request_creation(self):
        """Test SearchRequest model creation."""
        request = SearchRequest(
            query="test query",
            search_type="news",
            max_results=20,
            include_content=False,
            country="uk",
            language="en",
            time_period="d",
            safe_search=False
        )
        
        assert request.query == "test query"
        assert request.search_type == "news"
        assert request.max_results == 20
        assert request.include_content is False
        assert request.country == "uk"
        assert request.language == "en"
        assert request.time_period == "d"
        assert request.safe_search is False
    
    def test_batch_search_request_creation(self):
        """Test BatchSearchRequest model creation."""
        request = BatchSearchRequest(
            queries=["query1", "query2", "query3"],
            search_type="web",
            max_results_per_query=5,
            parallel=True,
            save_to="results.json"
        )
        
        assert request.queries == ["query1", "query2", "query3"]
        assert request.search_type == "web"
        assert request.max_results_per_query == 5
        assert request.parallel is True
        assert request.save_to == "results.json"
    
    def test_search_response_creation(self):
        """Test SearchResponse model creation."""
        response = SearchResponse(
            success=True,
            query="test query",
            total_results=10,
            scraped_successfully=8,
            execution_time=2.5,
            results=[],
            failed_urls=["https://example.com/failed"],
            proxy_stats={"total_requests": 10, "successful": 8},
            error_message=None,
            request_id="req_123"
        )
        
        assert response.success is True
        assert response.query == "test query"
        assert response.total_results == 10
        assert response.scraped_successfully == 8
        assert response.execution_time == 2.5
        assert len(response.failed_urls) == 1
        assert response.proxy_stats["total_requests"] == 10
        assert response.request_id == "req_123"
    
    def test_batch_search_response_creation(self):
        """Test BatchSearchResponse model creation."""
        response = BatchSearchResponse(
            success=True,
            total_queries=3,
            successful_queries=2,
            failed_queries=1,
            total_execution_time=5.0,
            results_by_query={},
            total_results=20,
            total_scraped=15,
            batch_id="batch_123"
        )
        
        assert response.success is True
        assert response.total_queries == 3
        assert response.successful_queries == 2
        assert response.failed_queries == 1
        assert response.total_execution_time == 5.0
        assert response.total_results == 20
        assert response.total_scraped == 15
        assert response.batch_id == "batch_123"


class TestUnitClient:
    """Unit tests for SerperClient."""
    
    def test_client_initialization(self):
        """Test SerperClient initialization."""
        client = SerperClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://google.serper.dev"
        # Get actual values from config since they might have been modified
        from serp_forge.config import config
        assert client.timeout == config.serper.timeout
        assert client.max_requests_per_minute == config.serper.max_requests_per_minute
        assert client.session.headers["X-API-KEY"] == "test_key"
    
    def test_client_initialization_from_config(self):
        """Test SerperClient initialization from config."""
        # Update global config
        from serp_forge.config import config
        config.serper.api_key = "config_key"
        config.serper.timeout = 60
        config.serper.max_requests_per_minute = 30
        
        client = SerperClient()
        assert client.api_key == "config_key"
        assert client.timeout == 60
        assert client.max_requests_per_minute == 30
        assert client.session.headers["X-API-KEY"] == "config_key"
    
    @patch('serp_forge.serper.client.requests.Session')
    def test_rate_limiting(self, mock_session):
        """Test rate limiting functionality."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        client = SerperClient(api_key="test_key")
        
        # First request should go through immediately
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"organic": []}
        mock_session_instance.post.return_value = mock_response
        
        client.search("query1")
        
        # Second request should be rate limited
        client.search("query2")
        
        # Verify both requests were made
        assert mock_session_instance.post.call_count == 2
    
    def test_parse_search_results_empty(self):
        """Test parsing empty search results."""
        client = SerperClient(api_key="test_key")
        
        response = {"organic": []}
        results = client.parse_search_results(response)
        
        assert len(results) == 0
    
    def test_parse_search_results_with_news(self):
        """Test parsing search results with news results."""
        client = SerperClient(api_key="test_key")
        
        response = {
            "organic": [
                {
                    "title": "Organic Result",
                    "link": "https://example.com/organic",
                    "snippet": "Organic snippet",
                    "displayLink": "example.com"
                }
            ],
            "news": [
                {
                    "title": "News Result",
                    "link": "https://example.com/news",
                    "snippet": "News snippet",
                    "source": "news.com"
                }
            ]
        }
        
        results = client.parse_search_results(response)
        
        assert len(results) == 2
        assert results[0].title == "Organic Result"
        assert results[1].title == "News Result"
        assert results[1].position == 2  # News results get incremented position
    
    def test_parse_search_results_malformed(self):
        """Test parsing malformed search results."""
        client = SerperClient(api_key="test_key")
        
        response = {
            "organic": [
                {
                    "title": "Valid Result",
                    "link": "https://example.com/valid",
                    "snippet": "Valid snippet",
                    "displayLink": "example.com"
                },
                {
                    # Missing required fields
                    "title": "Invalid Result"
                }
            ]
        }
        
        results = client.parse_search_results(response)
        
        # Should only parse the valid result
        assert len(results) == 1
        assert results[0].title == "Valid Result"


class TestUnitScraper:
    """Unit tests for ContentScraper."""
    
    def test_scraper_initialization(self):
        """Test ContentScraper initialization."""
        scraper = ContentScraper()
        
        assert scraper is not None
        # Add more assertions based on actual implementation
    
    @patch('serp_forge.serper.scraper.requests.get')
    def test_scrape_url_success(self, mock_get):
        """Test successful URL scraping."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Content</h1>
                <p>This is test content for scraping.</p>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        scraper = ContentScraper()
        result = scraper.scrape_url("https://example.com")
        
        assert result is not None
        # Add more assertions based on actual implementation
    
    @patch('serp_forge.serper.scraper.requests.get')
    def test_scrape_url_failure(self, mock_get):
        """Test URL scraping failure."""
        # Mock failed response
        mock_get.side_effect = Exception("Network error")
        scraper = ContentScraper()
        # If the code handles the exception internally, just check the result is None
        result = scraper.scrape_url("https://example.com/fail")
        assert result is None


class TestUnitErrorHandling:
    """Unit tests for error handling."""
    
    def test_serper_api_error_creation(self):
        """Test SerperAPIError creation."""
        error = SerperAPIError("Test error", 429, {"message": "Rate limited"})
        
        assert str(error) == "Test error"
        assert error.status_code == 429
        assert error.response == {"message": "Rate limited"}
    
    def test_serper_api_error_without_response(self):
        """Test SerperAPIError without response data."""
        error = SerperAPIError("Test error", 500)
        
        assert str(error) == "Test error"
        assert error.status_code == 500
        assert error.response is None


class TestUnitEdgeCases:
    """Unit tests for edge cases."""
    
    def test_config_with_invalid_environment_file(self, tmp_path):
        """Test Config with non-existent environment file."""
        config_file = tmp_path / "nonexistent.yaml"
        
        with pytest.raises(FileNotFoundError):
            Config.load_from_file(config_file)
    
    def test_config_with_invalid_yaml(self, tmp_path):
        """Test Config with invalid YAML file."""
        config_file = tmp_path / "invalid.yaml"
        with open(config_file, "w") as f:
            f.write("invalid: yaml: content: [")
        
        with pytest.raises(Exception):  # Should raise YAML parsing error
            Config.load_from_file(config_file)
    
    def test_search_result_with_invalid_url(self):
        """Test SearchResult with invalid URL."""
        with pytest.raises(Exception):  # Should raise validation error
            SearchResult(
                title="Test",
                url="not-a-valid-url",
                snippet="Test",
                position=1,
                source="example.com"
            )
    
    def test_scraped_content_with_none_content(self):
        """Test ScrapedContent with None content."""
        with pytest.raises(Exception):
            ScrapedContent(
                title="Test",
                url="https://example.com",
                source="example.com",
                content=None
            )
    
    def test_batch_request_with_empty_queries(self):
        """Test batch_scrape with empty queries list."""
        result = batch_scrape([])
        # Should return a failed response with error message
        assert result.success is False
        assert "empty" in result.error_message.lower()


if __name__ == "__main__":
    pytest.main([__file__]) 