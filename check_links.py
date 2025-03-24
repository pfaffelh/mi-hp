import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

visited_urls = set()

def check_link(link_url, source_url, only_errors=False):
    try:
        response = requests.head(link_url, timeout=5, allow_redirects=True)
        if response.status_code >= 400:
            print(f"ERROR on {source_url}: {link_url} not found ({response.status_code})")
        elif not only_errors:
            print(f"ERROR on {source_url}: {link_url} returned status code {response.status_code}")
    except requests.RequestException as e:
        print(f"[ERROR] on {source_url}: {link_url}  could not be reached: {e}")

def crawl(url, base_url, max_depth=2, depth=0, only_errors=False):
    if url in visited_urls or depth > max_depth:
        return
    visited_urls.add(url)
    if not only_errors:
        print(f"\nCrawling: {url}")

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        print(f"[ERROR] on {url} : Failed to retrieve with error {e}")
        return

    if 'text/html' not in response.headers.get('Content-Type', ''):
        return  # Skip non-HTML content

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Skip mailto: and JavaScript links
        if parsed.scheme not in ['http', 'https']:
            continue

        # Check link and report source page
        check_link(full_url, source_url=url, only_errors=only_errors)

        # Only crawl internal links (same domain)
        if parsed.netloc == urlparse(base_url).netloc:
            crawl(full_url, base_url, max_depth, depth + 1, only_errors=only_errors)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check website links for errors.")
    parser.add_argument("url", help="The URL to check, e.g., https://example.com")
    parser.add_argument("--only-errors", action="store_true", help="Show only broken links")
    parser.add_argument("--depth", type=int, default=2, help="Set crawl depth (default: 2)")

    args = parser.parse_args()

    crawl(args.url, args.url, max_depth=args.depth, only_errors=args.only_errors)


# use with
# python3 check_links.py "https://www.math.uni-freiburg.de/nlehre/" --only-errors --depth 3 > broken_links