#!/usr/bin/env python3
"""
Get paper recommendations from Semantic Scholar based on seed papers.

Usage:
    # Recommendations based on positive examples
    python s2_recommend.py --positive "DOI:10.2307/2024717,DOI:10.1111/j.1933-1592.2004.tb00342.x"

    # With negative examples (papers to avoid similarity to)
    python s2_recommend.py --positive "DOI:10.xxx" --negative "DOI:10.yyy" --limit 50

    # Single paper recommendations
    python s2_recommend.py --for-paper "DOI:10.2307/2024717"

Paper ID formats:
    - DOI:10.xxx/xxx
    - CorpusId:12345
    - ARXIV:2301.00001
    - URL:https://...
    - Raw Semantic Scholar paper ID

Output:
    JSON object with recommended papers.

Exit Codes:
    0: Success
    1: No recommendations found
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
S2_RECOMMEND_URL = "https://api.semanticscholar.org/recommendations/v1/papers"
S2_FIELDS = "paperId,title,authors,year,abstract,citationCount,externalIds,url,venue"


def output_success(query: str, results: list) -> None:
    """Output successful recommendation results."""
    print(json.dumps({
        "status": "success",
        "source": "semantic_scholar",
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
    }


def get_batch_recommendations(
    positive_ids: list[str],
    negative_ids: list[str],
    limit: int,
    api_key: Optional[str],
    limiter,
    backoff: ExponentialBackoff,
    debug: bool = False
) -> tuple[list[dict], list[dict]]:
    """
    Get recommendations based on positive and negative paper examples.

    Returns:
        Tuple of (results, errors)
    """
    url = f"{S2_RECOMMEND_URL}/"
    params = {
        "fields": S2_FIELDS,
        "limit": min(limit, 500),
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    body = {
        "positivePaperIds": positive_ids,
    }
    if negative_ids:
        body["negativePaperIds"] = negative_ids

    results = []
    errors = []

    for attempt in range(backoff.max_attempts):
        limiter.wait()

        if debug:
            print(f"DEBUG: POST {url}", file=sys.stderr)
            print(f"DEBUG: Body: {body}", file=sys.stderr)

        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=body,
                timeout=30
            )
            limiter.record()

            if debug:
                print(f"DEBUG: Response status: {response.status_code}", file=sys.stderr)

            if response.status_code == 200:
                data = response.json()
                papers = data.get("recommendedPapers", [])

                for paper in papers:
                    results.append(format_paper(paper))

                return results, errors

            elif response.status_code == 429:
                if not backoff.wait(attempt):
                    errors.append({
                        "type": "rate_limit",
                        "message": "Rate limit exceeded",
                        "recoverable": True
                    })
                    return results, errors
                continue

            elif response.status_code == 400:
                error_msg = response.json().get("message", "Bad request")
                raise ValueError(f"Invalid request: {error_msg}")

            elif response.status_code == 404:
                raise LookupError("One or more seed papers not found")

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
            return results, errors

    errors.append({
        "type": "max_retries",
        "message": "Maximum retries exceeded",
        "recoverable": True
    })
    return results, errors


def get_single_paper_recommendations(
    paper_id: str,
    limit: int,
    pool: str,
    api_key: Optional[str],
    limiter,
    backoff: ExponentialBackoff,
    debug: bool = False
) -> tuple[list[dict], list[dict]]:
    """
    Get recommendations for a single paper.

    Returns:
        Tuple of (results, errors)
    """
    url = f"{S2_RECOMMEND_URL}/forpaper/{paper_id}"
    params = {
        "fields": S2_FIELDS,
        "limit": min(limit, 500),
        "from": pool,
    }

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    results = []
    errors = []

    for attempt in range(backoff.max_attempts):
        limiter.wait()

        if debug:
            print(f"DEBUG: GET {url}", file=sys.stderr)

        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            limiter.record()

            if debug:
                print(f"DEBUG: Response status: {response.status_code}", file=sys.stderr)

            if response.status_code == 200:
                data = response.json()
                papers = data.get("recommendedPapers", [])

                for paper in papers:
                    results.append(format_paper(paper))

                return results, errors

            elif response.status_code == 429:
                if not backoff.wait(attempt):
                    errors.append({
                        "type": "rate_limit",
                        "message": "Rate limit exceeded",
                        "recoverable": True
                    })
                    return results, errors
                continue

            elif response.status_code == 404:
                raise LookupError(f"Paper not found: {paper_id}")

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
            return results, errors

    errors.append({
        "type": "max_retries",
        "message": "Maximum retries exceeded",
        "recoverable": True
    })
    return results, errors


def main():
    parser = argparse.ArgumentParser(
        description="Get paper recommendations from Semantic Scholar"
    )
    parser.add_argument(
        "--positive",
        help="Comma-separated IDs of papers to find similar to"
    )
    parser.add_argument(
        "--negative",
        help="Comma-separated IDs of papers to avoid similarity to"
    )
    parser.add_argument(
        "--for-paper",
        help="Single paper ID for quick recommendations"
    )
    parser.add_argument(
        "--pool",
        choices=["recent", "all-cs"],
        default="recent",
        help="Recommendation pool for --for-paper (default: recent)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum recommendations (default: 100, max: 500)"
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

    # Validate arguments
    if not args.positive and not args.for_paper:
        output_error(
            "",
            "config_error",
            "Must provide either --positive or --for-paper",
            exit_code=2
        )

    if args.positive and args.for_paper:
        output_error(
            "",
            "config_error",
            "Cannot use both --positive and --for-paper. Choose one mode.",
            exit_code=2
        )

    if args.negative and not args.positive:
        output_error(
            "",
            "config_error",
            "--negative requires --positive (not compatible with --for-paper)",
            exit_code=2
        )

    if args.limit > 500:
        output_error(
            "",
            "config_error",
            f"Limit {args.limit} exceeds maximum 500",
            exit_code=2
        )

    # Initialize rate limiter and backoff
    limiter = get_limiter("semantic_scholar")
    backoff = ExponentialBackoff(max_attempts=5)

    try:
        if args.for_paper:
            query_str = f"recommendations for {args.for_paper}"
            results, errors = get_single_paper_recommendations(
                args.for_paper,
                args.limit,
                args.pool,
                args.api_key,
                limiter,
                backoff,
                args.debug
            )
        else:
            positive_ids = [id.strip() for id in args.positive.split(",") if id.strip()]
            negative_ids = []
            if args.negative:
                negative_ids = [id.strip() for id in args.negative.split(",") if id.strip()]

            query_str = f"recommendations from {len(positive_ids)} positive"
            if negative_ids:
                query_str += f", {len(negative_ids)} negative"

            results, errors = get_batch_recommendations(
                positive_ids,
                negative_ids,
                args.limit,
                args.api_key,
                limiter,
                backoff,
                args.debug
            )

        if not results and not errors:
            output_error(query_str, "not_found", "No recommendations found", exit_code=1)

        if errors:
            warning = f"Completed with {len(errors)} error(s)."
            output_partial(query_str, results, errors, warning)
        else:
            output_success(query_str, results)

    except LookupError as e:
        output_error(args.for_paper or args.positive, "not_found", str(e), exit_code=1)

    except ValueError as e:
        output_error(args.for_paper or args.positive, "config_error", str(e), exit_code=2)

    except RuntimeError as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower():
            output_error(args.for_paper or args.positive, "rate_limit", error_msg, exit_code=3)
        else:
            output_error(args.for_paper or args.positive, "api_error", error_msg, exit_code=3)


if __name__ == "__main__":
    main()
