# Favicon Fetcher Service

Favicon Fetcher is a FastAPI service designed to fetch favicon URLs from given websites. It is capable of following redirects, handling different favicon storage types, and deduping the fetched icons. The service also integrates Prometheus metrics through the `prometheus_fastapi_instrumentator` package.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- FastAPI
- Uvicorn
- httpx
- BeautifulSoup
- Prometheus (Optional, for metrics)

### Installation

1. Clone the repository by curling the most recent release cut in a tarball.
2. Change directory into your newly cloned repo and run the setup.sh script:

```bash
cd project3
./setup.sh
```

### Usage

Once the service is running, you can fetch favicons by making a GET request to:

```bash
http://localhost:8000/favicon/{protocol:url}
```

If your host and port are externally exposed by an IP or domain, you can replace localhost:8000 with the appropriate external address.

### Sample Requests
```bash
http://localhost:8000/favicon/http:duckduckgo.com
```