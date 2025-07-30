# Serp Forge 🚀

[![CI: Python Tests](https://github.com/vishal-mishra/serp-forge/actions/workflows/python-tests.yml/badge.svg)](https://github.com/vishal-mishra/serp-forge/actions/workflows/python-tests.yml)
[![PyPI version](https://badge.fury.io/py/serp-forge.svg)](https://badge.fury.io/py/serp-forge)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

> **The next-generation search & web intelligence engine for developers, analysts, and AI workflows.**

---

## 🌟 Vision & Purpose

Serp Forge empowers you to **search, extract, and analyze the world's information** with ease, speed, and stealth. Whether you're building data-driven products, monitoring trends, or fueling AI models, Serp Forge is your all-in-one toolkit for:

- **Unrestricted search** across web, news, images, and videos
- **Anti-detection scraping** with IP rotation, browser evasion, and header randomization
- **AI-powered content extraction** and sentiment/meta analysis
- **Batch, async, and high-performance workflows**
- **Rich, ready-to-use outputs** for analytics, ML, and reporting

> **Purpose:** Democratize access to web data, making advanced search and extraction accessible, ethical, and developer-friendly.

---

## 🛠️ How Serp Forge Works

```mermaid
flowchart TD
    A["User/Developer"] -->|"CLI / Python API"| B["Serp Forge"]
    B --> C["Serper API"]
    B --> D["Anti-Detection Engine"]
    B --> E["Content Extraction & AI Analysis"]
    D --> F["Proxy Rotation"]
    D --> G["Header Randomization"]
    D --> H["Browser Evasion"]
    E --> I["Text Extraction"]
    E --> J["Sentiment & Metadata"]
    E --> K["Batch & Async Processing"]
    B --> L["Rich Output: JSON, CSV, Analysis"]
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:1px
    style E fill:#bfb,stroke:#333,stroke-width:1px
```

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install serp-forge

# Or install from source
git clone https://github.com/vishal-mishra/serp-forge.git
cd serp-forge
pip install -e .
```

### Setup

```bash
# Set API key
export SERPER_API_KEY="your_api_key_here"

# Basic usage
serp-forge search "AI news 2025" --max-results 10
```

---

## 🧠 Why Serp Forge?

- **No more blocks:** Advanced anti-detection, proxy, and browser evasion built-in
- **AI-native:** Sentiment, metadata, and content extraction for downstream ML/analytics
- **Lightning fast:** Async, batch, and parallel scraping for scale
- **Developer-first:** Python API, CLI, config, and rich output formats
- **Ethical & transparent:** Designed for responsible, legal, and auditable use

---

## 🐍 Python Usage

```python
import serp_forge as sf

# Simple search and scrape
results = sf.scrape("latest AI news", max_results=10)

# News search
news = sf.scrape("blockchain technology", search_type="news", max_results=5)

# Batch processing
queries = ["AI trends", "ML news", "tech updates"]
batch_results = sf.batch_scrape(queries, parallel=True)
```

---

## ✨ Features

- 🔍 **Serper API Integration** - Get search results with full content extraction
- 🛡️ **Anti-Detection** - IP rotation, header randomization, browser fingerprinting evasion
- 🤖 **AI Content Extraction** - Intelligent content parsing and cleaning
- ⚡ **Async Support** - High-performance concurrent scraping
- 📊 **Batch Processing** - Process multiple queries efficiently
- 🎯 **Multiple Search Types** - Web, news, images, videos
- 📝 **Rich Output** - JSON, CSV, sentiment analysis, metadata extraction

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/vishal-mishra/serp-forge.git
cd serp-forge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest
```

---

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Examples](docs/USAGE.md)
- [Configuration](docs/CONFIGURATION.md)
- [API Reference](docs/API.md)
- [CLI Reference](docs/CLI.md)
- [Testing Guide](TESTING.md)

---

## 📦 PyPI Package

Serp Forge is available on PyPI: https://pypi.org/project/serp-forge/

```bash
pip install serp-forge
```

---

## 💡 License

MIT License - see [LICENSE](LICENSE) file for details. 