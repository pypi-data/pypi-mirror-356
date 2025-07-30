"""
Data models for Serper integration.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, computed_field, field_validator


class SearchResult(BaseModel):
    """Search result from Serper API."""
    
    title: str = Field(..., description="Page title")
    url: HttpUrl = Field(..., description="Page URL")
    snippet: str = Field(..., description="Page snippet/description")
    position: int = Field(..., description="Search result position")
    source: str = Field(..., description="Source domain")
    
    # Optional fields
    image_url: Optional[HttpUrl] = Field(None, description="Image URL if available")
    sitelinks: Optional[List[Dict[str, Any]]] = Field(None, description="Site links")
    date: Optional[str] = Field(None, description="Publication date")
    
    @field_validator("url", mode="before")
    @classmethod
    def normalize_url(cls, v):
        """Normalize URL by removing trailing slash."""
        if isinstance(v, str):
            return v.rstrip("/")
        return v
    
    @field_validator("position")
    @classmethod
    def validate_position(cls, v):
        """Validate position is greater than 0."""
        if v <= 0:
            raise ValueError("Position must be greater than 0")
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class ScrapedContent(BaseModel):
    """Scraped content from a webpage."""
    
    # Basic info
    title: str = Field(..., description="Page title")
    url: HttpUrl = Field(..., description="Page URL")
    source: str = Field(..., description="Source domain")
    
    # Content
    content: str = Field(..., description="Main content text")
    snippet: Optional[str] = Field(None, description="Content snippet")
    
    # Metadata
    author: Optional[str] = Field(None, description="Article author")
    publish_date: Optional[datetime] = Field(None, description="Publication date")
    last_modified: Optional[datetime] = Field(None, description="Last modified date")
    
    # Images
    images: List[Dict[str, Any]] = Field(default_factory=list, description="Page images")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    
    # AI Analysis
    sentiment: Optional[str] = Field(None, description="Content sentiment")
    sentiment_score: Optional[float] = Field(None, description="Sentiment score (-1 to 1)")
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords")
    summary: Optional[str] = Field(None, description="AI-generated summary")
    language: Optional[str] = Field(None, description="Detected language")
    
    # Quality metrics
    reading_time: Optional[str] = Field(None, description="Estimated reading time")
    quality_score: Optional[float] = Field(None, description="Content quality score (0-1)")
    
    # Technical info
    raw_html: Optional[str] = Field(None, description="Raw HTML content")
    extraction_method: str = Field("ai", description="Content extraction method used")
    confidence_score: float = Field(1.0, description="Extraction confidence (0-1)")
    
    # Scraping metadata
    scraped_at: datetime = Field(default_factory=datetime.utcnow, description="Scraping timestamp")
    proxy_used: Optional[str] = Field(None, description="Proxy used for scraping")
    user_agent: Optional[str] = Field(None, description="User agent used")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    
    @computed_field
    @property
    def word_count(self) -> int:
        """Calculate word count from content."""
        if not self.content:
            return 0
        return len(self.content.split())
    
    @field_validator("url", mode="before")
    @classmethod
    def normalize_url(cls, v):
        """Normalize URL by removing trailing slash."""
        if isinstance(v, str):
            return v.rstrip("/")
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class SearchRequest(BaseModel):
    """Search request model."""
    
    query: str = Field(..., description="Search query")
    search_type: str = Field("web", description="Search type (web, news, images, videos)")
    max_results: int = Field(10, description="Maximum number of results")
    include_content: bool = Field(True, description="Include scraped content")
    proxy_rotation: bool = Field(True, description="Enable proxy rotation")
    extract_metadata: bool = Field(True, description="Extract metadata")
    
    # Advanced options
    country: str = Field("us", description="Country code for search")
    language: str = Field("en", description="Language code")
    time_period: Optional[str] = Field(None, description="Time period filter")
    safe_search: bool = Field(True, description="Enable safe search")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class BatchSearchRequest(BaseModel):
    """Batch search request model."""
    
    queries: List[str] = Field(..., description="List of search queries")
    search_type: str = Field("web", description="Search type")
    max_results_per_query: int = Field(10, description="Max results per query")
    parallel: bool = Field(True, description="Run queries in parallel")
    save_to: Optional[str] = Field(None, description="Save results to file")
    
    # Inherit other options from SearchRequest
    include_content: bool = Field(True, description="Include scraped content")
    proxy_rotation: bool = Field(True, description="Enable proxy rotation")
    extract_metadata: bool = Field(True, description="Extract metadata")
    country: str = Field("us", description="Country code")
    language: str = Field("en", description="Language code")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class SearchResponse(BaseModel):
    """Search response model."""
    
    success: bool = Field(..., description="Request success status")
    query: str = Field(..., description="Original search query")
    total_results: int = Field(0, description="Total results found")
    scraped_successfully: int = Field(0, description="Successfully scraped results")
    execution_time: float = Field(0.0, description="Total execution time")
    
    # Results
    results: List[ScrapedContent] = Field(default_factory=list, description="Scraped results")
    failed_urls: List[str] = Field(default_factory=list, description="Failed URLs")
    
    # Statistics
    proxy_stats: Optional[Dict[str, Any]] = Field(None, description="Proxy statistics")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class BatchSearchResponse(BaseModel):
    """Batch search response model."""
    
    success: bool = Field(..., description="Overall success status")
    total_queries: int = Field(0, description="Total queries processed")
    successful_queries: int = Field(0, description="Successfully processed queries")
    failed_queries: int = Field(0, description="Failed queries")
    total_execution_time: float = Field(0.0, description="Total execution time")
    
    # Results by query
    results_by_query: Dict[str, SearchResponse] = Field(
        default_factory=dict, 
        description="Results organized by query"
    )
    
    # Summary
    total_results: int = Field(0, description="Total results across all queries")
    total_scraped: int = Field(0, description="Total successfully scraped results")
    
    # Error handling
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    batch_id: Optional[str] = Field(None, description="Batch ID for tracking")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        } 