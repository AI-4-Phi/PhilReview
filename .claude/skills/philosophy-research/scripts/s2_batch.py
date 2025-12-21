#!/usr/bin/env python3
"""
Batch fetch paper details for multiple IDs from Semantic Scholar.

Usage:
    # Comma-separated IDs
    python s2_batch.py --ids "DOI:10.2307/2024717,CorpusId:123,DOI:10.1111/j.1933-1592.2004.tb00342.x"

    # From file (one ID per line)
    python s2_batch.py --file paper_ids.txt

    # With custom fields
    python s2_batch.py --ids "DOI:10.xxx" --fields "paperId,title,authors,abstract"

Paper ID formats:
    - DOI:10.xxx/xxx
    - CorpusId:12345
    - ARXIV:2301.00001
    - PMID:12345678
    - URL:https://...
    - Raw Semantic Scholar paper ID

Output:
    JSON object with paper details for each ID.

Exit Codes:
    0: Success (at least some papers found)
    1: No papers found
    2: Configuration error
    3: API error
"""

import argparse
import json
import os
import sys
from typing import Optional

import requests

# Add parent directory to path for rate_limiter import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rate_limiter import ExponentialBackoff, get_limiter

# Semantic Scholar API configuration
S2_BASE_URL = "https://api.semanticscholar.org/graph/v1"
S2_DEFAULT_FIELDS = "paperId,title,authors,year,abstract,citationCount,externalIds,url,venue,publicationTypes,journal"


def output_success(query: str, results: list, not_found: list = None) -> None:
    """Output successful batch results."""
    output = {
        "status": "success",
        "source": "semantic_scholar",
        "query": query,
        "results": results,
        "count": len(results),
        "errors": []
    }
    if not_found:
        output["not_found"] = not_found
    print(json.dumps(output, indent=2))
    sys.exit(0)


def output_partial(query: str, results: list, errors: list, warning: str, not_found: list = None) -> None:
    """Output partial results with errors."""
    output = {
        "status": "partial",
        "source": "semantic_scholar",
        "query": query,
        "results": results,
        "count": len(results),
        "errors": errors,
        "warning": warning
    }
    if not_found:
        output["not_found"] = not_found
    print(json.dumps(output, indent=2))
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
    if not paper:
        return None

    external_ids = paper.get("externalIds", {}) or {}
    doi = external_ids.get("DOI")
    arxiv_id = external_ids.get("ArXiv")

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


def batch_fetch(
    paper_ids: list[str],
    fields: str,
    api_key: Optional[str],
    limiter,
    backoff: ExponentialBackoff,
    debug: bool = False
) -> tuple[list[dict], list[str], list[dict]]:
    """
    Fetch paper details for multiple IDs in a single request.

    Args:
        paper_ids: List of paper identifiers (max 500)
        fields: Comma-separated fields to retrieve
        api_key: Optional API key
        limiter: Rate limiter instance
        backoff: Backoff configuration
        debug: Enable debug output

    Returns:
        Tuple of (results, not_found_ids, errors)
    """
    url = f"{S2_BASE_URL}/paper/batch"
    params = {"fields": fields}

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    body = {"ids": paper_ids}

    results = []
    not_found = []
    errors = []

    for attempt in range(backoff.max_attempts):
        limiter.wait()

        if debug:
            print(f"DEBUG: POST {url} with {len(paper_ids)} IDs", file=sys.stderr)

        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=body,
                timeout=60  # Longer timeout for batch
            )
            limiter.record()

            if debug:
                print(f"DEBUG: Response status: {response.status_code}", file=sys.stderr)

            if response.status_code == 200:
                data = response.json()

                # Response is a list matching input order
                # None values indicate not found
                for i, paper in enumerate(data):
                    if paper is None:
                        not_found.append(paper_ids[i])
                    else:
                        formatted = format_paper(paper)
                        if formatted:
                            # Add the original query ID for reference
                            formatted["_queryId"] = paper_ids[i]
                            results.append(formatted)

                return results, not_found, errors

            elif response.status_code == 429:
                if not backoff.wait(attempt):
                    errors.append({
                        "type": "rate_limit",
                        "message": "Rate limit exceeded during batch fetch",
                        "recoverable": True
                    })
                    return results, not_found, errors
                continue

            elif response.status_code == 400:
                error_msg = response.json().get("message", "Bad request")
                raise ValueError(f"Invalid request: {error_msg}")

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
            return results, not_found, errors

    errors.append({
        "type": "max_retries",
        "message": "Maximum retries exceeded",
        "recoverable": True
    })
    return results, not_found, errors


def main():
    parser = argparse.ArgumentParser(
        description="Batch fetch paper details from Semantic Scholar"
    )
    parser.add_argument(
        "--ids",
        help="Comma-separated paper IDs"
    )
    parser.add_argument(
        "--file",
        help="File with paper IDs (one per line)"
    )
    parser.add_argument(
        "--fields",
        default=S2_DEFAULT_FIELDS,
        help=f"Comma-separated fields to retrieve (default: {S2_DEFAULT_FIELDS})"
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

    # Get paper IDs from args
    paper_ids = []

    if args.ids:
        paper_ids = [id.strip() for id in args.ids.split(",") if id.strip()]

    if args.file:
        try:
            with open(args.file, "r") as f:
                file_ids = [line.strip() for line in f if line.strip()]
                paper_ids.extend(file_ids)
        except FileNotFoundError:
            output_error(
                args.ids or args.file,
                "config_error",
                f"File not found: {args.file}",
                exit_code=2
            )
        except Exception as e:
            output_error(
                args.ids or args.file,
                "config_error",
                f"Error reading file: {e}",
                exit_code=2
            )

    if not paper_ids:
        output_error(
            "",
            "config_error",
            "Must provide paper IDs via --ids or --file",
            exit_code=2
        )

    # Check limit
    if len(paper_ids) > 500:
        output_error(
            f"{len(paper_ids)} IDs",
            "config_error",
            f"Too many IDs ({len(paper_ids)}). Maximum is 500 per batch.",
            exit_code=2
        )

    query_str = f"{len(paper_ids)} paper IDs"

    # Initialize rate limiter and backoff
    limiter = get_limiter("semantic_scholar")
    backoff = ExponentialBackoff(max_attempts=5)

    try:
        results, not_found, errors = batch_fetch(
            paper_ids,
            args.fields,
            args.api_key,
            limiter,
            backoff,
            args.debug
        )

        if args.debug:
            print(f"DEBUG: Found {len(results)}, not found {len(not_found)}", file=sys.stderr)

        if not results and not errors:
            output_error(query_str, "not_found", "No papers found for any of the provided IDs", exit_code=1)

        if errors:
            warning = f"Completed with {len(errors)} error(s). Found {len(results)} papers, {len(not_found)} not found."
            output_partial(query_str, results, errors, warning, not_found if not_found else None)
        else:
            output_success(query_str, results, not_found if not_found else None)

    except ValueError as e:
        output_error(query_str, "config_error", str(e), exit_code=2)

    except RuntimeError as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            output_error(query_str, "rate_limit", error_msg, exit_code=3)
        else:
            output_error(query_str, "api_error", error_msg, exit_code=3)


if __name__ == "__main__":
    main()
