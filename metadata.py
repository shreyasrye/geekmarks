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
    if len(url_ls) != 0:
        print("successfully loaded urls")
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


def write_metadata(url_ls, output_file):
    with open(output_file, "a") as file:
        for url in url_ls:
            meta_json = json.dumps(scrape(url))
            if meta_json == '[]':
                continue
            file.write(meta_json)
            file.write("\n")

def filter4Prodigy(read_file, write_file):
    """ Filter the metadata so only the headlines & urls are used for annotating. """
    for line in open(read_file, 'r'):
        dictionary = json.loads(line)
        text, publisher = "", ""
        for key, value in dictionary.items():
            if key == 'headline':
                text = value
            if key == 'publisher':
                try:
                    publisher = value['url']
                except (KeyError, TypeError):
                    publisher = value
        else:
            for key, value in dictionary.items():
                if key == '@graph':
                    for inner_dict in value:
                        for x, y in inner_dict.items():
                            if x == 'headline':
                                text = y
                            if x == 'publisher':
                                try:
                                    publisher = y['url']
                                except KeyError:
                                    publisher = y
        if text == "" and publisher == "":
            continue
        output = {
                "text": text,
                "meta": {
                    "source": publisher
                    }
            }
        output_file = open(write_file, 'a', encoding='utf-8')
        output_file.write(json.dumps(output))
        output_file.write("\n")
        output_file.close()

def main():
    url_ls = get_urls('ner/urls.txt')
    write_metadata(url_ls, "ner/metadata.txt")
    filter4Prodigy("ner/metadata.txt", "ner/train_data.jsonl")


if __name__ == '__main__':
    main()