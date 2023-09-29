from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
import os
import uvicorn

'''
Favicon Fetcher is a FastAPI service designed to fetch 
favicon URLs from given websites. It supports async calls 
and is capable of following redirects, handling different 
favicon storage types, and deduping the fetched icons. 

Supports the following request calls:
GET /favicon/{protocol:url}
    ex. /favicon/https:duckduckgo.com
GET /metrics
    exposes system metrics to prometheus
GET /openapi.json
    automated service documentation provided by OpenAPI. Also available in ../docs/openapi.json
'''

app = FastAPI()

# Pull environment variables set in Dockerfile. If not found, use local defaults.
HOST = str(os.getenv("host", "127.0.0.1"))
PORT = int(os.getenv("port", 8000))

# List of common favicon storage types
LINK_RELS = ['icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed']
META_NAMES = ['msapplication-TileImage', 'og:image']

# auto instrument prometheus using FastAPI instrumentor
Instrumentator().instrument(app).expose(app)

@app.get("/favicon/{url:path}")
async def fetch_favicon(url: str):
    ''' Defines GET /favicon/{args} and processes request

    args:
        url(str): URL path where favicon will be fetched.
        The :path allows '/' to be valid in the string

    returns:
        {base_url: (str), favicons: [(str)]}

    exceptions:
        InvalidURL: 400 Bad Request
        RequestError: 404: Failed to fetch favicon.ico
        else: An unexpected error occurred
    '''
    # Fail fast if request is not formatted correctly
    if "://" in url:
        raise HTTPException(status_code=400, detail="400 Bad Syntax: accepted format is protocol:url (e.g. http:duckduckgo.com) and should not contain '//'")
    try:
        icon_urls = []
        # Reformat URL from protocol:base_url to protocol://base_url
        if url.startswith("http:") or url.startswith("https:"):
            url = url.split(":")
            url = "://".join(url[:2])
        else:
            url = "http://" + url

        # async the request to increase responsiveness & scalability with parallel executions
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            # Handle redirects
            while response.status_code in (301, 302, 307, 308):
                url = response.headers.get('Location')
                if url:
                    response = await client.get(url)
                else:
                    break # Break out of While loop once response no longer includes a redirect

            try:
                # Check for most common favicon storage at /favicon.ico first  
                favicon_response = await client.get(urljoin(url, "/favicon.ico"))
                favicon_response.raise_for_status()
                icon_urls.append(urljoin(url, "/favicon.ico"))
            except httpx.HTTPStatusError:
                # If the status code indicates that /favicon.ico was not found,
                # continue with the other favicon storage methods. 
                pass

            # Check for other favicon storage methods
            response = await client.get(url)
            response.raise_for_status()
            icon_urls.extend(parse_html(url, response.text))
            icon_urls = list(set(icon_urls))

        # return json formatted api response to client
        return {
            "base_url": url,
            "favicons": icon_urls
        }
    # Handle errors
    except httpx.InvalidURL as e:
        raise HTTPException(status_code=400, detail=f"400 Bad Request: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=404, detail=f"404: Failed to fetch favicon.ico: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

def parse_html(url: str, html: str) -> List[str]:
    ''' Parse html source to find favicon link tags. Used in fetch_favicon function

    args:
        url(str): URL path where favicon is being fetched.
        html(str): contains the HTML content of the site fetched 

    returns:
        -> List[str]: returns a list of strings in the following format
        icon_urls: [(str)]

    exceptions are handled in parent function
    '''
    soup = BeautifulSoup(html, features='html.parser')
    icon_urls = set()

    # loop through link tags and check if its value is in predefined LINK_RELS list
    # add value to icon_urls list if href value exists.
    for link_tag in soup.find_all('link', attrs={'rel': lambda r: r and r.lower() in LINK_RELS, 'href': True}):
        href = link_tag.get('href', '').strip()
        if href and not href.startswith('data:image/'):
            url_parsed = urljoin(url, href)
            icon_urls.add(url_parsed)

    # loop through meta tags and check if its value is in predefined META_NAMES list
    # add value to icon_urls list if href value exists.
    for meta_tag in soup.find_all('meta', attrs={'content': True}):
        meta_type = meta_tag.get('name', '').lower()
        if meta_type in META_NAMES:
            href = meta_tag.get('content', '').strip()
            if href and not href.startswith('data:image/'):
                url_parsed = urljoin(url, href)
                icon_urls.add(url_parsed)

    return list(icon_urls)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)