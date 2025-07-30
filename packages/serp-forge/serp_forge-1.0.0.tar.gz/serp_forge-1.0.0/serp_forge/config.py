"""
Configuration management for Serp Forge.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SerperConfig(BaseSettings):
    """Serper API configuration."""
    
    api_key: Optional[str] = Field(None, description="Serper API key")
    base_url: str = Field("https://google.serper.dev", description="Serper API base URL")
    timeout: int = Field(30, description="API request timeout in seconds")
    max_requests_per_minute: int = Field(60, description="Rate limit for API requests")
    
    model_config = SettingsConfigDict(env_prefix="SERPER_")


class ScrapingConfig(BaseSettings):
    """Scraping engine configuration."""
    
    max_concurrent: int = Field(5, description="Maximum concurrent scraping requests")
    retry_attempts: int = Field(3, description="Number of retry attempts for failed requests")
    retry_delay: List[int] = Field([1, 3, 5], description="Progressive delay between retries")
    request_timeout: int = Field(15, description="HTTP request timeout in seconds")
    content_timeout: int = Field(30, description="Content extraction timeout")
    max_results_per_query: int = Field(100, description="Maximum results per search query")
    
    model_config = SettingsConfigDict(env_prefix="SCRAPING_")
    
    @field_validator("retry_delay")
    @classmethod
    def validate_retry_delay(cls, v: List[int]) -> List[int]:
        """Validate retry delay is ascending."""
        if len(v) < 1:
            raise ValueError("Retry delay must have at least one value")
        if not all(isinstance(x, int) and x >= 0 for x in v):
            raise ValueError("Retry delay values must be non-negative integers")
        return v


class AntiDetectionConfig(BaseSettings):
    """Anti-detection configuration."""
    
    rotate_headers: bool = Field(True, description="Enable header rotation")
    rotate_user_agents: bool = Field(True, description="Enable user agent rotation")
    random_delays: List[int] = Field([1, 4], description="Random delay range in seconds")
    session_rotation: bool = Field(True, description="Enable session rotation")
    cookie_handling: bool = Field(True, description="Enable cookie management")
    fingerprint_randomization: bool = Field(True, description="Enable browser fingerprint randomization")
    
    model_config = SettingsConfigDict(env_prefix="ANTI_DETECTION_")
    
    @field_validator("random_delays")
    @classmethod
    def validate_random_delays(cls, v: List[int]) -> List[int]:
        """Validate random delays has min and max values."""
        if len(v) != 2:
            raise ValueError("Random delays must have exactly 2 values [min, max]")
        if v[0] > v[1]:
            raise ValueError("Random delay min must be less than max")
        return v


class ProxyConfig(BaseSettings):
    """Proxy configuration."""
    
    enabled: bool = Field(True, description="Enable proxy usage")
    rotation_strategy: str = Field("round_robin", description="Proxy rotation strategy")
    health_check_interval: int = Field(300, description="Health check interval in seconds")
    max_failures: int = Field(5, description="Maximum failures before marking proxy as bad")
    types: List[str] = Field(["residential", "datacenter"], description="Proxy types to use")
    
    # Proxy lists
    residential_proxies: List[str] = Field(default_factory=list, description="Residential proxy list")
    datacenter_proxies: List[str] = Field(default_factory=list, description="Datacenter proxy list")
    tor_proxies: List[str] = Field(default_factory=list, description="Tor proxy list")
    
    model_config = SettingsConfigDict(env_prefix="PROXY_")
    
    @field_validator("rotation_strategy")
    @classmethod
    def validate_rotation_strategy(cls, v: str) -> str:
        """Validate rotation strategy."""
        valid_strategies = ["round_robin", "random", "weighted", "geographic"]
        if v not in valid_strategies:
            raise ValueError(f"Rotation strategy must be one of {valid_strategies}")
        return v


class ContentExtractionConfig(BaseSettings):
    """Content extraction configuration."""
    
    ai_powered: bool = Field(True, description="Enable AI-powered content extraction")
    clean_html: bool = Field(True, description="Clean HTML content")
    extract_metadata: bool = Field(True, description="Extract metadata from content")
    sentiment_analysis: bool = Field(True, description="Enable sentiment analysis")
    keyword_extraction: bool = Field(True, description="Enable keyword extraction")
    language_detection: bool = Field(True, description="Enable language detection")
    auto_summarization: bool = Field(True, description="Enable auto summarization")
    min_content_length: int = Field(100, description="Minimum content length to accept")
    max_content_length: int = Field(50000, description="Maximum content length to extract")
    
    model_config = SettingsConfigDict(env_prefix="CONTENT_EXTRACTION_")


class OutputConfig(BaseSettings):
    """Output configuration."""
    
    format: str = Field("json", description="Output format")
    include_raw_html: bool = Field(False, description="Include raw HTML in output")
    include_screenshots: bool = Field(False, description="Include screenshots in output")
    compress_large_content: bool = Field(True, description="Compress large content")
    save_to_file: bool = Field(False, description="Save results to file")
    output_directory: str = Field("./output", description="Output directory for files")
    
    model_config = SettingsConfigDict(env_prefix="OUTPUT_")
    
    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Validate output format."""
        valid_formats = ["json", "csv", "xml", "excel"]
        if v not in valid_formats:
            raise ValueError(f"Output format must be one of {valid_formats}")
        return v


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    enabled: bool = Field(False, description="Enable database storage")
    url: str = Field("sqlite:///serp_forge.db", description="Database URL")
    echo: bool = Field(False, description="Enable SQL echo")
    pool_size: int = Field(10, description="Database connection pool size")
    max_overflow: int = Field(20, description="Database max overflow")
    
    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class CacheConfig(BaseSettings):
    """Cache configuration."""
    
    enabled: bool = Field(True, description="Enable caching")
    redis_url: str = Field("redis://localhost:6379", description="Redis URL")
    ttl: int = Field(3600, description="Cache TTL in seconds")
    max_size: int = Field(1000, description="Maximum cache entries")
    
    model_config = SettingsConfigDict(env_prefix="CACHE_")


