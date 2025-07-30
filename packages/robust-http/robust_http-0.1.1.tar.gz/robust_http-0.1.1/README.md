# robust_http

A Python package providing:

- **RobustClient**: High-level HTTP client with:

  - Cookie & JS-challenge caching (requests_cache)
  - User-Agent rotation (fake_useragent)
  - Rate-limiting & jitter
  - Retries with exponential backoff
  - Optional Tor support (proxying & automatic circuit rotation)
- **TorManager**: Helper for configuring Tor proxies and sending NEWNYM signals.

## Installation

```bash
pip install robust_http
```

## Usage

```python
from robust_http import RobustClient

client = RobustClient(use_tor=True, tor_kwargs={"password": "mytorpwd"}, rotate_tor_every=50)
resp = client.get("https://example.com/api")
print(resp.json())
```
