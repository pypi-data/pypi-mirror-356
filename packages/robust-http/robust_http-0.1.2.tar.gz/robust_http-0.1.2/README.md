# robust_http

A smarter **requests** session for robust, fault-tolerant HTTP requests.

Net net: a smoother crawling experience.

**Why use it?**

One-line drop-in for `requests.Session` that automatically:

* Keeps long-running crawls stable with automatic retries
* Cuts redundant network traffic via transparent caching
* Throttles requests to respect rate limits
* 🧅 Adds optional Tor routing for privacy-sensitive use cases

**Features**

- Transparent cache (via `requests_cache`)
- User-Agent rotation (via `fake_useragent`)
- Throttling with jitter
- Retry logic with exponential backoff
- Tor proxy support with circuit rotation
- `TorManager` for NEWNYM signals and proxy config

## Installation

```bash
pip install robust_http
```

## Usage

You can use it like a drop-in replacement for **requests.Session**, either directly or as a context manager:

```python
from robust_http import session

client = session(use_tor=True, rotate_tor_every=50)
resp = client.get("https://example.com/api")
print(resp.json())
```

Or:

```python
from robust_http import session

with session(use_tor=True, rotate_tor_every=50) as client:
    resp = client.get("https://example.com/api")
    print(resp.json())
```

## Tor Support

To enable Tor-based routing, pass `use_tor=True` to your client.

👉 See [**TOR_SETUP.md**](TOR_SETUP.md) for instructions to set up Tor locally.
