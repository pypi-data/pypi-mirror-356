"""
Serp Forge - Advanced Web Scraping Solution

A foolproof, production-ready web scraping solution powered by Serper API
with advanced anti-detection capabilities, IP rotation, and intelligent content extraction.
"""

__version__ = "0.1.0"
__author__ = "Serp Forge Team"
__email__ = "team@serp-forge.com"

from .config import Config
from .serper import scrape, batch_scrape

__all__ = [
    "Config",
    "scrape", 
    "batch_scrape",
    "__version__",
    "__author__",
    "__email__",
] 