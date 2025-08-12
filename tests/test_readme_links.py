from pathlib import Path
import re
import requests


def extract_links(content: str) -> list[str]:
    """Return list of URLs from href and src attributes."""
    hrefs = re.findall(r'href="([^"]+)"', content)
    srcs = re.findall(r'src="([^"]+)"', content)
    return hrefs + srcs


def fetch_status(url: str) -> int:
    """Fetch URL returning HTTP status code."""
    for method in ("head", "get"):
        try:
            resp = requests.request(method, url, allow_redirects=True, timeout=10)
            return resp.status_code
        except requests.RequestException:
            if method == "get":
                raise
            continue
    raise AssertionError(f"Unable to fetch {url}")


def test_readme_links():
    content = Path("README.md").read_text(encoding="utf-8")
    links = extract_links(content)
    assert links, "No links found in README.md"
    for url in links:
        status = fetch_status(url)
        assert status < 400, f"{url} returned status {status}"
