"""
Functional tests for Serp Forge.

These tests focus on end-to-end functionality and integration between components.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from serp_forge.config import Config, SerperConfig, ScrapingConfig
from serp_forge.serper.models import SearchResult, ScrapedContent, SearchResponse
from serp_forge.serper.client import SerperClient, SerperAPIError
from serp_forge.serper.core import scrape, batch_scrape
from serp_forge.serper.scraper import ContentScraper


class TestFunctionalScraping:
    """Test end-to-end scraping functionality."""
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_basic_scraping_workflow(self, mock_scraper_class, mock_client_class):
        """Test complete scraping workflow."""
        # Mock client setup
        mock_client = Mock()
        mock_client.search.return_value = {
            "organic": [
                {
                    "title": "Test Article 1",
                    "link": "https://example1.com/article1",
                    "snippet": "First test article",
                    "displayLink": "example1.com"
                },
                {
                    "title": "Test Article 2", 
                    "link": "https://example2.com/article2",
                    "snippet": "Second test article",
                    "displayLink": "example2.com"
                }
            ]
        }
        
        mock_client.parse_search_results.return_value = [
            SearchResult(
                title="Test Article 1",
                url="https://example1.com/article1",
                snippet="First test article",
                position=1,
                source="example1.com"
            ),
            SearchResult(
                title="Test Article 2",
                url="https://example2.com/article2", 
                snippet="Second test article",
                position=2,
                source="example2.com"
            )
        ]
        mock_client_class.return_value = mock_client
        
        # Mock scraper setup
        mock_scraper = Mock()
        mock_scraper.scrape_url.side_effect = [
            ScrapedContent(
                title="Test Article 1",
                url="https://example1.com/article1",
                source="example1.com",
                content="This is the content of the first article."
            ),
            ScrapedContent(
                title="Test Article 2",
                url="https://example2.com/article2",
                source="example2.com", 
                content="This is the content of the second article."
            )
        ]
        mock_scraper_class.return_value = mock_scraper
        
        # Execute scraping
        result = scrape("test query", max_results=2, include_content=True)
        
        # Verify results
        assert result.success is True
        assert result.query == "test query"
        assert result.total_results == 2
        assert result.scraped_successfully == 2
        assert len(result.results) == 2
        
        # Verify content
        assert result.results[0].title == "Test Article 1"
        assert result.results[0].word_count == 8
        assert result.results[1].title == "Test Article 2"
        assert result.results[1].word_count == 8
        
        # Verify API calls
        mock_client.search.assert_called_once_with(query="test query", search_type="web", num=2)
        assert mock_scraper.scrape_url.call_count == 2
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_scraping_with_partial_failures(self, mock_scraper_class, mock_client_class):
        """Test scraping when some URLs fail to scrape."""
        # Mock client setup
        mock_client = Mock()
        mock_client.search.return_value = {
            "organic": [
                {
                    "title": "Success Article",
                    "link": "https://example.com/success",
                    "snippet": "This will succeed",
                    "displayLink": "example.com"
                },
                {
                    "title": "Failed Article",
                    "link": "https://example.com/failed",
                    "snippet": "This will fail",
                    "displayLink": "example.com"
                }
            ]
        }
        
        mock_client.parse_search_results.return_value = [
            SearchResult(
                title="Success Article",
                url="https://example.com/success",
                snippet="This will succeed",
                position=1,
                source="example.com"
            ),
            SearchResult(
                title="Failed Article",
                url="https://example.com/failed",
                snippet="This will fail",
                position=2,
                source="example.com"
            )
        ]
        mock_client_class.return_value = mock_client
        
        # Mock scraper with one failure
        mock_scraper = Mock()
        mock_scraper.scrape_url.side_effect = [
            ScrapedContent(
                title="Success Article",
                url="https://example.com/success",
                source="example.com",
                content="This succeeded."
            ),
            Exception("Scraping failed")
        ]
        mock_scraper_class.return_value = mock_scraper
        
        # Execute scraping
        result = scrape("test query", max_results=2, include_content=True)
        
        # Verify results
        assert result.success is True
        assert result.total_results == 2
        assert result.scraped_successfully == 1
        assert len(result.results) == 1
        assert len(result.failed_urls) == 1
        assert "https://example.com/failed" in result.failed_urls
    
    @patch('serp_forge.serper.core.SerperClient')
    def test_search_only_mode(self, mock_client_class):
        """Test search without content scraping."""
        # Mock client setup
        mock_client = Mock()
        mock_client.search.return_value = {
            "organic": [
                {
                    "title": "Test Article",
                    "link": "https://example.com/article",
                    "snippet": "Test snippet",
                    "displayLink": "example.com"
                }
            ]
        }
        
        mock_client.parse_search_results.return_value = [
            SearchResult(
                title="Test Article",
                url="https://example.com/article",
                snippet="Test snippet",
                position=1,
                source="example.com"
            )
        ]
        mock_client_class.return_value = mock_client
        
        # Execute search only
        result = scrape("test query", max_results=1, include_content=False)
        
        # Verify results
        assert result.success is True
        assert result.total_results == 1
        assert result.scraped_successfully == 0
        assert len(result.results) == 0
        assert len(result.failed_urls) == 0


class TestFunctionalBatchProcessing:
    """Test batch processing functionality."""
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_batch_scraping_sequential(self, mock_scraper_class, mock_client_class):
        """Test batch scraping in sequential mode."""
        # Mock client setup
        mock_client = Mock()
        mock_client.search.side_effect = [
            {
                "organic": [
                    {
                        "title": "Query 1 Result",
                        "link": "https://example.com/query1",
                        "snippet": "Result for query 1",
                        "displayLink": "example.com"
                    }
                ]
            },
            {
                "organic": [
                    {
                        "title": "Query 2 Result",
                        "link": "https://example.com/query2",
                        "snippet": "Result for query 2",
                        "displayLink": "example.com"
                    }
                ]
            }
        ]
        
        mock_client.parse_search_results.side_effect = [
            [
                SearchResult(
                    title="Query 1 Result",
                    url="https://example.com/query1",
                    snippet="Result for query 1",
                    position=1,
                    source="example.com"
                )
            ],
            [
                SearchResult(
                    title="Query 2 Result",
                    url="https://example.com/query2",
                    snippet="Result for query 2",
                    position=1,
                    source="example.com"
                )
            ]
        ]
        mock_client_class.return_value = mock_client
        
        # Mock scraper
        mock_scraper = Mock()
        mock_scraper.scrape_url.return_value = ScrapedContent(
            title="Test Content",
            url="https://example.com/test",
            source="example.com",
            content="Test content."
        )
        mock_scraper_class.return_value = mock_scraper
        
        # Execute batch scraping
        queries = ["query 1", "query 2"]
        result = batch_scrape(queries, max_results_per_query=1, parallel=False)
        
        # Verify results
        assert result.success is True
        assert result.total_queries == 2
        assert result.successful_queries == 2
        assert result.failed_queries == 0
        assert len(result.results_by_query) == 2
        
        # Verify API calls
        assert mock_client.search.call_count == 2
        mock_client.search.assert_any_call(query="query 1", search_type="web", num=1)
        mock_client.search.assert_any_call(query="query 2", search_type="web", num=1)
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_batch_scraping_with_failures(self, mock_scraper_class, mock_client_class):
        """Test batch scraping when some queries fail."""
        # Mock client setup
        mock_client = Mock()
        mock_client.search.side_effect = [
            {
                "organic": [
                    {
                        "title": "Success Result",
                        "link": "https://example.com/success",
                        "snippet": "Success",
                        "displayLink": "example.com"
                    }
                ]
            },
            SerperAPIError("API Error", 500)
        ]
        
        mock_client.parse_search_results.return_value = [
            SearchResult(
                title="Success Result",
                url="https://example.com/success",
                snippet="Success",
                position=1,
                source="example.com"
            )
        ]
        mock_client_class.return_value = mock_client
        
        # Mock scraper
        mock_scraper = Mock()
        mock_scraper.scrape_url.return_value = ScrapedContent(
            title="Test Content",
            url="https://example.com/test",
            source="example.com",
            content="Test content."
        )
        mock_scraper_class.return_value = mock_scraper
        
        # Execute batch scraping
        queries = ["success query", "failed query"]
        result = batch_scrape(queries, max_results_per_query=1, parallel=False)
        
        # Verify results
        assert result.success is True
        assert result.total_queries == 2
        assert result.successful_queries == 1
        assert result.failed_queries == 1
        assert len(result.results_by_query) == 2


class TestFunctionalConfiguration:
    """Test configuration functionality."""
    
    def test_config_environment_loading(self):
        """Test configuration loading from environment."""
        # Test with environment variables
        import os
        os.environ["ENVIRONMENT"] = "production"
        os.environ["DEBUG"] = "true"
        os.environ["SERPER_API_KEY"] = "test_key"
        
        config = Config()
        
        assert config.environment == "production"
        assert config.debug is True
        assert config.serper.api_key == "test_key"
        
        # Clean up
        del os.environ["ENVIRONMENT"]
        del os.environ["DEBUG"]
        del os.environ["SERPER_API_KEY"]
    
    def test_config_serialization(self):
        """Test configuration serialization and deserialization."""
        config = Config()
        config.environment = "test"
        config.debug = True
        config.serper.api_key = "test_key"
        
        # Test to_dict
        config_dict = config.to_dict()
        assert config_dict["environment"] == "test"
        assert config_dict["debug"] is True
        assert config_dict["serper"]["api_key"] == "test_key"
        
        # Test update_from_dict
        new_config = Config()
        new_config.update_from_dict(config_dict)
        assert new_config.environment == "test"
        assert new_config.debug is True
        assert new_config.serper.api_key == "test_key"
    
    def test_config_file_operations(self, tmp_path):
        """Test configuration file save and load."""
        import yaml
        
        config = Config()
        config.environment = "test"
        config.debug = True
        config.serper.api_key = "test_key"
        
        # Save to file
        config_file = tmp_path / "test_config.yaml"
        config.save_to_file(config_file)
        
        # Verify file exists and has correct content
        assert config_file.exists()
        with open(config_file, "r") as f:
            saved_data = yaml.safe_load(f)
        
        assert saved_data["environment"] == "test"
        assert saved_data["debug"] is True
        assert saved_data["serper"]["api_key"] == "test_key"
        
        # Load from file
        loaded_config = Config.load_from_file(config_file)
        assert loaded_config.environment == "test"
        assert loaded_config.debug is True
        assert loaded_config.serper.api_key == "test_key"


class TestFunctionalErrorHandling:
    """Test error handling functionality."""
    
    @patch('serp_forge.serper.core.SerperClient')
    def test_api_error_handling(self, mock_client_class):
        """Test handling of API errors."""
        # Mock client that raises API error
        mock_client = Mock()
        mock_client.search.side_effect = SerperAPIError("Rate limited", 429)
        mock_client_class.return_value = mock_client
        
        # Execute scraping
        result = scrape("test query", max_results=1)
        
        # Verify error handling
        assert result.success is False
        assert "Rate limited" in result.error_message
        assert result.total_results == 0
        assert result.scraped_successfully == 0
    
    @patch('serp_forge.serper.core.SerperClient')
    @patch('serp_forge.serper.core.ContentScraper')
    def test_network_error_handling(self, mock_scraper_class, mock_client_class):
        """Test handling of network errors."""
        # Mock client that raises network error
        mock_client = Mock()
        mock_client.search.side_effect = Exception("Network error")
        mock_client_class.return_value = mock_client
        
        # Execute scraping
        result = scrape("test query", max_results=1)
        
        # Verify error handling
        assert result.success is False
        assert "Network error" in result.error_message
        assert result.total_results == 0
        assert result.scraped_successfully == 0


if __name__ == "__main__":
    pytest.main([__file__]) 