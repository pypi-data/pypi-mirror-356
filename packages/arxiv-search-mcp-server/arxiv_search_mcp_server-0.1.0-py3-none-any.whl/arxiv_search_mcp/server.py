#!/usr/bin/env python3
"""
arXiv Search MCP Server

An MCP server that provides search functionality for arXiv.org papers using the arXiv API.
Supports searching by terms, subject categories, date ranges, and result count limits.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, quote
import xml.etree.ElementTree as ET
import requests
import feedparser
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("arXiv Search")

# arXiv API configuration
ARXIV_API_BASE = "http://export.arxiv.org/api/query"
MAX_RESULTS_LIMIT = 2000  # arXiv API limit per request

# Subject category mappings based on arXiv taxonomy
SUBJECT_CATEGORIES = {
    # Physics
    "physics": "physics",
    "astro-ph": "astro-ph",  # Astrophysics
    "cond-mat": "cond-mat",  # Condensed Matter
    "gr-qc": "gr-qc",        # General Relativity and Quantum Cosmology
    "hep-ex": "hep-ex",      # High Energy Physics - Experiment
    "hep-lat": "hep-lat",    # High Energy Physics - Lattice
    "hep-ph": "hep-ph",      # High Energy Physics - Phenomenology
    "hep-th": "hep-th",      # High Energy Physics - Theory
    "math-ph": "math-ph",    # Mathematical Physics
    "nlin": "nlin",          # Nonlinear Sciences
    "nucl-ex": "nucl-ex",    # Nuclear Experiment
    "nucl-th": "nucl-th",    # Nuclear Theory
    "quant-ph": "quant-ph",  # Quantum Physics
    
    # Mathematics
    "math": "math",
    
    # Computer Science
    "cs": "cs",
    
    # Economics
    "econ": "econ",
    
    # Electrical Engineering and Systems Science
    "eess": "eess",
    
    # Statistics
    "stat": "stat",
    
    # Quantitative Biology
    "q-bio": "q-bio",
    
    # Quantitative Finance
    "q-fin": "q-fin"
}


def build_search_query(
    terms: str,
    subject: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Build arXiv API search query string.
    
    Args:
        terms: Search terms (required)
        subject: Subject category (optional)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    
    Returns:
        Formatted search query string
    """
    query_parts = []
    
    # Add search terms (search in all fields)
    if terms:
        query_parts.append(f"all:{terms}")
    
    # Add subject category filter
    if subject and subject in SUBJECT_CATEGORIES:
        query_parts.append(f"cat:{SUBJECT_CATEGORIES[subject]}")
    
    # Add date range filter if provided
    if start_date or end_date:
        # Convert dates to arXiv format YYYYMMDD
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
                start_formatted = "19910101"  # arXiv started in 1991
            if not end_formatted:
                end_formatted = datetime.now().strftime("%Y%m%d")
            
            date_filter = f"submittedDate:[{start_formatted}+TO+{end_formatted}]"
            query_parts.append(date_filter)
    
    return " AND ".join(query_parts)


def parse_arxiv_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a single arXiv entry from the API response.
    
    Args:
        entry: Raw entry from feedparser
    
    Returns:
        Parsed paper information
    """
    # Extract arXiv ID from the entry id
    arxiv_id = entry.get("id", "").replace("http://arxiv.org/abs/", "")
    
    # Extract PDF URL
    pdf_url = ""
    for link in entry.get("links", []):
        if link.get("title") == "pdf":
            pdf_url = link.get("href", "")
            break
    
    # Extract categories
    categories = []
    for tag in entry.get("tags", []):
        if tag.get("scheme") == "http://arxiv.org/schemas/atom":
            categories.append(tag.get("term", ""))
    
    # Extract authors
    authors = []
    for author in entry.get("authors", []):
        authors.append(author.get("name", ""))
    
    # Extract publication date
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


@mcp.tool()
def search_arxiv_papers(
    terms: str,
    subject: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search for papers on arXiv.org.
    
    Args:
        terms: Search terms to look for in paper titles, abstracts, and content (required)
        subject: Subject category to filter by (optional). Valid options include:
                physics, astro-ph, cond-mat, gr-qc, hep-ex, hep-lat, hep-ph, hep-th,
                math-ph, nlin, nucl-ex, nucl-th, quant-ph, math, cs, econ, eess,
                stat, q-bio, q-fin
        start_date: Start date for filtering papers in YYYY-MM-DD format (optional)
        end_date: End date for filtering papers in YYYY-MM-DD format (optional)
        max_results: Maximum number of results to return (default: 10, max: 2000)
    
    Returns:
        Dictionary containing search results with paper details including PDF URLs
    """
    try:
        # Validate inputs
        if not terms or not terms.strip():
            return {
                "error": "Search terms are required",
                "results": []
            }
        
        # Limit max_results
        max_results = min(max_results, MAX_RESULTS_LIMIT)
        if max_results < 1:
            max_results = 10
        
        # Validate subject category
        if subject and subject not in SUBJECT_CATEGORIES:
            available_subjects = ", ".join(SUBJECT_CATEGORIES.keys())
            return {
                "error": f"Invalid subject category. Available options: {available_subjects}",
                "results": []
            }
        
        # Build search query
        search_query = build_search_query(terms, subject, start_date, end_date)
        
        # Prepare API request parameters
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        # Make API request
        logger.info(f"Searching arXiv with query: {search_query}")
        response = requests.get(ARXIV_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse response using feedparser
        feed = feedparser.parse(response.content)
        
        # Check for errors in the response
        if hasattr(feed, 'status') and feed.status != 200:
            return {
                "error": f"arXiv API returned status {feed.status}",
                "results": []
            }
        
        # Check if any results were found
        if not feed.entries:
            return {
                "message": "No papers found matching your search criteria",
                "results": [],
                "total_results": 0,
                "search_query": search_query
            }
        
        # Parse results
        results = []
        for entry in feed.entries:
            parsed_entry = parse_arxiv_entry(entry)
            results.append(parsed_entry)
        
        # Get total results count from OpenSearch elements
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
        return {
            "error": f"Failed to fetch data from arXiv API: {str(e)}",
            "results": []
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "results": []
        }


@mcp.tool()
def get_subject_categories() -> Dict[str, Any]:
    """
    Get available subject categories for arXiv search.
    
    Returns:
        Dictionary containing all available subject categories and their descriptions
    """
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


def main():
    """Main entry point for the CLI script."""
    mcp.run()


if __name__ == "__main__":
    main()
