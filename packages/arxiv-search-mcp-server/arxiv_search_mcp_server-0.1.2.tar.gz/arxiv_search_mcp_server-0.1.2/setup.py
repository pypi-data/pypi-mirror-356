#!/usr/bin/env python3
"""Setup script for arxiv-search-mcp package."""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="arxiv-search-mcp-server",
    version="0.1.2",
    author="Gavin Huang",
    author_email="gavin@example.com",  # Replace with your actual email
    description="An MCP server that provides search functionality for arXiv.org papers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gavinHuang/arxiv-search-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/gavinHuang/arxiv-search-mcp/issues",
        "Documentation": "https://github.com/gavinHuang/arxiv-search-mcp/blob/main/README.md",
        "Source Code": "https://github.com/gavinHuang/arxiv-search-mcp",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
    },    entry_points={
        "console_scripts": [
            "arxiv-search-mcp-server=arxiv_search_mcp_server.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
