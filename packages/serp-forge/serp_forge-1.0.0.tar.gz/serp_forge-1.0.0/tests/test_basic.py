"""
Basic tests for Serp Forge.

These tests cover fundamental functionality and basic use cases.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from serp_forge.config import Config, SerperConfig, ScrapingConfig
from serp_forge.serper.models import SearchResult, ScrapedContent, SearchResponse
from serp_forge.serper.client import SerperClient, SerperAPIError
from serp_forge.serper.core import scrape, batch_scrape


class TestBasicConfig:
    """Basic configuration tests."""
    
    def test_config_creation(self):
        """Test basic config creation."""
        config = Config()
        assert config is not None
        assert config.environment == "development"
        assert config.debug is False
    
    def test_serper_config(self):
        """Test SerperConfig creation."""
        serper_config = SerperConfig(api_key="test_key")
        assert serper_config.api_key == "test_key"
        assert serper_config.base_url == "https://google.serper.dev"
        assert serper_config.timeout == 30
    
    def test_scraping_config(self):
        """Test ScrapingConfig creation."""
        scraping_config = ScrapingConfig(
            max_concurrent=5,
            retry_delay=[1, 3, 5],
            request_timeout=30
        )
        assert scraping_config.max_concurrent == 5
        assert scraping_config.retry_delay == [1, 3, 5]
        assert scraping_config.request_timeout == 30
    
    def test_config_validation(self):
        """Test config validation."""
        config = Config()
        
        # Test valid retry delay
        config.scraping.retry_delay = [1, 3, 5]
        assert config.scraping.retry_delay == [1, 3, 5]
        
        # Test invalid retry delay - should raise ValueError during validation
        with pytest.raises(ValueError):
            from serp_forge.config import ScrapingConfig
            ScrapingConfig(retry_delay=[])
    
    def test_config_serialization(self):
        """Test config serialization."""
        config = Config()
        config.environment = "test"
        config.debug = True
        
        config_dict = config.to_dict()
        assert config_dict["environment"] == "test"
        assert config_dict["debug"] is True
        
        # Test update from dict
        new_config = Config()
        new_config.update_from_dict(config_dict)
        assert new_config.environment == "test"
        assert new_config.debug is True


class TestBasicModels:
    """Basic model tests."""
    
    def test_search_result(self):
        """Test SearchResult model."""
        result = SearchResult(
            title="Test Article",
            url="https://example.com/article",
            snippet="This is a test article",
            position=1,
            source="example.com"
        )
        
        assert result.title == "Test Article"
        assert str(result.url).rstrip("/") == "https://example.com/article"
        assert result.snippet == "This is a test article"
        assert result.position == 1
        assert result.source == "example.com"
    
    def test_scraped_content(self):
        """Test ScrapedContent model."""
        content = ScrapedContent(
            title="Test Content",
            url="https://example.com/content",
            source="example.com",
            content="This is the main content of the article."
        )
        
        assert content.title == "Test Content"
        assert str(content.url).rstrip("/") == "https://example.com/content"
        assert content.source == "example.com"
        assert content.content == "This is the main content of the article."
        assert content.word_count == 8  # "This is the main content of the article."
    
    def test_search_response(self):
        """Test SearchResponse model."""
        response = SearchResponse(
            success=True,
            query="test query",
            total_results=5,
            scraped_successfully=3,
            execution_time=2.5,
            results=[],
            failed_urls=[],
            proxy_stats={},
            error_message=None,
            request_id="test_123"
        )
        
        assert response.success is True
        assert response.query == "test query"
        assert response.total_results == 5
        assert response.scraped_successfully == 3
        assert response.execution_time == 2.5
        assert response.request_id == "test_123"
    
    def test_search_result_with_optional_fields(self):
        """Test SearchResult with optional fields."""
        result = SearchResult(
            title="Test Article",
            url="https://example.com/article",
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


class TestBasicClient:
    """Basic client tests."""
    
    def test_client_creation(self):
        """Test SerperClient creation."""
        client = SerperClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://google.serper.dev"
        assert client.session.headers["X-API-KEY"] == "test_key"
        assert client.session.headers["Content-Type"] == "application/json"
    
    def test_parse_search_results(self):
        """Test parsing search results."""
        client = SerperClient(api_key="test_key")
        
        response = {
            "organic": [
                {
                    "title": "Test Result 1",
                    "link": "https://example1.com",
                    "snippet": "Test snippet 1",
                    "displayLink": "example1.com"
                },
                {
                    "title": "Test Result 2",
                    "link": "https://example2.com",
                    "snippet": "Test snippet 2",
                    "displayLink": "example2.com"
                }
            ]
        }
        
        results = client.parse_search_results(response)
        
        assert len(results) == 2
        assert results[0].title == "Test Result 1"
        assert str(results[0].url).rstrip("/") == "https://example1.com"
        assert results[0].position == 1
        assert results[1].title == "Test Result 2"
        assert results[1].position == 2
    
    def test_parse_empty_results(self):
        """Test parsing empty search results."""
        client = SerperClient(api_key="test_key")
        
        response = {"organic": []}
        results = client.parse_search_results(response)
        
        assert len(results) == 0
    
    def test_parse_malformed_results(self):
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
    
    def test_serper_api_error(self):
        """Test SerperAPIError creation."""
        error = SerperAPIError("Test error", 429, {"message": "Rate limited"})
        assert str(error) == "Test error"
        assert error.status_code == 429
        assert error.response == {"message": "Rate limited"}


class TestBasicCore:
    """Basic core functionality tests."""
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_basic_scrape(self, mock_scraper_class, mock_client_class):
        """Test basic scraping functionality."""
        # Mock client
        mock_client = Mock()
        mock_client.search.return_value = {
            "organic": [
                {
                    "title": "Test Result",
                    "link": "https://example.com",
                    "snippet": "Test snippet",
                    "displayLink": "example.com"
                }
            ]
        }
        mock_client.parse_search_results.return_value = [
            SearchResult(
                title="Test Result",
                url="https://example.com",
                snippet="Test snippet",
                position=1,
                source="example.com"
            )
        ]
        mock_client_class.return_value = mock_client
        
        # Mock scraper to return None (no content scraping)
        mock_scraper = Mock()
        mock_scraper.scrape_url.return_value = None
        mock_scraper_class.return_value = mock_scraper
        
        # Execute scraping
        result = scrape("test query", max_results=1)
        
        # Verify results
        assert result.success is True
        assert result.query == "test query"
        assert result.total_results == 1
        assert result.scraped_successfully == 0  # No content scraping
        assert len(result.results) == 0  # No content results
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_scrape_with_content(self, mock_scraper_class, mock_client_class):
        """Test scraping with content extraction."""
        # Mock client
        mock_client = Mock()
        mock_client.search.return_value = {
            "organic": [
                {
                    "title": "Test Result",
                    "link": "https://example.com",
                    "snippet": "Test snippet",
                    "displayLink": "example.com"
                }
            ]
        }
        mock_client.parse_search_results.return_value = [
            SearchResult(
                title="Test Result",
                url="https://example.com",
                snippet="Test snippet",
                position=1,
                source="example.com"
            )
        ]
        mock_client_class.return_value = mock_client
        
        # Mock scraper
        mock_scraper = Mock()
        mock_scraper.scrape_url.return_value = ScrapedContent(
            title="Test Content",
            url="https://example.com",
            source="example.com",
            content="This is test content."
        )
        mock_scraper_class.return_value = mock_scraper
        
        # Execute scraping with content
        result = scrape("test query", max_results=1, include_content=True)
        
        # Verify results
        assert result.success is True
        assert result.total_results == 1
        assert result.scraped_successfully == 1
        assert len(result.results) == 1
        assert result.results[0].word_count == 4  # "This is test content."
    
    @patch('serp_forge.serper.core.SerperClient')
    def test_scrape_failure(self, mock_client_class):
        """Test scraping with API failure."""
        # Mock client that raises error
        mock_client = Mock()
        mock_client.search.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client
        
        # Execute scraping
        result = scrape("test query", max_results=1)
        
        # Verify error handling
        assert result.success is False
        assert "API Error" in result.error_message
        assert result.total_results == 0
        assert result.scraped_successfully == 0
    
    @patch('serp_forge.serper.core.scrape')
    def test_batch_scrape(self, mock_scrape):
        """Test batch scraping functionality."""
        # Mock scrape function to return different responses for each call
        def mock_scrape_side_effect(query, **kwargs):
            return SearchResponse(
                success=True,
                query=query,
                total_results=1,
                scraped_successfully=1,
                execution_time=1.0,
                results=[
                    ScrapedContent(
                        title="Test",
                        url="https://example.com",
                        source="example.com",
                        content="Test content"
                    )
                ]
            )
        
        mock_scrape.side_effect = mock_scrape_side_effect
        
        # Execute batch scraping
        queries = ["query1", "query2"]
        result = batch_scrape(queries, max_results_per_query=1, parallel=False)
        
        # Verify results
        assert result.success is True
        assert result.total_queries == 2
        assert result.successful_queries == 2
        assert result.failed_queries == 0
        assert len(result.results_by_query) == 2
    
    @patch('serp_forge.serper.core.scrape')
    def test_duplicate_queries(self, mock_scrape):
        """Test batch scraping with duplicate queries."""
        # Mock scrape function to return different responses for each call
        def mock_scrape_side_effect(query, **kwargs):
            return SearchResponse(
                success=True,
                query=query,
                total_results=1,
                scraped_successfully=0,
                execution_time=1.0,
                results=[]
            )
        
        mock_scrape.side_effect = mock_scrape_side_effect
        
        queries = ["query1", "query1", "query2"]
        result = batch_scrape(queries, max_results_per_query=1, parallel=False)
        # Should handle duplicates gracefully
        assert result.success is True
        assert result.total_queries == 2  # Only unique queries are processed


class TestBasicEdgeCases:
    """Basic edge case tests."""
    
    def test_empty_query(self):
        """Test scraping with empty query."""
        result = scrape("", max_results=1)
        assert result.success is False
        assert "empty" in result.error_message.lower()
    
    def test_zero_max_results(self):
        """Test scraping with zero max results."""
        result = scrape("test query", max_results=0)
        assert result.success is False
        assert "max_results" in result.error_message.lower()
    
    def test_negative_max_results(self):
        """Test scraping with negative max results."""
        result = scrape("test query", max_results=-1)
        assert result.success is False
        assert "max_results" in result.error_message.lower()
    
    def test_large_max_results(self):
        """Test scraping with very large max results."""
        result = scrape("test query", max_results=1000)
        assert result.success is False
        assert "max_results" in result.error_message.lower()
    
    def test_invalid_search_type(self):
        """Test scraping with invalid search type."""
        result = scrape("test query", search_type="invalid")
        assert result.success is False
        assert "search_type" in result.error_message.lower()
    
    def test_empty_batch_queries(self):
        """Test batch scraping with empty queries list."""
        result = batch_scrape([], max_results_per_query=1)
        assert result.success is False
        assert "empty" in result.error_message.lower()


class TestBasicValidation:
    """Basic validation tests."""
    
    def test_url_validation(self):
        """Test URL validation in models."""
        # Valid URL
        result = SearchResult(
            title="Test",
            url="https://example.com",
            snippet="Test",
            position=1,
            source="example.com"
        )
        assert result is not None
        
        # Invalid URL should raise validation error
        with pytest.raises(Exception):
            SearchResult(
                title="Test",
                url="not-a-valid-url",
                snippet="Test",
                position=1,
                source="example.com"
            )
    
    def test_position_validation(self):
        """Test position validation in models."""
        # Valid position
        result = SearchResult(
            title="Test",
            url="https://example.com",
            snippet="Test",
            position=1,
            source="example.com"
        )
        assert result.position == 1
        
        # Invalid position should raise validation error
        with pytest.raises(Exception):
            SearchResult(
                title="Test",
                url="https://example.com",
                snippet="Test",
                position=0,  # Should be > 0
                source="example.com"
            )
    
    def test_content_validation(self):
        """Test content validation in models."""
        # Valid content
        content = ScrapedContent(
            title="Test",
            url="https://example.com",
            source="example.com",
            content="Valid content"
        )
        assert content.content == "Valid content"
        
        # Empty content should be allowed
        content = ScrapedContent(
            title="Test",
            url="https://example.com",
            source="example.com",
            content=""
        )
        assert content.content == ""
        assert content.word_count == 0


if __name__ == "__main__":
    pytest.main([__file__]) 