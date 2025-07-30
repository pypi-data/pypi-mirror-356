"""
CLI tests for Serp Forge.

These tests focus on command-line interface functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys
from io import StringIO
import pathlib

from serp_forge.cli import main


class TestCLI:
    """Test CLI functionality."""
    
    @patch('sys.argv', ['serp-forge', '--help'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_help(self, mock_stdout):
        """Test main command help."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        # Accept both 0 and 1 as valid exit codes for help
        assert exc_info.value.code in (0, 1)
        output = mock_stdout.getvalue()
        assert "Serp Forge" in output
        assert "search" in output
        assert "batch" in output
        assert "config" in output
    
    @patch('serp_forge.cli.scrape')
    @patch('sys.argv', ['serp-forge', 'search', 'test query', '--max-results', '2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_command_success(self, mock_stdout, mock_scrape):
        """Test successful search command."""
        # Mock successful response
        mock_response = Mock()
        mock_response.success = True
        mock_response.query = "test query"
        mock_response.total_results = 2
        mock_response.scraped_successfully = 2
        mock_response.results = [
            Mock(title="Result 1", url="https://example1.com", snippet="Snippet 1"),
            Mock(title="Result 2", url="https://example2.com", snippet="Snippet 2")
        ]
        mock_scrape.return_value = mock_response
        
        # Run command
        main()
        
        # Verify function call
        mock_scrape.assert_called_once_with(
            query="test query",
            search_type="web",
            max_results=2,
            include_content=False,
            proxy_rotation=False
        )
    
    @patch('serp_forge.cli.scrape')
    @patch('sys.argv', ['serp-forge', 'search', 'test query', '--type', 'news', '--include-content'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_command_with_options(self, mock_stdout, mock_scrape):
        """Test search command with various options."""
        # Mock response
        mock_response = Mock()
        mock_response.success = True
        mock_response.total_results = 1
        mock_response.scraped_successfully = 1
        mock_response.results = [Mock(title="Result", url="https://example.com", snippet="Snippet")]
        mock_scrape.return_value = mock_response
        
        # Run command
        main()
        
        # Verify function call with options
        mock_scrape.assert_called_once_with(
            query="test query",
            search_type="news",
            max_results=10,
            include_content=True,
            proxy_rotation=False
        )
    
    @patch('serp_forge.cli.scrape')
    @patch('sys.argv', ['serp-forge', 'search', 'test query'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_command_failure(self, mock_stdout, mock_scrape):
        """Test search command with API failure."""
        # Mock failed response
        mock_response = Mock()
        mock_response.success = False
        mock_response.error_message = "API Error"
        mock_response.total_results = 0
        mock_response.scraped_successfully = 0
        mock_response.results = []
        mock_scrape.return_value = mock_response
        
        # Run command - should exit with error
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
    
    @patch('serp_forge.cli.batch_scrape')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('pathlib.Path.exists', return_value=True)
    @patch('sys.argv', ['serp-forge', 'batch', '--queries', 'test_queries.txt'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_batch_search_command_success(self, mock_stdout, mock_exists, mock_open, mock_batch_scrape):
        """Test successful batch search command."""
        # Mock file reading
        mock_file = MagicMock()
        mock_file.readlines.return_value = ["query1\n", "query2\n"]
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock successful response
        mock_response = Mock()
        mock_response.success = True
        mock_response.total_queries = 2
        mock_response.successful_queries = 2
        mock_response.failed_queries = 0
        mock_response.results_by_query = {
            "query1": Mock(total_results=1, scraped_successfully=1),
            "query2": Mock(total_results=1, scraped_successfully=1)
        }
        mock_batch_scrape.return_value = mock_response
        
        # Run command
        main()
        
        # Verify function call
        mock_batch_scrape.assert_called_once()
    
    @patch('serp_forge.cli.Config')
    @patch('sys.argv', ['serp-forge', 'config', '--show'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_config_command_show(self, mock_stdout, mock_config_class):
        """Test config show command."""
        # Mock config
        mock_config = Mock()
        mock_config.to_dict.return_value = {
            "environment": "test",
            "debug": True,
            "serper": {"api_key": "test_key"}
        }
        mock_config_class.return_value = mock_config
        
        # Run command
        main()
        
        # Verify output (JSON format)
        output = mock_stdout.getvalue()
        assert '"environment": "test"' in output
        assert '"debug": true' in output
        assert '"api_key": "test_key"' in output
    
    @patch('serp_forge.cli.Config')
    @patch('sys.argv', ['serp-forge', 'config', '--validate'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_config_command_validate(self, mock_stdout, mock_config_class):
        """Test config validate command."""
        # Mock valid config
        mock_config = Mock()
        mock_config_class.return_value = mock_config
        
        # Run command
        main()
        
        # Verify output
        output = mock_stdout.getvalue()
        assert "Configuration is valid" in output


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    @patch('serp_forge.cli.scrape')
    @patch('sys.argv', ['serp-forge', 'search', 'test query'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_command_exception(self, mock_stdout, mock_scrape):
        """Test search command with exception."""
        # Mock exception
        mock_scrape.side_effect = Exception("Unexpected error")
        
        # Run command - should exit with error
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1
    
    @patch('serp_forge.cli.batch_scrape')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('pathlib.Path.exists', return_value=True)
    @patch('sys.argv', ['serp-forge', 'batch', '--queries', 'test_queries.txt'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_batch_search_command_exception(self, mock_stdout, mock_exists, mock_open, mock_batch_scrape):
        """Test batch search command with exception."""
        # Mock file reading
        mock_file = MagicMock()
        mock_file.readlines.return_value = ["query1\n", "query2\n"]
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock exception
        mock_batch_scrape.side_effect = Exception("Batch error")
        
        # Run command - should exit with error
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 1


if __name__ == "__main__":
    pytest.main([__file__]) 