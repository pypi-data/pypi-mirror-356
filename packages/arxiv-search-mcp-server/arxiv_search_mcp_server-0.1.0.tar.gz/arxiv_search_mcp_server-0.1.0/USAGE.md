# arXiv Search MCP Server - Usage Guide

This guide shows how to use the arXiv Search MCP server to find academic papers on arXiv.org.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the MCP server:**
   ```bash
   python server.py
   ```

3. **Use the server tools in your MCP client**

## Available Tools

### 1. search_arxiv_papers

Search for papers with various filtering options.

**Basic Search:**
```json
{
  "terms": "machine learning"
}
```

**Advanced Search with Filters:**
```json
{
  "terms": "quantum computing",
  "subject": "quant-ph",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "max_results": 20
}
```

**Parameters:**
- `terms` (required): Search keywords
- `subject` (optional): Subject category (see list below)
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)
- `max_results` (optional): Number of results (default: 10, max: 2000)

### 2. get_subject_categories

Get list of available subject categories for filtering.

```json
{}
```

## Subject Categories

| Code | Description |
|------|-------------|
| `physics` | Physics (general) |
| `astro-ph` | Astrophysics |
| `cond-mat` | Condensed Matter Physics |
| `gr-qc` | General Relativity and Quantum Cosmology |
| `hep-ex` | High Energy Physics - Experiment |
| `hep-lat` | High Energy Physics - Lattice |
| `hep-ph` | High Energy Physics - Phenomenology |
| `hep-th` | High Energy Physics - Theory |
| `math-ph` | Mathematical Physics |
| `nlin` | Nonlinear Sciences |
| `nucl-ex` | Nuclear Experiment |
| `nucl-th` | Nuclear Theory |
| `quant-ph` | Quantum Physics |
| `math` | Mathematics |
| `cs` | Computer Science |
| `econ` | Economics |
| `eess` | Electrical Engineering and Systems Science |
| `stat` | Statistics |
| `q-bio` | Quantitative Biology |
| `q-fin` | Quantitative Finance |

## Response Format

Each paper result includes:

```json
{
  "arxiv_id": "2301.12345",
  "title": "Paper Title Here",
  "authors": ["Author 1", "Author 2", "..."],
  "abstract": "Paper abstract text...",
  "categories": ["cs.LG", "cs.AI"],
  "published_date": "2023-01-15",
  "pdf_url": "http://arxiv.org/pdf/2301.12345v1",
  "arxiv_url": "http://arxiv.org/abs/2301.12345",
  "comment": "Additional author comments",
  "journal_ref": "Journal reference if available",
  "doi": "DOI if available"
}
```

## Example Use Cases

### Research Paper Discovery
Find recent papers in your field:
```json
{
  "terms": "neural networks deep learning",
  "subject": "cs",
  "start_date": "2024-01-01",
  "max_results": 50
}
```

### Literature Review
Search for papers on a specific topic:
```json
{
  "terms": "climate change modeling",
  "subject": "physics",
  "max_results": 100
}
```

### Following Specific Research Areas
Get latest quantum physics papers:
```json
{
  "terms": "quantum entanglement",
  "subject": "quant-ph",
  "start_date": "2024-06-01",
  "max_results": 25
}
```

## Notes

- **PDF URLs**: Every result includes a direct link to the PDF for easy download
- **Rate Limiting**: Please be respectful with API usage
- **Date Formats**: Use YYYY-MM-DD format for dates
- **Search Terms**: Can include multiple keywords, phrases in quotes
- **Result Ordering**: Results are sorted by relevance by default

## Testing

Run the test suite to verify functionality:
```bash
python test_standalone.py
```

This will test:
- Basic search functionality
- Subject category filtering
- Date range filtering
- Error handling
- Available categories listing

## Troubleshooting

### Common Issues

1. **No results found**: Try broader search terms or remove filters
2. **Network errors**: Check internet connection
3. **Invalid subject**: Use `get_subject_categories` to see valid options
4. **Date format errors**: Use YYYY-MM-DD format

### Getting Help

- Check the arXiv API documentation: https://info.arxiv.org/help/api/
- Review the test_standalone.py file for working examples
- Ensure all dependencies are installed correctly
