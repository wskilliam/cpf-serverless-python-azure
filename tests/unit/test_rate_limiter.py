import time
import unittest.mock
from src.core.utils.rate_limiter import is_rate_limited, RATE_LIMIT_COUNT, RATE_LIMIT_WINDOW

def test_first_request_not_limited():
    """Test that the first request from an IP is not rate-limited."""
    ip = "10.0.0.1"
    assert is_rate_limited(ip) is False

def test_multiple_requests_within_limit():
    """Test that multiple requests within the limit are not rate-limited."""
    ip = "10.0.0.2"
    for _ in range(RATE_LIMIT_COUNT - 1):
        assert is_rate_limited(ip) is False

def test_exceeding_rate_limit():
    """Test that requests are blocked after exceeding the rate limit."""
    ip = "10.0.0.3"
    # Make requests up to the limit
    for _ in range(RATE_LIMIT_COUNT):
        is_rate_limited(ip)
    # The next one should be limited
    assert is_rate_limited(ip) is True

def test_rate_limit_resets_after_window():
    """Test that the rate limit resets after the time window expires."""
    ip = "10.0.0.4"

    # Exceed the limit
    for _ in range(RATE_LIMIT_COUNT + 1):
        is_rate_limited(ip)

    # Mock time to be in the future, past the window
    future_time = time.time() + RATE_LIMIT_WINDOW + 1
    with unittest.mock.patch('time.time', return_value=future_time):
        # The limit should be reset
        assert is_rate_limited(ip) is False
