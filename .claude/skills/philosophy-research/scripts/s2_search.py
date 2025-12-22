#!/usr/bin/env python3
"""
Semantic Scholar paper search with relevance ranking or bulk retrieval.

Usage:
    # Basic relevance search
    python s2_search.py "free will compatibilism" --limit 20

    # Bulk search (no ranking, up to 1000 results)
    python s2_search.py "moral responsibility" --bulk --year 2020-2024

    # Filtered search
    python s2_search.py "Frankfurt cases" --field Philosophy --min-citations 10

    # With year range
    python s2_search.py "epistemic injustice" --year 2015-2025 --limit 50

Output:
    JSON object with search results following the standard output schema.

Exit Codes:
    0: Success (results found) or partial success
    1: No results found
    2: Configuration error
    3: API error
"""

import argparse
import json
import os
import sys
from typing import Any, Optional

import requests

# Add parent directory to path for rate_limiter import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rate_limiter import ExponentialBackoff, get_limiter

# Semantic Scholar API configuration
S2_BASE_URL = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,authors,year,abstract,citationCount,externalIds,url,venue,publicationTypes,journal"


def log_progress(message: str) -> None:
    """Emit progress to stderr (visible to user, doesn't break JSON output)."""
    print(f"[s2_search.py] {message}", file=sys.stderr, flush=True)


def output_success(query: str, results: list, source: str = "semantic_scholar") -> None:
    """Output successful search results."""
    print(json.dumps({
        "status": "success",
        "source": source,
        "query": query,
        "results": results,
        "count": len(results),
        "errors": []
    }, indent=2))
    sys.exit(0)


def output_partial(query: str, results: list, errors: list, warning: str) -> None:
    """Output partial results with errors."""
    print(json.dumps({
        "status": "partial",
        "source": "semantic_scholar",
        "query": query,
        "results": results,
        "count": len(results),
        "errors": errors,
        "warning": warning
    }, indent=2))
    sys.exit(0)


def output_error(query: str, error_type: str, message: str, exit_code: int = 2) -> None:
    """Output error result."""
    print(json.dumps({
        "status": "error",
        "source": "semantic_scholar",
        "query": query,
        "results": [],
        "count": 0,
        "errors": [{"type": error_type, "message": message, "recoverable": error_type == "rate_limit"}]
    }, indent=2))
    sys.exit(exit_code)


def format_paper(paper: dict) -> dict:
    """Format S2 paper response into standard output format."""
    # Extract DOI from externalIds
    external_ids = paper.get("externalIds", {}) or {}
    doi = external_ids.get("DOI")
    arxiv_id = external_ids.get("ArXiv")

    # Format authors
    authors = []
    for author in paper.get("authors", []) or []:
        authors.append({
            "name": author.get("name", ""),
            "authorId": author.get("authorId")
        })

    return {
        "paperId": paper.get("paperId"),
        "title": paper.get("title"),
        "authors": authors,
        "year": paper.get("year"),
        "abstract": paper.get("abstract"),
        "citationCount": paper.get("citationCount"),
        "doi": doi,
        "arxivId": arxiv_id,
        "url": paper.get("url"),
        "venue": paper.get("venue"),
        "journal": paper.get("journal"),
        "publicationTypes": paper.get("publicationTypes"),
    }


