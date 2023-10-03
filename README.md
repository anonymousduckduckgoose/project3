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
curl -L "https://github.com/anonymousduckduckgoose/project3/archive/refs/tags/v3.0.0.tar.gz" > project3-v3.0.0.tar.gz
tar -xf project3-v3.0.0.tar.gz
```

2. Change directory into your newly cloned repo and run the setup.sh script:

```bash
cd project3-3.0.0
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

### Monitoring
Basic monitoring has been instrumented through Prometheus and ingested to Grafana.

To view the default Grafana Dashboard:
{HOST} is either `localhost` or your Public IP with a corresponding exposed port.
Both username and password is `admin` on first login.
Once logged in you will find the `Favicon Fetcher API Service Dashboard` listed under General Dashboards.

```bash
http://{HOST}:3000/
```

To directly view the Prometheus UI
{HOST} is either `localhost` or your Public IP with a corresponding exposed port.

```bash
http://{HOST}:9090/
```

### Testing
Simplified testcases are provided via ./test/test-favicon-service.py
To run these tests from the VM, simply run:

```bash
python3 -m pytest test-favicon-service.py
```