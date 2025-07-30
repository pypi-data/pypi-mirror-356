# ============ robust_http/utils.py ============
"""
Helper utilities for robust_http.
"""
import time
import random


def append_cache_buster(url: str) -> str:
    """Append a random float and timestamp to defeat caches."""
    rnd = f"{random.random():.16f}"
    ts = str(int(time.time() * 1000))
    sep = '&' if '?' in url else '?'
    return f"{url}{sep}rnd={rnd}&_={ts}"