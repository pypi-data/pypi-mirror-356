"""
Command-line interface for Serp Forge.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .config import Config
from .serper import scrape, batch_scrape
from .utils.logging import setup_logging, get_logger

logger = get_logger(__name__)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Serp Forge - Advanced Web Scraping Solution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  serp-forge search "AI news 2025" --max-results 10
  serp-forge news "blockchain technology" --include-content
  serp-forge batch --queries queries.txt --save-to results.json
  serp-forge config --show
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search and scrape content")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--type", choices=["web", "news", "images", "videos"], 
                              default="web", help="Search type")
    search_parser.add_argument("--max-results", type=int, default=10, 
                              help="Maximum number of results")
    search_parser.add_argument("--include-content", action="store_true", 
                              help="Include scraped content")
    search_parser.add_argument("--proxy-rotation", action="store_true", 
                              help="Enable proxy rotation")
    search_parser.add_argument("--output", help="Output file path")
    search_parser.add_argument("--format", choices=["json", "csv"], default="json",
                              help="Output format")
    
    # News command
    news_parser = subparsers.add_parser("news", help="Search for news articles")
    news_parser.add_argument("query", help="News search query")
    news_parser.add_argument("--max-results", type=int, default=10, 
                            help="Maximum number of results")
    news_parser.add_argument("--include-content", action="store_true", 
                            help="Include scraped content")
    news_parser.add_argument("--output", help="Output file path")
    
    # Images command
    images_parser = subparsers.add_parser("images", help="Search for images")
    images_parser.add_argument("query", help="Image search query")
    images_parser.add_argument("--max-results", type=int, default=10, 
                              help="Maximum number of results")
    images_parser.add_argument("--output", help="Output file path")
    
    # Videos command
    videos_parser = subparsers.add_parser("videos", help="Search for videos")
    videos_parser.add_argument("query", help="Video search query")
    videos_parser.add_argument("--max-results", type=int, default=10, 
                              help="Maximum number of results")
    videos_parser.add_argument("--output", help="Output file path")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch processing")
    batch_parser.add_argument("--queries", required=True, 
                             help="File containing queries (one per line)")
    batch_parser.add_argument("--type", choices=["web", "news", "images", "videos"], 
                             default="web", help="Search type")
    batch_parser.add_argument("--max-results-per-query", type=int, default=10,
                             help="Maximum results per query")
    batch_parser.add_argument("--parallel", action="store_true", 
                             help="Run queries in parallel")
    batch_parser.add_argument("--save-to", help="Output file path")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_parser.add_argument("--show", action="store_true", 
                              help="Show current configuration")
    config_parser.add_argument("--load", help="Load configuration from file")
    config_parser.add_argument("--save", help="Save configuration to file")
    config_parser.add_argument("--validate", action="store_true", 
                              help="Validate configuration")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    try:
        if args.command == "search":
            handle_search(args)
        elif args.command == "news":
            handle_news(args)
        elif args.command == "images":
            handle_images(args)
        elif args.command == "videos":
            handle_videos(args)
        elif args.command == "batch":
            handle_batch(args)
        elif args.command == "config":
            handle_config(args)
        elif args.command == "version":
            handle_version(args)
        else:
            logger.error(f"Unknown command: {args.command}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def handle_search(args) -> None:
    """Handle search command."""
    logger.info(f"Searching for: {args.query}")
    
    result = scrape(
        query=args.query,
        search_type=args.type,
        max_results=args.max_results,
        include_content=args.include_content,
        proxy_rotation=args.proxy_rotation
    )
    
    if result.success:
        logger.info(f"Search completed: {result.scraped_successfully}/{result.total_results} results scraped")
        output_results(result, args.output, args.format)
    else:
        logger.error(f"Search failed: {result.error_message}")
        sys.exit(1)


def handle_news(args) -> None:
    """Handle news command."""
    logger.info(f"Searching for news: {args.query}")
    
    result = scrape(
        query=args.query,
        search_type="news",
        max_results=args.max_results,
        include_content=args.include_content
    )
    
    if result.success:
        logger.info(f"News search completed: {result.scraped_successfully}/{result.total_results} results scraped")
        output_results(result, args.output, "json")
    else:
        logger.error(f"News search failed: {result.error_message}")
        sys.exit(1)


def handle_images(args) -> None:
    """Handle images command."""
    logger.info(f"Searching for images: {args.query}")
    
    result = scrape(
        query=args.query,
        search_type="images",
        max_results=args.max_results
    )
    
    if result.success:
        logger.info(f"Image search completed: {result.total_results} results found")
        output_results(result, args.output, "json")
    else:
        logger.error(f"Image search failed: {result.error_message}")
        sys.exit(1)


def handle_videos(args) -> None:
    """Handle videos command."""
    logger.info(f"Searching for videos: {args.query}")
    
    result = scrape(
        query=args.query,
        search_type="videos",
        max_results=args.max_results
    )
    
    if result.success:
        logger.info(f"Video search completed: {result.total_results} results found")
        output_results(result, args.output, "json")
    else:
        logger.error(f"Video search failed: {result.error_message}")
        sys.exit(1)


def handle_batch(args) -> None:
    """Handle batch command."""
    # Read queries from file
    queries_file = Path(args.queries)
    if not queries_file.exists():
        logger.error(f"Queries file not found: {args.queries}")
        sys.exit(1)
    
    with open(queries_file, 'r') as f:
        queries = [line.strip() for line in f if line.strip()]
    
    logger.info(f"Batch processing {len(queries)} queries")
    
    result = batch_scrape(
        queries=queries,
        search_type=args.type,
        max_results_per_query=args.max_results_per_query,
        parallel=args.parallel,
        save_to=args.save_to
    )
    
    if result.success:
        logger.info(f"Batch processing completed: {result.successful_queries}/{result.total_queries} queries successful")
        if not args.save_to:
            output_results(result, None, "json")
    else:
        logger.error(f"Batch processing failed: {result.error_message}")
        sys.exit(1)


def handle_config(args) -> None:
    """Handle config command."""
    config = Config()
    
    if args.show:
        print("Current Configuration:")
        print(json.dumps(config.to_dict(), indent=2, default=str))
    
    elif args.load:
        try:
            config = Config.load_from_file(args.load)
            print(f"Configuration loaded from: {args.load}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)
    
    elif args.save:
        try:
            config.save_to_file(args.save)
            print(f"Configuration saved to: {args.save}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            sys.exit(1)
    
    elif args.validate:
        try:
            # Config validation happens during initialization
            print("Configuration is valid")
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            sys.exit(1)
    
    else:
        print("Configuration Management:")
        print("  --show     Show current configuration")
        print("  --load     Load configuration from file")
        print("  --save     Save configuration to file")
        print("  --validate Validate configuration")


def handle_version(args) -> None:
    """Handle version command."""
    from . import __version__, __author__, __email__
    
    print(f"Serp Forge v{__version__}")
    print(f"Author: {__author__}")
    print(f"Email: {__email__}")


def output_results(result, output_file: Optional[str], format_type: str) -> None:
    """Output results to file or stdout.
    
    Args:
        result: Search result
        output_file: Output file path (None for stdout)
        format_type: Output format (json, csv)
    """
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format_type == "json":
            with open(output_path, 'w') as f:
                json.dump(result.model_dump(), f, indent=2, default=str)
        elif format_type == "csv":
            import csv
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Title', 'URL', 'Source', 'Content', 'Author', 'Publish Date'])
                # Write data
                for item in result.results:
                    writer.writerow([
                        item.title,
                        item.url,
                        item.source,
                        item.content[:200] + "..." if len(item.content) > 200 else item.content,
                        item.author or "",
                        item.publish_date or ""
                    ])
        
        logger.info(f"Results saved to: {output_file}")
    else:
        # Output to stdout
        if format_type == "json":
            print(json.dumps(result.model_dump(), indent=2, default=str))
        else:
            # Simple text output
            print(f"\nSearch Results for: {result.query}")
            print(f"Total Results: {result.total_results}")
            print(f"Scraped Successfully: {result.scraped_successfully}")
            print(f"Execution Time: {result.execution_time:.2f}s")
            print("\n" + "="*50)
            
            for i, item in enumerate(result.results, 1):
                print(f"\n{i}. {item.title}")
                print(f"   URL: {item.url}")
                print(f"   Source: {item.source}")
                if item.author:
                    print(f"   Author: {item.author}")
                if item.publish_date:
                    print(f"   Date: {item.publish_date}")
                print(f"   Content: {item.content[:200]}...")
                print("-" * 30)


if __name__ == "__main__":
    main() 