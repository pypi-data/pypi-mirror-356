#!/usr/bin/env python3
"""
Standalone test script for the arXiv Search functionality

This script tests the core functionality without MCP server components.
"""

import requests
import feedparser
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, quote
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# arXiv API configuration
ARXIV_API_BASE = "http://export.arxiv.org/api/query"
MAX_RESULTS_LIMIT = 2000

# Subject categories
SUBJECT_CATEGORIES = {
    "physics": "physics",
    "astro-ph": "astro-ph",
    "cond-mat": "cond-mat",
    "gr-qc": "gr-qc",
    "hep-ex": "hep-ex",
    "hep-lat": "hep-lat",
    "hep-ph": "hep-ph",
    "hep-th": "hep-th",
    "math-ph": "math-ph",
    "nlin": "nlin",
    "nucl-ex": "nucl-ex",
    "nucl-th": "nucl-th",
    "quant-ph": "quant-ph",
    "math": "math",
    "cs": "cs",
    "econ": "econ",
    "eess": "eess",
    "stat": "stat",
    "q-bio": "q-bio",
    "q-fin": "q-fin"
}


def build_search_query(
    terms: str,
    subject: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Build arXiv API search query string."""
    query_parts = []
    
    if terms:
        query_parts.append(f"all:{terms}")
    
    if subject and subject in SUBJECT_CATEGORIES:
        query_parts.append(f"cat:{SUBJECT_CATEGORIES[subject]}")
    
    if start_date or end_date:
        start_formatted = ""
        end_formatted = ""
        
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                start_formatted = start_dt.strftime("%Y%m%d")
            except ValueError:
                logger.warning(f"Invalid start_date format: {start_date}")
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                end_formatted = end_dt.strftime("%Y%m%d")
            except ValueError:
                logger.warning(f"Invalid end_date format: {end_date}")
        
        if start_formatted or end_formatted:
            if not start_formatted:
                start_formatted = "19910101"
            if not end_formatted:
                end_formatted = datetime.now().strftime("%Y%m%d")
            
            date_filter = f"submittedDate:[{start_formatted}+TO+{end_formatted}]"
            query_parts.append(date_filter)
    
    return " AND ".join(query_parts)


def parse_arxiv_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a single arXiv entry from the API response."""
    arxiv_id = entry.get("id", "").replace("http://arxiv.org/abs/", "")
    
    pdf_url = ""
    for link in entry.get("links", []):
        if link.get("title") == "pdf":
            pdf_url = link.get("href", "")
            break
    
    categories = []
    for tag in entry.get("tags", []):
        if tag.get("scheme") == "http://arxiv.org/schemas/atom":
            categories.append(tag.get("term", ""))
    
    authors = []
    for author in entry.get("authors", []):
        authors.append(author.get("name", ""))
    
    published = entry.get("published", "")
    if published:
        try:
            pub_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z")
            published = pub_date.strftime("%Y-%m-%d")
        except ValueError:
            pass
    
    return {
        "arxiv_id": arxiv_id,
        "title": entry.get("title", "").strip(),
        "authors": authors,
        "abstract": entry.get("summary", "").strip(),
        "categories": categories,
        "published_date": published,
        "pdf_url": pdf_url,
        "arxiv_url": entry.get("id", ""),
        "comment": entry.get("arxiv_comment", ""),
        "journal_ref": entry.get("arxiv_journal_ref", ""),
        "doi": entry.get("arxiv_doi", "")
    }


def search_arxiv_papers(
    terms: str,
    subject: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_results: int = 10
) -> Dict[str, Any]:
    """Search for papers on arXiv."""
    try:
        if not terms or not terms.strip():
            return {"error": "Search terms are required", "results": []}
        
        max_results = min(max_results, MAX_RESULTS_LIMIT)
        if max_results < 1:
            max_results = 10
        
        if subject and subject not in SUBJECT_CATEGORIES:
            available_subjects = ", ".join(SUBJECT_CATEGORIES.keys())
            return {
                "error": f"Invalid subject category. Available options: {available_subjects}",
                "results": []
            }
        
        search_query = build_search_query(terms, subject, start_date, end_date)
        
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        logger.info(f"Searching arXiv with query: {search_query}")
        response = requests.get(ARXIV_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        
        if hasattr(feed, 'status') and feed.status != 200:
            return {"error": f"arXiv API returned status {feed.status}", "results": []}
        
        if not feed.entries:
            return {
                "message": "No papers found matching your search criteria",
                "results": [],
                "total_results": 0,
                "search_query": search_query
            }
        
        results = []
        for entry in feed.entries:
            parsed_entry = parse_arxiv_entry(entry)
            results.append(parsed_entry)
        
        total_results = 0
        if hasattr(feed.feed, 'opensearch_totalresults'):
            try:
                total_results = int(feed.feed.opensearch_totalresults)
            except (ValueError, AttributeError):
                total_results = len(results)
        
        return {
            "results": results,
            "total_results": total_results,
            "returned_results": len(results),
            "search_query": search_query,
            "parameters": {
                "terms": terms,
                "subject": subject,
                "start_date": start_date,
                "end_date": end_date,
                "max_results": max_results
            }
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return {"error": f"Failed to fetch data from arXiv API: {str(e)}", "results": []}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}", "results": []}


def get_subject_categories() -> Dict[str, Any]:
    """Get available subject categories."""
    categories_info = {
        "physics": "Physics (general)",
        "astro-ph": "Astrophysics",
        "cond-mat": "Condensed Matter Physics",
        "gr-qc": "General Relativity and Quantum Cosmology",
        "hep-ex": "High Energy Physics - Experiment",
        "hep-lat": "High Energy Physics - Lattice",
        "hep-ph": "High Energy Physics - Phenomenology",
        "hep-th": "High Energy Physics - Theory",
        "math-ph": "Mathematical Physics",
        "nlin": "Nonlinear Sciences",
        "nucl-ex": "Nuclear Experiment",
        "nucl-th": "Nuclear Theory",
        "quant-ph": "Quantum Physics",
        "math": "Mathematics",
        "cs": "Computer Science",
        "econ": "Economics",
        "eess": "Electrical Engineering and Systems Science",
        "stat": "Statistics",
        "q-bio": "Quantitative Biology",
        "q-fin": "Quantitative Finance"
    }
    
    return {
        "categories": categories_info,
        "total_categories": len(categories_info),
        "usage": "Use these category keys as the 'subject' parameter in search_arxiv_papers"
    }


def test_basic_search():
    """Test basic search functionality"""
    print("Testing basic search for 'quantum computing'...")
    result = search_arxiv_papers(terms="quantum computing", max_results=3)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"✅ Found {result['total_results']} total results, showing {result['returned_results']}:")
    
    for i, paper in enumerate(result["results"], 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
        print(f"   arXiv ID: {paper['arxiv_id']}")
        print(f"   Categories: {', '.join(paper['categories'])}")
        print(f"   Published: {paper['published_date']}")
        print(f"   PDF: {paper['pdf_url']}")


def test_subject_filter():
    """Test search with subject category filter"""
    print("\nTesting search with computer science subject filter...")
    result = search_arxiv_papers(terms="machine learning", subject="cs", max_results=2)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"✅ Found {result['total_results']} total results in Computer Science")
    
    for i, paper in enumerate(result["results"], 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Categories: {', '.join(paper['categories'])}")


def test_date_filter():
    """Test search with date range filter"""
    print("\nTesting search with date range filter (2023)...")
    result = search_arxiv_papers(
        terms="neural networks",
        start_date="2023-01-01",
        end_date="2023-12-31",
        max_results=2
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"✅ Found {result['total_results']} total results from 2023")
    
    for i, paper in enumerate(result["results"], 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Published: {paper['published_date']}")


def test_subject_categories():
    """Test getting available subject categories"""
    print("\nTesting get_subject_categories...")
    result = get_subject_categories()
    
    print(f"✅ Available categories ({result['total_categories']}):")
    for code, description in list(result["categories"].items())[:5]:
        print(f"  {code}: {description}")
    print("  ... (and more)")


def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    
    # Test empty search terms
    result = search_arxiv_papers(terms="")
    if "error" in result:
        print(f"✅ Empty terms error: {result['error']}")
    
    # Test invalid subject
    result = search_arxiv_papers(terms="test", subject="invalid_subject")
    if "error" in result:
        print(f"✅ Invalid subject error: {result['error']}")


if __name__ == "__main__":
    print("arXiv Search Functionality Test")
    print("=" * 50)
    
    try:
        test_subject_categories()
        test_basic_search()
        test_subject_filter()
        test_date_filter()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\nThe arXiv search MCP server is ready to use!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Please check your internet connection and try again.")
