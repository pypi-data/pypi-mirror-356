#!/usr/bin/env python3
"""
Test script for the arXiv Search MCP Server

This script demonstrates how to use the arXiv search functionality.
"""

import sys
import os

# Add the src directory to Python path so we can import our package
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from arxiv_search_mcp.server import search_arxiv_papers, get_subject_categories


def test_basic_search():
    """Test basic search functionality"""
    print("Testing basic search for 'quantum computing'...")
    result = search_arxiv_papers(terms="quantum computing", max_results=5)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Found {result['total_results']} total results, showing {result['returned_results']}:")
    print()
    
    for i, paper in enumerate(result["results"], 1):
        print(f"{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'])}")
        print(f"   arXiv ID: {paper['arxiv_id']}")
        print(f"   Categories: {', '.join(paper['categories'])}")
        print(f"   Published: {paper['published_date']}")
        print(f"   PDF: {paper['pdf_url']}")
        print(f"   Abstract: {paper['abstract'][:200]}...")
        print()


def test_subject_filter():
    """Test search with subject category filter"""
    print("Testing search with computer science subject filter...")
    result = search_arxiv_papers(
        terms="machine learning",
        subject="cs",
        max_results=3
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Found {result['total_results']} total results in Computer Science:")
    
    for i, paper in enumerate(result["results"], 1):
        print(f"{i}. {paper['title']}")
        print(f"   Categories: {', '.join(paper['categories'])}")
        print()


def test_date_filter():
    """Test search with date range filter"""
    print("Testing search with date range filter (2023)...")
    result = search_arxiv_papers(
        terms="neural networks",
        start_date="2023-01-01",
        end_date="2023-12-31",
        max_results=3
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Found {result['total_results']} total results from 2023:")
    
    for i, paper in enumerate(result["results"], 1):
        print(f"{i}. {paper['title']}")
        print(f"   Published: {paper['published_date']}")
        print()


def test_subject_categories():
    """Test getting available subject categories"""
    print("Testing get_subject_categories...")
    result = get_subject_categories()
    
    print(f"Available categories ({result['total_categories']}):")
    for code, description in result["categories"].items():
        print(f"  {code}: {description}")
    print()


def test_error_handling():
    """Test error handling"""
    print("Testing error handling with empty search terms...")
    result = search_arxiv_papers(terms="")
    
    if "error" in result:
        print(f"Expected error: {result['error']}")
    
    print("Testing error handling with invalid subject...")
    result = search_arxiv_papers(terms="test", subject="invalid_subject")
    
    if "error" in result:
        print(f"Expected error: {result['error']}")
    print()


if __name__ == "__main__":
    print("arXiv Search MCP Server Test Suite")
    print("=" * 50)
    print()
    
    # Run all tests
    test_subject_categories()
    test_basic_search()
    test_subject_filter() 
    test_date_filter()
    test_error_handling()
    
    print("All tests completed!")