def relevance_search(
    query: str,
    limit: int,
    year: Optional[str],
    field: Optional[str],
    min_citations: Optional[int],
    api_key: Optional[str],
    limiter,
    backoff: ExponentialBackoff,
    debug: bool = False
) -> list[dict]:
    """
    Perform relevance-ranked search (default mode).
    Returns up to 100 results per request.
    """
    # Build search description
    search_desc = f"'{query}'"
    if year:
        search_desc += f" (year={year})"
    if field:
        search_desc += f" (field={field})"
    if min_citations:
        search_desc += f" (min_citations={min_citations})"

    log_progress(f"Searching Semantic Scholar: {search_desc}, limit={limit}")

    url = f"{S2_BASE_URL}/paper/search"

    params = {
        "query": query,
        "fields": S2_FIELDS,
        "limit": min(limit, 100),  # API max is 100 for relevance search
    }

    if year:
        params["year"] = year
    if field:
        params["fieldsOfStudy"] = field
    if min_citations:
        params["minCitationCount"] = min_citations

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    all_results = []
    offset = 0
    errors = []

    while len(all_results) < limit:
        params["offset"] = offset
        params["limit"] = min(limit - len(all_results), 100)

        for attempt in range(backoff.max_attempts):
            limiter.wait()

            if debug:
                print(f"DEBUG: GET {url} offset={offset}", file=sys.stderr)

            try:
                response = requests.get(url, params=params, headers=headers, timeout=30)
                limiter.record()

                if debug:
                    print(f"DEBUG: Response status: {response.status_code}", file=sys.stderr)

                if response.status_code == 200:
                    data = response.json()
                    papers = data.get("data", [])

                    if not papers:
                        # No more results
                        log_progress(f"Found {len(all_results)} papers total")
                        return all_results

                    for paper in papers:
                        all_results.append(format_paper(paper))

                    # Check if there are more results
                    total = data.get("total", 0)
                    log_progress(f"Retrieved {len(all_results)}/{min(limit, total)} papers...")

                    if offset + len(papers) >= total or len(papers) < params["limit"]:
                        log_progress(f"Search complete: {len(all_results)} papers found")
                        return all_results

                    offset += len(papers)
                    break  # Success, move to next page

                elif response.status_code == 429:
                    log_progress(f"Rate limited, backing off (attempt {attempt+1}/{backoff.max_attempts})...")
                    if not backoff.wait(attempt):
                        log_progress(f"Max retries reached, returning {len(all_results)} partial results")
                        errors.append({
                            "type": "rate_limit",
                            "message": f"Rate limit exceeded at offset {offset}",
                            "recoverable": True
                        })
                        # Return partial results
                        return all_results
                    log_progress(f"Retrying after {backoff.last_delay:.1f}s backoff...")
                    continue

                elif response.status_code == 400:
                    error_msg = response.json().get("message", "Bad request")
                    raise ValueError(f"Invalid query: {error_msg}")

                else:
                    raise RuntimeError(f"S2 API error: {response.status_code}")

            except requests.exceptions.RequestException as e:
                log_progress(f"Network error: {str(e)[:100]}, retrying (attempt {attempt+1}/{backoff.max_attempts})...")
                if attempt < backoff.max_attempts - 1:
                    backoff.wait(attempt)
                    log_progress(f"Retrying after {backoff.last_delay:.1f}s backoff...")
                    continue
                log_progress(f"Max retries reached after network errors, returning {len(all_results)} partial results")
                errors.append({
                    "type": "network_error",
                    "message": str(e),
                    "recoverable": True
                })
                return all_results

    return all_results