class MonitoringConfig(BaseSettings):
    """Monitoring configuration."""
    
    enabled: bool = Field(True, description="Enable monitoring")
    prometheus_port: int = Field(9090, description="Prometheus metrics port")
    log_level: str = Field("INFO", description="Logging level")
    log_format: str = Field("json", description="Log format")
    alert_webhook_url: Optional[str] = Field(None, description="Alert webhook URL")
    
    model_config = SettingsConfigDict(env_prefix="MONITORING_")
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()


class Config(BaseSettings):
    """Main configuration class."""
    
    # Environment
    environment: str = Field("development", description="Environment (development, staging, production)")
    debug: bool = Field(False, description="Enable debug mode")
    
    # Component configurations
    serper: SerperConfig = Field(default_factory=SerperConfig)
    scraping: ScrapingConfig = Field(default_factory=ScrapingConfig)
    anti_detection: AntiDetectionConfig = Field(default_factory=AntiDetectionConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    content_extraction: ContentExtractionConfig = Field(default_factory=ContentExtractionConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize configuration with environment variables."""
        super().__init__(**kwargs)
        self._load_proxy_lists()
    
    def _load_proxy_lists(self) -> None:
        """Load proxy lists from environment variables."""
        # Load from environment variables
        if proxy_list := os.getenv("SERP_FORGE_PROXY_LIST"):
            self.proxy.residential_proxies.extend(proxy_list.split(","))
        
        if user_agents_file := os.getenv("SERP_FORGE_USER_AGENTS"):
            self._load_user_agents_from_file(user_agents_file)
    
    def _load_user_agents_from_file(self, file_path: str) -> None:
        """Load user agents from file."""
        try:
            path = Path(file_path)
            if path.exists():
                with open(path, "r") as f:
                    user_agents = [line.strip() for line in f if line.strip()]
                    # Store in a way that can be accessed by the header manager
                    setattr(self, "_custom_user_agents", user_agents)
        except Exception as e:
            print(f"Warning: Could not load user agents from {file_path}: {e}")
    
    def get_custom_user_agents(self) -> List[str]:
        """Get custom user agents if loaded."""
        return getattr(self, "_custom_user_agents", [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "environment": self.environment,
            "debug": self.debug,
            "serper": self.serper.model_dump(),
            "scraping": self.scraping.model_dump(),
            "anti_detection": self.anti_detection.model_dump(),
            "proxy": self.proxy.model_dump(),
            "content_extraction": self.content_extraction.model_dump(),
            "output": self.output.model_dump(),
            "database": self.database.model_dump(),
            "cache": self.cache.model_dump(),
            "monitoring": self.monitoring.model_dump(),
        }
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in config_dict.items():
            if hasattr(self, key):
                if isinstance(value, dict) and hasattr(getattr(self, key), "model_validate"):
                    # Update nested config
                    current_config = getattr(self, key)
                    updated_config = current_config.model_validate({**current_config.model_dump(), **value})
                    setattr(self, key, updated_config)
                else:
                    setattr(self, key, value)
    
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> "Config":
        """Load configuration from YAML file."""
        import yaml
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(path, "r") as f:
            config_data = yaml.safe_load(f)
        
        return cls(**config_data)
    
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """Save configuration to YAML file."""
        import yaml
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)


# Global configuration instance
config = Config() 