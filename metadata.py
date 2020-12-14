"""Fetch structured JSON-LD data from a given URL."""
import requests
import extruct
from w3lib.html import get_base_url
import json


def get_urls(filename):
    url_ls = []
    with open(filename, "r") as file:
        for line in file:
            stripped_line = line.strip()
            url_ls.append(stripped_line)
    return url_ls


def scrape(url: str):
    """Parse structured data from a target page."""
    html = get_html(url)
    metadata = get_metadata(html, url)
    return metadata


def get_html(url):
    """Get raw HTML from a URL."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(url, headers=headers)
    return req.content


def get_metadata(html: bytes, url: str):
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url=get_base_url(url),
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']
    if bool(metadata) and isinstance(metadata, list):
        metadata = metadata[0]
    return metadata


def write_metadata(url_ls):
    with open(r"metadata.txt", "w") as file:
        for url in url_ls:
            meta_json = json.dumps(scrape(url))
            if meta_json == '[]':
                continue


def main():
    url_ls = get_urls(r'urls.txt')
    write_metadata(url_ls)


if __name__ == '__main__':
    main()