def bulk_search(
    query: str,
    limit: int,
    year: Optional[str],
    field: Optional[str],
    min_citations: Optional[int],
    sort: Optional[str],
    api_key: Optional[str],
    limiter,
    backoff: ExponentialBackoff,
    debug: bool = False
) -> list[dict]:
    """
    Perform bulk search (no relevance ranking, up to 1000 per request).
    Supports boolean operators in query.
    """
    # Build search description
    search_desc = f"'{query}'"
    if year:
        search_desc += f" (year={year})"
    if field:
        search_desc += f" (field={field})"
    if min_citations:
        search_desc += f" (min_citations={min_citations})"

    log_progress(f"Bulk searching Semantic Scholar: {search_desc}, limit={limit}")

    url = f"{S2_BASE_URL}/paper/search/bulk"

    params = {
        "query": query,
        "fields": S2_FIELDS,
    }

    if year:
        params["year"] = year
    if field:
        params["fieldsOfStudy"] = field
    if min_citations:
        params["minCitationCount"] = min_citations
    if sort:
        params["sort"] = sort

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    all_results = []
    token = None
    errors = []

    while len(all_results) < limit:
        if token:
            params["token"] = token

        for attempt in range(backoff.max_attempts):
            limiter.wait()

            if debug:
                print(f"DEBUG: GET {url} token={token}", file=sys.stderr)

            try:
                response = requests.get(url, params=params, headers=headers, timeout=30)
                limiter.record()

                if debug:
                    print(f"DEBUG: Response status: {response.status_code}", file=sys.stderr)

                if response.status_code == 200:
                    data = response.json()
                    papers = data.get("data", [])

                    for paper in papers:
                        if len(all_results) >= limit:
                            break
                        all_results.append(format_paper(paper))

                    log_progress(f"Retrieved {len(all_results)} papers...")

                    # Check for continuation token
                    token = data.get("token")
                    if not token or len(papers) == 0:
                        log_progress(f"Bulk search complete: {len(all_results)} papers found")
                        return all_results

                    break  # Success, move to next page

                elif response.status_code == 429:
                    log_progress(f"Rate limited, backing off (attempt {attempt+1}/{backoff.max_attempts})...")
                    if not backoff.wait(attempt):
                        log_progress(f"Max retries reached, returning {len(all_results)} partial results")
                        errors.append({
                            "type": "rate_limit",
                            "message": "Rate limit exceeded during bulk search",
                            "recoverable": True
                        })
                        return all_results
                    log_progress(f"Retrying after {backoff.last_delay:.1f}s backoff...")
                    continue

                elif response.status_code == 400:
                    error_msg = response.json().get("message", "Bad request")
                    raise ValueError(f"Invalid query: {error_msg}")

                else:
                    raise RuntimeError(f"S2 API error: {response.status_code}")

            except requests.exceptions.RequestException as e:
                if attempt < backoff.max_attempts - 1:
                    backoff.wait(attempt)
                    continue
                errors.append({
                    "type": "network_error",
                    "message": str(e),
                    "recoverable": True
                })
                return all_results

    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar for papers"
    )
    parser.add_argument(
        "query",
        help="Search query string"
    )
    parser.add_argument(
        "--bulk",
        action="store_true",
        help="Use bulk search (no ranking, up to 1000 results, supports boolean operators)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of results (default: 20, max: 100 for relevance, 1000 for bulk)"
    )
    parser.add_argument(
        "--year",
        help="Year filter: YYYY or YYYY-YYYY range"
    )
    parser.add_argument(
        "--field",
        help="Field of study filter (e.g., Philosophy, Computer Science)"
    )
    parser.add_argument(
        "--min-citations",
        type=int,
        help="Minimum citation count filter"
    )
    parser.add_argument(
        "--sort",
        choices=["paperId", "publicationDate", "citationCount"],
        help="Sort order for bulk search"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("S2_API_KEY", ""),
        help="Semantic Scholar API key (default: S2_API_KEY env var)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information"
    )

    args = parser.parse_args()

    # Validate limit
    max_limit = 1000 if args.bulk else 100
    if args.limit > max_limit:
        output_error(
            args.query,
            "config_error",
            f"Limit {args.limit} exceeds maximum {max_limit} for {'bulk' if args.bulk else 'relevance'} search",
            exit_code=2
        )

    if not args.api_key and args.debug:
        print("DEBUG: S2_API_KEY not set, using unauthenticated access", file=sys.stderr)

    # Initialize rate limiter and backoff
    limiter = get_limiter("semantic_scholar")
    backoff = ExponentialBackoff(max_attempts=5)

    try:
        if args.bulk:
            results = bulk_search(
                args.query,
                args.limit,
                args.year,
                args.field,
                args.min_citations,
                args.sort,
                args.api_key,
                limiter,
                backoff,
                args.debug
            )
        else:
            results = relevance_search(
                args.query,
                args.limit,
                args.year,
                args.field,
                args.min_citations,
                args.api_key,
                limiter,
                backoff,
                args.debug
            )

        if not results:
            output_error(args.query, "not_found", "No papers found matching query", exit_code=1)

        output_success(args.query, results)

    except ValueError as e:
        output_error(args.query, "config_error", str(e), exit_code=2)

    except RuntimeError as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            output_error(args.query, "rate_limit", error_msg, exit_code=3)
        else:
            output_error(args.query, "api_error", error_msg, exit_code=3)


if __name__ == "__main__":
    main()
