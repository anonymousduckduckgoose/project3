# Favicon Fetcher Service

Favicon Fetcher is a FastAPI service designed to fetch favicon URLs from given websites. It is capable of following redirects, handling different favicon storage types, and deduping the fetched icons. The service also integrates Prometheus metrics through the `prometheus_fastapi_instrumentator` package.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- FastAPI
- Uvicorn
- httpx
- BeautifulSoup
- Prometheus (for metrics)
- Pytest (Optional, for testcase validations)

### Installation
This installation includes monitoring. If you would like to disable monitoring, 
you may comment out lines 17-58 in ./docker-compose.yml

1. Clone the repository by curling and unzipping the most recent release cut in a tarball.
```bash
curl -L "https://github.com/anonymousduckduckgoose/project3/archive/refs/tags/v2.0.0.tar.gz" > project3-v2.0.0.tar.gz
tar -xf project3-v2.0.0.tar.gz
```

2. Change directory into your newly cloned repo and run the setup.sh script:

```bash
cd project3-2.0.0
./setup.sh
```

### Usage

Once the service is running, you can fetch favicons by making GET requests:

```bash
# From the local machine
http://localhost:8000/favicon/{protocol:url}
```

If your host and port are externally exposed by an IP or domain, you can replace PUBLICIP:8000 with the appropriate external address.

### Sample Requests
```bash
http://PUBLICIP:8000/favicon/http:duckduckgo.com
```

### Tests
Simplified testcases are provided via ./test/test-favicon-service.py
To run these tests from the VM, simply run:

```bash
python3 -m pytest test-favicon-service.py
```