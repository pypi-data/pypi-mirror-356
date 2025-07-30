#!/usr/bin/env python3
"""
Setup script for Serp Forge.
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="serp-forge",
    version="1.0.0",
    author="Serp Forge Team",
    author_email="team@serp-forge.com",
    description="Advanced web scraping solution powered by Serper API with anti-detection capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishalm/serp-forge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
            "plotly>=5.15.0",
            "pandas>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "serp-forge=serp_forge.cli:main",
        ],
    },
    package_data={
        "serp_forge": ["*.yaml", "*.yml", "*.json"],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/vishalm/serp-forge/issues",
        "Source": "https://github.com/vishalm/serp-forge",
        "Documentation": "https://serp-forge.readthedocs.io",
    },
) 