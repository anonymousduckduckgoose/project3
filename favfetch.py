from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List

app = FastAPI()

@app.get("/favicon/{url:path}")
def fetch_favicon(url: str):
    try:
        if url.startswith("http:") or url.startswith("https:"):
            url = url.split(":")
        if len(url) >= 2:
            url = "://".join(url[:2])

        response = requests.get(url)
        response.raise_for_status()
        icons = get_favicons(url, response.text)

        # Check if the root URL also has a /favicon.ico endpoint
        favicon_url = urljoin(url, "/favicon.ico")
        try:
            response = requests.get(favicon_url)
            response.raise_for_status()
            icons.append(favicon_url)
        except requests.exceptions.RequestException:
            pass
        return icons
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch favicon: {str(e)}")

def get_favicons(url: str, html: str) -> List[str]:
    # Define the link relations (rel) and meta tag names for favicons as global variables
    global LINK_RELS
    global META_NAMES
    LINK_RELS = ['icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed']
    META_NAMES = ['msapplication-TileImage', 'og:image']
    
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
