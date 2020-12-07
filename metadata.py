import urllib.request
from bs4 import BeautifulSoup

URL = 'https://www.crazyegg.com/blog/homepage-design/'


def get_data(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    meta_tags = soup.find_all('meta')
    meta_list = [t for t in meta_tags]
    return meta_list


def content_attr(t, key):
    if t.has_attr('content') and t.has_attr(key):
        return {'content': t['content'], key: t[key]}


def main():
    meta_list = get_data(URL)
    for i in meta_list:
        print( i)

    # Content names
    names = [content_attr(i, 'name') for i in meta_list if i is not None]
    properties = [content_attr(i, 'properties') for i in meta_list if i is not None]
    for x in names:
        if x is None:
            names.remove(x)
            continue
        print(x)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for y in properties:
        if x is None:
            properties.remove(y)
            continue
        print(y)


if __name__ == '__main__':
    main()