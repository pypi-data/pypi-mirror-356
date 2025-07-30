# ============ robust_http/client.py ============
"""
High-level HTTP client module.

Provides:
- RobustSession: a drop-in replacement for requests.Session with caching, UA rotation,
  throttling, retries, and optional Tor circuit renewal.
- session(): convenience function aliasing RobustSession(**kwargs).
"""

import time
import random
import logging
from typing import Optional, Dict, Any, Callable

import requests
import requests_cache
from fake_useragent import UserAgent

from .tor_manager import TorManager
from .utils import append_cache_buster

logger = logging.getLogger(__name__)

class RobustSession:
    """
    HTTP client handling cookies, UA rotation, throttle, retries, and Tor.
    
    In many cases, this class can be used as a drop-in replacement for `requests.Session`.
    
    Usage:
    ```python
    from robust_http import RobustSession

    client = RobustSession(
        use_tor=True,
        tor_kwargs={"password": "mytorpwd"},
        rotate_tor_every=50
    )
    resp = client.get("https://example.com/api")
    data = resp.json()
    print(data)
    ```
    """

    def __init__(
        self,
        cache_name: str = "http_cache",
        expire_after: int = 3600,
        throttle: float = 3.0,
        max_retries: int = 3,
        backoff: float = 0.5,
        proxy_pool: Optional[list] = None,
        use_tor: bool = False,
        tor_kwargs: Optional[Dict[str, Any]] = None,
        rotate_tor_every: Optional[int] = None,
    ):
        """Initialize the RobustSession.

        Args:
            cache_name: Name of the requests_cache cache.
            expire_after: Seconds until cache expiration.
            throttle: Minimum seconds between requests (plus jitter).
            max_retries: Number of retry attempts.
            backoff: Base backoff multiplier for retry sleeping.
            proxy_pool: List of proxy dicts to cycle through.
            use_tor: Enable Tor proxy and circuit renewal.
            tor_kwargs: Parameters for TorManager.
            rotate_tor_every: Renew Tor circuit after this many calls.
        
        Usage:
        ```python
        from robust_http import RobustSession, session

        # 1) via helper
        client = session(use_tor=True)

        # 2) instantiate directly
        client = RobustSession(use_tor=True)

        # 3) using tor options
        client = RobustSession(
            use_tor=True,
            tor_kwargs={"password": "mytorpwd"},
            rotate_tor_every=50
        )
        
        resp = client.get("https://example.com/api")
        data = resp.json()
        print(data)
        ```
        """
        self.session = requests_cache.CachedSession(
            cache_name=cache_name,
            expire_after=expire_after,
            allowable_methods=["GET", "POST"],
        )
        # Ensure compatibility with custom session types:
        if not hasattr(self.session, "headers"):
            self.session.headers = {}
        if not hasattr(self.session, "proxies"):
            self.session.proxies = {}

        self.ua = UserAgent()
        self._rotate_user_agent()
        self.session.headers.update({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        })

        self.proxy_pool = proxy_pool or [{}]
        self.session.proxies = self.proxy_pool[0]

        self.throttle = throttle
        self._last_call = 0.0
        self.max_retries = max_retries
        self.backoff = backoff
        self.rotate_tor_every = rotate_tor_every
        self._call_count = 0

        if use_tor:
            self.tor = TorManager(**(tor_kwargs or {}))
            self.tor.apply_to_session(self.session)
            try:
                logger.info("Tor exit IP: %s", self.tor.get_exit_ip())
            except Exception:
                logger.warning("Could not fetch Tor IP")
        else:
            self.tor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.session.close()

    def _rotate_user_agent(self) -> None:
        """Rotate the User-Agent header for the session."""
        self.session.headers["User-Agent"] = self.ua.random

    def _respect_throttle(self) -> None:
        """Enforce a minimum delay (with jitter) between requests."""
        now = time.time()
        wait = (self.throttle - (now - self._last_call)) + random.uniform(-0.2, 0.2)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.time()

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        retry_if: Optional[Callable[[requests.Response], bool]] = None,
        cache_buster: bool = False,
        **kwargs,
    ) -> requests.Response:
        """Send HTTP request with retries, throttle, UA rotation, and optional Tor renewal.

        Args:
            method: HTTP method.
            url: Request URL.
            params: Query parameters.
            data: Form data.
            json: JSON body.
            retry_if: Callable to trigger retry on response.
            cache_buster: Append cache-buster to URL.
            **kwargs: Passed to requests.

        Returns:
            A successful requests.Response.

        Raises:
            RuntimeError: If all retries fail.
        """
        last_err = None
        if cache_buster:
            url = append_cache_buster(url)

        for attempt in range(1, self.max_retries + 1):
            logger.debug("Attempt %d %s %s", attempt, method, url)
            self._respect_throttle()
            if self.tor and attempt > 1:
                self.tor.renew_circuit()
                self._rotate_user_agent()

            try:
                resp = self.session.request(
                    method, url,
                    params=params, data=data, json=json,
                    timeout=30, **kwargs
                )
                text = resp.text.lower()
                if "pardon our interruption" in text or "imperva" in text:
                    raise RuntimeError("WAF challenge detected")
                resp.raise_for_status()
                if retry_if and retry_if(resp):
                    raise RuntimeError("Custom retry condition")

                self._call_count += 1
                if (
                    self.tor
                    and self.rotate_tor_every
                    and self._call_count % self.rotate_tor_every == 0
                ):
                    logger.info(
                        "Auto-renewing Tor circuit after %d requests",
                        self._call_count,
                    )
                    self.tor.renew_circuit()
                    self._rotate_user_agent()

                return resp

            except Exception as e:
                # Do not retry non-GET methods
                if method.upper() != "GET":
                    raise RuntimeError(f"Non-GET request failed: {e}")

                # For HTTP errors: do not retry 4xx (except 429)
                if isinstance(e, requests.HTTPError):
                    code = None
                    if hasattr(e, "response") and e.response is not None:
                        code = e.response.status_code
                    else:
                        try:
                            code = int(str(e))
                        except Exception:
                            pass
                    if code and 400 <= code < 500 and code != 429:
                        raise

                last_err = e
                logger.warning("Error on attempt %d: %s", attempt, e)
                time.sleep(self.backoff * attempt * random.uniform(0.8, 1.2))

        logger.critical(
            "All %d attempts failed for %s %s",
            self.max_retries,
            method,
            url,
        )
        raise RuntimeError(f"Request failed after {self.max_retries} tries: {last_err}")

    def get(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP GET."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP POST."""
        return self.request("POST", url, **kwargs)
    
    def head(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP HEAD."""
        return self.request("HEAD", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP PUT."""
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP PATCH."""
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP DELETE."""
        return self.request("DELETE", url, **kwargs)

    def options(self, url: str, **kwargs) -> requests.Response:
        """Convenience method for HTTP OPTIONS."""
        return self.request("OPTIONS", url, **kwargs)

def session(
    cache_name: str = "http_cache",
    expire_after: int = 3600,
    throttle: float = 3.0,
    max_retries: int = 3,
    backoff: float = 0.5,
    proxy_pool: Optional[list] = None,
    use_tor: bool = False,
    tor_kwargs: Optional[Dict[str, Any]] = None,
    rotate_tor_every: Optional[int] = None,
) -> RobustSession:
    """
    Create and return a `RobustSession` instance.

    Preferred way to use the library—acts as a drop-in replacement for 
    `requests.session()` with added caching, retries, UA rotation, throttling, 
    and optional Tor support.

    Args:
        cache_name: Name of the requests_cache cache.
        expire_after: Seconds until cache expiration.
        throttle: Minimum seconds between requests (plus jitter).
        max_retries: Number of retry attempts.
        backoff: Base backoff multiplier for retry sleeping.
        proxy_pool: List of proxy dicts to cycle through.
        use_tor: Enable Tor proxy and circuit renewal.
        tor_kwargs: Parameters for TorManager.
        rotate_tor_every: Renew Tor circuit after this many calls.

    Returns:
        A configured `RobustSession` instance.

    Example:
    ```python
    from robust_http import session

    client = session(use_tor=True)
    resp = client.get("https://example.com")
    print(resp.json())
    ```
    """
    return RobustSession(
        cache_name=cache_name,
        expire_after=expire_after,
        throttle=throttle,
        max_retries=max_retries,
        backoff=backoff,
        proxy_pool=proxy_pool,
        use_tor=use_tor,
        tor_kwargs=tor_kwargs,
        rotate_tor_every=rotate_tor_every,
    )