from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
import uvicorn

app = FastAPI()

# List of common favicon storage types
LINK_RELS = ['icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed']
META_NAMES = ['msapplication-TileImage', 'og:image']

Instrumentator().instrument(app).expose(app)

@app.get("/favicon/{url:path}")
async def fetch_favicon(url: str):
    try:
        # Reformat URL
        if url.startswith("http:") or url.startswith("https:"):
            url = url.split(":")
        if len(url) >= 2:
            url = "://".join(url[:2])

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            # Handle redirects
            while response.status_code in (301, 302, 307, 308):
                url = response.headers.get('Location')
                if url:
                    response = await client.get(url)
                else:
                    break  # Break if Location header is missing

            response.raise_for_status()

            # Fetch Favicon
            icons = get_favicons(url, response.text)

            # Check for most common favicon storage at /favicon.ico 
            try:
                favicon_url = urljoin(url, "/favicon.ico")
                response = await client.get(favicon_url)
                response.raise_for_status()
                icons.append(favicon_url)
                icons = list(set(icons)) # Dedupe 
            except:
                pass
        # jsonify the response  
        return {
            "base_url": url,
            "favicons": icons
        }
    # Handle errors
    except httpx.HTTPStatusError:
        # If the status code indicates that /favicon.ico was not found,
        # continue with the other favicon storage methods.
        pass
    except httpx.InvalidURL as e:
        # catch mis-formatted requests
        raise HTTPException(status_code=400, detail=f"400 Bad Request: {str(e)}")
    except httpx.RequestError as e:
        # Handle other request errors
        raise HTTPException(status_code=404, detail=f"404: Failed to fetch favicon.ico: {str(e)}")
    except Exception as e:
        # Catch any other exceptions and return a 500 Internal Server Error response
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


def get_favicons(url: str, html: str) -> List[str]:
    soup = BeautifulSoup(html, features='html.parser')
    icons = set()

    for link_tag in soup.find_all('link', attrs={'rel': lambda r: r and r.lower() in LINK_RELS, 'href': True}):
        href = link_tag.get('href', '').strip()
        if href and not href.startswith('data:image/'):
            url_parsed = urljoin(url, href)
            icons.add(url_parsed)

    for meta_tag in soup.find_all('meta', attrs={'content': True}):
        meta_type = meta_tag.get('name', '').lower()
        if meta_type in META_NAMES:
            href = meta_tag.get('content', '').strip()
            if href and not href.startswith('data:image/'):
                url_parsed = urljoin(url, href)
                icons.add(url_parsed)

    return list(icons)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)