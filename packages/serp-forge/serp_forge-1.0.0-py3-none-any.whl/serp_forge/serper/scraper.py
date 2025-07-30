"""
Content scraping functionality for Serp Forge.
"""

import random
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from newspaper import Article
from textblob import TextBlob
from trafilatura import extract, extract_metadata

from ..config import config
from ..utils.logging import get_logger
from .models import ScrapedContent

logger = get_logger(__name__)


class ContentScraper:
    """Content scraper with anti-detection capabilities."""
    
    def __init__(self):
        """Initialize content scraper."""
        self.user_agent = UserAgent()
        self.session = requests.Session()
        self.setup_session()
        
        # Anti-detection settings
        self.rotate_headers = config.anti_detection.rotate_headers
        self.rotate_user_agents = config.anti_detection.rotate_user_agents
        self.random_delays = config.anti_detection.random_delays
        self.session_rotation = config.anti_detection.session_rotation
        
        logger.info("Content scraper initialized")
    
    def setup_session(self) -> None:
        """Setup session with default headers."""
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent."""
        try:
            return self.user_agent.random
        except:
            # Fallback user agents
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            ]
            return random.choice(user_agents)
    
    def get_random_headers(self) -> Dict[str, str]:
        """Get random headers for anti-detection."""
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "en-GB,en;q=0.9",
                "en-CA,en;q=0.9",
                "en-AU,en;q=0.9"
            ]),
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        }
        
        # Add random referer
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://duckduckgo.com/",
        ]
        headers["Referer"] = random.choice(referers)
        
        return headers
    
    def apply_random_delay(self) -> None:
        """Apply random delay between requests."""
        if self.random_delays:
            delay = random.uniform(self.random_delays[0], self.random_delays[1])
            time.sleep(delay)
    
    def scrape_url(
        self,
        url: str,
        title: Optional[str] = None,
        source: Optional[str] = None,
        proxy_rotation: bool = True
    ) -> Optional[ScrapedContent]:
        """Scrape content from a URL.
        
        Args:
            url: URL to scrape
            title: Page title (if known)
            source: Source domain (if known)
            proxy_rotation: Whether to use proxy rotation
            
        Returns:
            ScrapedContent object or None if failed
        """
        start_time = time.time()
        
        try:
            # Apply random delay
            self.apply_random_delay()
            
            # Setup headers
            if self.rotate_headers:
                headers = self.get_random_headers()
                self.session.headers.update(headers)
            
            # Setup proxy if enabled
            proxies = None
            if proxy_rotation and config.proxy.enabled:
                proxies = self._get_proxy()
            
            # Make request
            logger.debug(f"Scraping URL: {url}")
            response = self.session.get(
                url,
                timeout=config.scraping.request_timeout,
                proxies=proxies,
                allow_redirects=True
            )
            
            response.raise_for_status()
            
            # Extract content
            content = self._extract_content(response.text, url)
            
            if not content:
                logger.warning(f"No content extracted from {url}")
                return None
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Create scraped content object
            scraped_content = ScrapedContent(
                title=content.get("title", title or ""),
                url=url,
                source=source or self._extract_domain(url),
                content=content.get("content", ""),
                snippet=content.get("snippet"),
                author=content.get("author"),
                publish_date=content.get("publish_date"),
                last_modified=content.get("last_modified"),
                images=content.get("images", []),
                featured_image=content.get("featured_image"),
                sentiment=content.get("sentiment"),
                sentiment_score=content.get("sentiment_score"),
                keywords=content.get("keywords", []),
                summary=content.get("summary"),
                language=content.get("language"),
                word_count=content.get("word_count", 0),
                reading_time=content.get("reading_time"),
                quality_score=content.get("quality_score"),
                raw_html=response.text if config.output.include_raw_html else None,
                extraction_method=content.get("extraction_method", "ai"),
                confidence_score=content.get("confidence_score", 1.0),
                proxy_used=proxies.get("http") if proxies else None,
                user_agent=self.session.headers.get("User-Agent"),
                response_time=response_time,
                status_code=response.status_code
            )
            
            logger.info(f"Successfully scraped {url} - {len(scraped_content.content)} chars")
            return scraped_content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
    
    def _extract_content(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """Extract content from HTML.
        
        Args:
            html: Raw HTML content
            url: Source URL
            
        Returns:
            Dictionary with extracted content and metadata
        """
        try:
            # Try multiple extraction methods
            content = None
            extraction_method = "unknown"
            
            # Method 1: Trafilatura (best for news/articles)
            if config.content_extraction.ai_powered:
                try:
                    content = extract(html, include_formatting=True, include_links=True)
                    if content and len(content.strip()) > 100:
                        extraction_method = "trafilatura"
                except:
                    pass
            
            # Method 2: Newspaper3k
            if not content:
                try:
                    article = Article(url)
                    article.download(input_html=html)
                    article.parse()
                    content = article.text
                    if content and len(content.strip()) > 100:
                        extraction_method = "newspaper3k"
                except:
                    pass
            
            # Method 3: BeautifulSoup fallback
            if not content:
                try:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Try to find main content
                    main_content = None
                    for tag in ['main', 'article', '[role="main"]', '.content', '.post-content']:
                        main_content = soup.select_one(tag)
                        if main_content:
                            break
                    
                    if not main_content:
                        main_content = soup.find('body')
                    
                    if main_content:
                        content = main_content.get_text(separator=' ', strip=True)
                        extraction_method = "beautifulsoup"
                except:
                    pass
            
            if not content:
                return None
            
            # Clean content
            content = self._clean_content(content)
            
            # Extract metadata
            metadata = self._extract_metadata(html, url)
            
            # AI analysis
            ai_analysis = self._analyze_content(content)
            
            # Calculate quality metrics
            word_count = len(content.split())
            reading_time = f"{max(1, word_count // 200)} min"
            quality_score = self._calculate_quality_score(content, metadata)
            
            return {
                "content": content,
                "title": metadata.get("title"),
                "author": metadata.get("author"),
                "publish_date": metadata.get("publish_date"),
                "last_modified": metadata.get("last_modified"),
                "images": metadata.get("images", []),
                "featured_image": metadata.get("featured_image"),
                "snippet": content[:200] + "..." if len(content) > 200 else content,
                "extraction_method": extraction_method,
                "confidence_score": quality_score,
                "word_count": word_count,
                "reading_time": reading_time,
                "quality_score": quality_score,
                **ai_analysis
            }
            
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return None
    
    def _clean_content(self, content: str) -> str:
        """Clean extracted content.
        
        Args:
            content: Raw content text
            
        Returns:
            Cleaned content
        """
        if not content:
            return ""
        
        # Remove extra whitespace
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        content = ' '.join(lines)
        
        # Remove multiple spaces
        import re
        content = re.sub(r'\s+', ' ', content)
        
        # Truncate if too long
        max_length = config.content_extraction.max_content_length
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        return content.strip()
    
    def _extract_metadata(self, html: str, url: str) -> Dict[str, Any]:
        """Extract metadata from HTML.
        
        Args:
            html: Raw HTML content
            url: Source URL
            
        Returns:
            Dictionary with metadata
        """
        metadata = {}
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                metadata["title"] = title_tag.get_text().strip()
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata["description"] = meta_desc.get('content', '').strip()
            
            # Extract author
            author_meta = soup.find('meta', attrs={'name': 'author'})
            if author_meta:
                metadata["author"] = author_meta.get('content', '').strip()
            
            # Extract publish date
            date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
            if date_meta:
                metadata["publish_date"] = date_meta.get('content', '').strip()
            
            # Extract images
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    images.append({
                        "src": src,
                        "alt": img.get('alt', ''),
                        "title": img.get('title', '')
                    })
            
            metadata["images"] = images
            
            # Extract featured image
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            if og_image:
                metadata["featured_image"] = og_image.get('content', '').strip()
            
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {e}")
        
        return metadata
    
    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze content using AI/NLP techniques.
        
        Args:
            content: Content text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {}
        
        try:
            # Sentiment analysis
            if config.content_extraction.sentiment_analysis:
                blob = TextBlob(content)
                analysis["sentiment_score"] = blob.sentiment.polarity
                
                if blob.sentiment.polarity > 0.1:
                    analysis["sentiment"] = "positive"
                elif blob.sentiment.polarity < -0.1:
                    analysis["sentiment"] = "negative"
                else:
                    analysis["sentiment"] = "neutral"
            
            # Keyword extraction
            if config.content_extraction.keyword_extraction:
                blob = TextBlob(content)
                # Simple keyword extraction based on frequency
                words = [word.lower() for word in blob.words if len(word) > 3]
                word_freq = {}
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
                
                # Get top keywords
                keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
                analysis["keywords"] = [word for word, freq in keywords]
            
            # Language detection
            if config.content_extraction.language_detection:
                blob = TextBlob(content)
                analysis["language"] = blob.detect_language()
            
            # Auto summarization
            if config.content_extraction.auto_summarization:
                sentences = content.split('.')
                if len(sentences) > 3:
                    # Simple extractive summarization
                    summary_sentences = sentences[:3]
                    analysis["summary"] = '. '.join(summary_sentences) + '.'
            
        except Exception as e:
            logger.warning(f"Content analysis failed: {e}")
        
        return analysis
    
    def _calculate_quality_score(self, content: str, metadata: Dict[str, Any]) -> float:
        """Calculate content quality score.
        
        Args:
            content: Content text
            metadata: Extracted metadata
            
        Returns:
            Quality score between 0 and 1
        """
        score = 0.5  # Base score
        
        # Length factor
        if len(content) > 500:
            score += 0.2
        elif len(content) > 200:
            score += 0.1
        
        # Metadata factor
        if metadata.get("title"):
            score += 0.1
        if metadata.get("author"):
            score += 0.1
        if metadata.get("publish_date"):
            score += 0.1
        
        # Content structure factor
        if '.' in content and len(content.split('.')) > 5:
            score += 0.1
        
        return min(1.0, score)
    
    def _get_proxy(self) -> Optional[Dict[str, str]]:
        """Get a proxy for requests.
        
        Returns:
            Proxy configuration or None
        """
        # Simple proxy selection - in a real implementation, you'd have a proxy manager
        if config.proxy.residential_proxies:
            proxy = random.choice(config.proxy.residential_proxies)
            return {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        elif config.proxy.datacenter_proxies:
            proxy = random.choice(config.proxy.datacenter_proxies)
            return {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        
        return None
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL.
        
        Args:
            url: URL to extract domain from
            
        Returns:
            Domain name
        """
        try:
            return urlparse(url).netloc
        except:
            return "unknown"
    
    def close(self) -> None:
        """Close the scraper session."""
        if hasattr(self, 'session'):
            self.session.close() 