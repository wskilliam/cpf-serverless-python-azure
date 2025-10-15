import time
from typing import Dict

# Basic in-memory store for rate limiting
# In a real-world distributed scenario, a shared store like Redis would be better.
request_counts: Dict[str, Dict[str, float]] = {}
RATE_LIMIT_COUNT = 10  # Max requests
RATE_LIMIT_WINDOW = 60  # Seconds

def is_rate_limited(ip_address: str) -> bool:
    """
    Checks if an IP address has exceeded the rate limit.
    """
    current_time = time.time()

    if ip_address not in request_counts:
        request_counts[ip_address] = {
            "count": 1,
            "window_start": current_time
        }
        return False

    ip_data = request_counts[ip_address]

    # Reset window if it has expired
    if current_time - ip_data["window_start"] > RATE_LIMIT_WINDOW:
        ip_data["count"] = 1
        ip_data["window_start"] = current_time
        return False

    # Increment count and check limit
    ip_data["count"] += 1
    if ip_data["count"] > RATE_LIMIT_COUNT:
        return True

    return False
