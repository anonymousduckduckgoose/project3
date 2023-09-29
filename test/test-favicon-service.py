from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.abspath('../favicon-fetcher'))
from main import app

client = TestClient(app)

def test_url_reformatting():
    '''
    Confirm the url input is being reformatted correctly.
    '''
    test_cases = [
        {"input": "http:duckduckgo.com", "expected": "https://duckduckgo.com/"},
        {"input": "https:redfin.com", "expected": "https://www.redfin.com/"},
    ]
    
    for test_case in test_cases:
        response = client.get(f"/favicon/{test_case['input']}")
        assert response.status_code == 200
        assert response.json()["base_url"] == test_case["expected"]


def test_fetch_favicon():
    '''
    Confirm the status code is 200 on known-good favicon fetches.
    '''
    url = "http:duckduckgo.com"
    response = client.get(f"/favicon/{url}")
    assert response.status_code == 200

    url = "flights.google.com"
    response = client.get(f"/favicon/{url}")
    assert response.status_code == 200


# Additional test cases for error scenarios, edge cases, etc. can be added as needed.