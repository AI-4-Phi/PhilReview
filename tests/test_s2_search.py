"""
Tests for s2_search.py (Semantic Scholar search).

Tests cover:
- Output schema validation
- Exit codes for different scenarios
- Query parameter handling
- Rate limiting integration
- Error handling
"""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import test utilities
from test_utils import validate_output_schema, run_script, SCRIPTS_DIR


class TestS2SearchOutputSchema:
    """Tests for JSON output schema compliance."""

    def test_success_output_schema(self, mock_s2_response):
        """Successful response should have correct schema."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: mock_s2_response
            )

            # Import fresh to avoid caching issues
            import importlib
            import s2_search
            importlib.reload(s2_search)

            # Capture output by mocking print and sys.exit
            output = None
            def capture_print(data):
                nonlocal output
                output = json.loads(data)

            with patch("builtins.print", capture_print):
                with pytest.raises(SystemExit) as exc_info:
                    s2_search.output_success("test query", [{"title": "Test"}])

            assert exc_info.value.code == 0
            errors = validate_output_schema(output, "success")
            assert errors == [], f"Schema errors: {errors}"

    def test_error_output_schema(self):
        """Error response should have correct schema."""
        import s2_search

        output = None
        def capture_print(data):
            nonlocal output
            output = json.loads(data)

        with patch("builtins.print", capture_print):
            with pytest.raises(SystemExit) as exc_info:
                s2_search.output_error("test query", "api_error", "Test error", exit_code=3)

        assert exc_info.value.code == 3
        errors = validate_output_schema(output, "error")
        assert errors == [], f"Schema errors: {errors}"

    def test_partial_output_schema(self):
        """Partial response should have correct schema."""
        import s2_search

        output = None
        def capture_print(data):
            nonlocal output
            output = json.loads(data)

        with patch("builtins.print", capture_print):
            with pytest.raises(SystemExit) as exc_info:
                s2_search.output_partial(
                    "test query",
                    [{"title": "Test"}],
                    [{"type": "rate_limit", "message": "Rate limited"}],
                    "Partial results"
                )

        assert exc_info.value.code == 0
        assert output["status"] == "partial"
        assert "warning" in output


class TestS2SearchExitCodes:
    """Tests for correct exit codes."""

    def test_exit_code_0_on_success(self):
        """Should exit with 0 on successful search."""
        import s2_search

        with patch("builtins.print"):
            with pytest.raises(SystemExit) as exc_info:
                s2_search.output_success("query", [{"title": "Test"}])

        assert exc_info.value.code == 0

    def test_exit_code_1_on_not_found(self):
        """Should exit with 1 when no results found."""
        import s2_search

        with patch("builtins.print"):
            with pytest.raises(SystemExit) as exc_info:
                s2_search.output_error("query", "not_found", "No results", exit_code=1)

        assert exc_info.value.code == 1

    def test_exit_code_2_on_config_error(self):
        """Should exit with 2 on configuration error."""
        import s2_search

        with patch("builtins.print"):
            with pytest.raises(SystemExit) as exc_info:
                s2_search.output_error("query", "config_error", "Bad config", exit_code=2)

        assert exc_info.value.code == 2

    def test_exit_code_3_on_api_error(self):
        """Should exit with 3 on API error."""
        import s2_search

        with patch("builtins.print"):
            with pytest.raises(SystemExit) as exc_info:
                s2_search.output_error("query", "api_error", "API failed", exit_code=3)

        assert exc_info.value.code == 3


class TestS2SearchFormatPaper:
    """Tests for paper formatting."""

    def test_format_paper_basic(self):
        """format_paper should extract basic fields."""
        import s2_search

        paper = {
            "paperId": "abc123",
            "title": "Test Paper",
            "authors": [{"name": "John Doe", "authorId": "123"}],
            "year": 2024,
            "abstract": "This is a test.",
            "citationCount": 10,
            "externalIds": {"DOI": "10.1234/test"},
            "url": "https://example.com",
            "venue": "Test Journal",
            "journal": {"name": "Test Journal"},
            "publicationTypes": ["JournalArticle"],
        }

        formatted = s2_search.format_paper(paper)

        assert formatted["paperId"] == "abc123"
        assert formatted["title"] == "Test Paper"
        assert formatted["year"] == 2024
        assert formatted["doi"] == "10.1234/test"
        assert formatted["citationCount"] == 10
        assert len(formatted["authors"]) == 1
        assert formatted["authors"][0]["name"] == "John Doe"

    def test_format_paper_missing_fields(self):
        """format_paper should handle missing fields gracefully."""
        import s2_search

        paper = {
            "paperId": "abc123",
            "title": "Minimal Paper",
        }

        formatted = s2_search.format_paper(paper)

        assert formatted["paperId"] == "abc123"
        assert formatted["title"] == "Minimal Paper"
        assert formatted["doi"] is None
        assert formatted["arxivId"] is None
        assert formatted["authors"] == []

    def test_format_paper_extracts_arxiv(self):
        """format_paper should extract arXiv ID."""
        import s2_search

        paper = {
            "paperId": "abc123",
            "title": "ArXiv Paper",
            "externalIds": {"ArXiv": "2401.12345"},
        }

        formatted = s2_search.format_paper(paper)
        assert formatted["arxivId"] == "2401.12345"


class TestS2SearchIntegration:
    """Integration tests using mocked HTTP responses."""

    @patch("requests.get")
    def test_relevance_search_success(self, mock_get, mock_s2_response):
        """Relevance search should return formatted results."""
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_s2_response
        )

        import s2_search
        from rate_limiter import get_limiter, ExponentialBackoff

        limiter = get_limiter("semantic_scholar")
        backoff = ExponentialBackoff()

        results = s2_search.relevance_search(
            query="free will",
            limit=10,
            year=None,
            field=None,
            min_citations=None,
            api_key=None,
            limiter=limiter,
            backoff=backoff,
        )

        assert len(results) == 2
        assert results[0]["title"] == "Free Will and Moral Responsibility"
        assert results[1]["title"] == "Compatibilism and Free Will"

    @patch("requests.get")
    def test_handles_rate_limit(self, mock_get):
        """Should handle 429 rate limit responses."""
        # First call returns 429, second returns success
        mock_get.side_effect = [
            MagicMock(status_code=429),
            MagicMock(
                status_code=200,
                json=lambda: {"total": 1, "data": [{"paperId": "123", "title": "Test"}]}
            ),
        ]

        import s2_search
        from rate_limiter import get_limiter, ExponentialBackoff

        limiter = get_limiter("semantic_scholar")
        backoff = ExponentialBackoff(max_attempts=3)

        with patch("time.sleep"):  # Don't actually sleep in tests
            results = s2_search.relevance_search(
                query="test",
                limit=1,
                year=None,
                field=None,
                min_citations=None,
                api_key=None,
                limiter=limiter,
                backoff=backoff,
            )

        assert len(results) == 1

    @patch("requests.get")
    def test_handles_api_error(self, mock_get):
        """Should raise on persistent API errors."""
        mock_get.return_value = MagicMock(status_code=500)

        import s2_search
        from rate_limiter import get_limiter, ExponentialBackoff

        limiter = get_limiter("semantic_scholar")
        backoff = ExponentialBackoff(max_attempts=1)

        with pytest.raises(RuntimeError) as exc_info:
            s2_search.relevance_search(
                query="test",
                limit=1,
                year=None,
                field=None,
                min_citations=None,
                api_key=None,
                limiter=limiter,
                backoff=backoff,
            )

        assert "500" in str(exc_info.value)


class TestS2SearchCLI:
    """Tests for command-line interface."""

    def test_cli_missing_query(self, run_skill_script):
        """Should fail when query is missing."""
        result = run_skill_script("s2_search.py")
        assert result.returncode == 2  # argparse error

    def test_cli_help(self, run_skill_script):
        """Should show help with --help."""
        result = run_skill_script("s2_search.py", "--help")
        assert result.returncode == 0
        assert "Search Semantic Scholar" in result.stdout

    def test_cli_limit_validation(self, run_skill_script):
        """Should reject limit exceeding maximum."""
        # For relevance search, max is 100
        result = run_skill_script("s2_search.py", "test", "--limit", "200")
        assert result.returncode == 2

        output = result.json
        assert output["status"] == "error"
        assert "exceeds maximum" in output["errors"][0]["message"]


class TestS2SearchProgressOutput:
    """Tests for progress/status output to stderr."""

    def test_log_progress_to_stderr(self):
        """Progress messages should go to stderr."""
        import s2_search
        import io
        import sys

        # Capture stderr
        captured = io.StringIO()
        with patch("sys.stderr", captured):
            s2_search.log_progress("Test message")

        output = captured.getvalue()
        assert "[s2_search.py]" in output
        assert "Test message" in output
