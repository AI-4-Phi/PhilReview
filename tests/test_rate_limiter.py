"""
Tests for the rate_limiter module.

Tests cover:
- Basic rate limiting functionality
- File locking behavior
- Exponential backoff
- Multi-API support
"""

import time
from pathlib import Path
from unittest.mock import patch

import pytest

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / ".claude" / "skills" / "philosophy-research" / "scripts"))

from rate_limiter import (
    RateLimiter,
    ExponentialBackoff,
    get_limiter,
    list_active_limiters,
    clear_all_limiters,
    LIMITERS,
)


class TestRateLimiter:
    """Tests for the RateLimiter class."""

    def test_init_creates_lock_dir(self):
        """Rate limiter should create lock directory if it doesn't exist."""
        limiter = RateLimiter("test_api", 0.1)
        assert limiter.LOCK_DIR.exists()

    def test_first_request_no_wait(self):
        """First request should not wait."""
        limiter = RateLimiter("test_first", 1.0)
        limiter.reset()  # Ensure clean state

        wait_time = limiter.wait()
        assert wait_time == 0.0

    def test_subsequent_request_waits(self):
        """Subsequent request should wait for min_interval."""
        limiter = RateLimiter("test_wait", 0.2)
        limiter.reset()

        # First request
        limiter.wait_and_record()

        # Second request should wait
        start = time.time()
        wait_time = limiter.wait()
        elapsed = time.time() - start

        assert wait_time > 0
        assert elapsed >= 0.15  # Allow some tolerance

    def test_record_updates_lock_file(self):
        """Record should update the lock file with current time."""
        limiter = RateLimiter("test_record", 0.1)
        limiter.reset()

        before = time.time()
        limiter.record()
        after = time.time()

        # Read lock file
        content = limiter.lock_file.read_text().strip()
        recorded_time = float(content)

        assert before <= recorded_time <= after

    def test_reset_removes_lock_file(self):
        """Reset should remove the lock file."""
        limiter = RateLimiter("test_reset", 0.1)
        limiter.record()  # Create lock file
        assert limiter.lock_file.exists()

        limiter.reset()
        assert not limiter.lock_file.exists()

    def test_wait_and_record_convenience(self):
        """wait_and_record should call both methods."""
        limiter = RateLimiter("test_convenience", 0.1)
        limiter.reset()

        wait_time = limiter.wait_and_record()
        assert wait_time == 0.0
        assert limiter.lock_file.exists()

    def test_last_wait_time_property(self):
        """last_wait_time should reflect most recent wait."""
        limiter = RateLimiter("test_last_wait", 0.1)
        limiter.reset()

        assert limiter.last_wait_time is None

        limiter.wait()
        assert limiter.last_wait_time == 0.0

        limiter.record()
        limiter.wait()
        assert limiter.last_wait_time > 0


class TestExponentialBackoff:
    """Tests for the ExponentialBackoff class."""

    def test_init_defaults(self):
        """Default initialization should have expected values."""
        backoff = ExponentialBackoff()
        assert backoff.max_attempts == 5
        assert backoff.base_delay == 1.0
        assert backoff.max_delay == 60.0

    def test_get_delay_exponential(self):
        """Delay should increase exponentially."""
        backoff = ExponentialBackoff(base_delay=1.0, max_delay=100.0)

        assert backoff.get_delay(0) == 1.0
        assert backoff.get_delay(1) == 2.0
        assert backoff.get_delay(2) == 4.0
        assert backoff.get_delay(3) == 8.0

    def test_get_delay_capped_at_max(self):
        """Delay should not exceed max_delay."""
        backoff = ExponentialBackoff(base_delay=1.0, max_delay=5.0)

        assert backoff.get_delay(10) == 5.0

    def test_wait_returns_false_on_max_attempts(self):
        """wait() should return False when max attempts reached."""
        backoff = ExponentialBackoff(max_attempts=3)

        assert backoff.wait(0) is True
        assert backoff.wait(1) is True
        assert backoff.wait(2) is False  # max_attempts - 1

    @patch("time.sleep")
    def test_wait_sleeps_with_jitter(self, mock_sleep):
        """wait() should sleep with jitter added."""
        backoff = ExponentialBackoff(base_delay=1.0, max_delay=100.0)

        backoff.wait(0)

        # Should have slept between 1.0 and 2.0 (base + jitter)
        mock_sleep.assert_called_once()
        sleep_time = mock_sleep.call_args[0][0]
        assert 1.0 <= sleep_time <= 2.0

    def test_last_delay_property(self):
        """last_delay should reflect most recent wait delay."""
        backoff = ExponentialBackoff()
        assert backoff.last_delay is None

        with patch("time.sleep"):
            backoff.wait(0)

        assert backoff.last_delay is not None
        assert backoff.last_delay >= 1.0


class TestGetLimiter:
    """Tests for the get_limiter factory function."""

    def test_returns_configured_limiter(self):
        """get_limiter should return properly configured limiter."""
        limiter = get_limiter("semantic_scholar")

        assert isinstance(limiter, RateLimiter)
        assert limiter.api_name == "semantic_scholar"
        assert limiter.min_interval == 1.1

    def test_all_apis_have_limiters(self):
        """All configured APIs should return valid limiters."""
        for api_name in LIMITERS.keys():
            limiter = get_limiter(api_name)
            assert isinstance(limiter, RateLimiter)
            assert limiter.api_name == api_name

    def test_unknown_api_raises(self):
        """Unknown API name should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_limiter("unknown_api")

        assert "Unknown API" in str(exc_info.value)
        assert "unknown_api" in str(exc_info.value)

    def test_each_call_returns_fresh_instance(self):
        """Each call should return a new limiter instance."""
        limiter1 = get_limiter("semantic_scholar")
        limiter2 = get_limiter("semantic_scholar")

        assert limiter1 is not limiter2


class TestLimiterManagement:
    """Tests for limiter listing and clearing."""

    def test_list_active_limiters_empty(self):
        """list_active_limiters should return empty list when no limiters active."""
        clear_all_limiters()
        active = list_active_limiters()
        assert active == []

    def test_list_active_limiters_shows_used(self):
        """list_active_limiters should show limiters that have been used."""
        clear_all_limiters()

        limiter = get_limiter("semantic_scholar")
        limiter.record()

        active = list_active_limiters()
        assert "semantic_scholar" in active

    def test_clear_all_limiters(self):
        """clear_all_limiters should remove all lock files."""
        # Create some limiters
        get_limiter("semantic_scholar").record()
        get_limiter("brave").record()

        count = clear_all_limiters()
        assert count >= 2

        active = list_active_limiters()
        assert len(active) == 0


class TestConcurrentAccess:
    """Tests for concurrent access behavior."""

    def test_multiple_limiters_independent(self):
        """Different API limiters should be independent."""
        limiter1 = get_limiter("semantic_scholar")
        limiter2 = get_limiter("brave")

        limiter1.reset()
        limiter2.reset()

        # Record on limiter1
        limiter1.wait_and_record()

        # limiter2 should not wait
        wait_time = limiter2.wait()
        assert wait_time == 0.0
