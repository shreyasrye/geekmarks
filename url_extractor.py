from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
import time
from config import cfd
from glob import glob    

DIR = 'some/where/'
existing_files = glob(DIR + '*.xls')
filename = DIR + 'stuff--%d--stuff.xls' % (len(existing_files) + 1)


def driver(browser):
    if browser == 'firefox':
        return webdriver.Firefox()
    if browser == 'chrome':
        return webdriver.Chrome(executable_path=cfd['chromedriverpath'])
    if browser == 'opera':
        return webdriver.Opera(executable_path=cfd['operadriverpath'])
    if browser == 'ie':
        return webdriver.Ie()
    if browser == 'edge':
        return webdriver.Edge(executable_path=cfd['edgedriverpath'])
    if browser == 'phantom':
        return webdriver.PhantomJS()
    raise Exception("The browser is not supported on webdriver")


class UrlExtractor:

    _URL = ""

    def __init__(self, url):
        self._URL = url

    def dynamic_web_scrape(self):
        dr = driver('chrome')
        dr.get('https://stackoverflow.com') # Can be any website that uses Google's login 
        dr.find_element_by_xpath('/html/body/header/div/ol[2]/li[2]/a[1]').click()
        time.sleep(3)
        dr.implicitly_wait(5)
        dr.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        time.sleep(3)
        dr.find_element_by_name('identifier').send_keys(cfd['google_usrnm']) # Insert username here
        dr.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
        dr.find_element_by_name('password').send_keys(cfd['google_pass'])  # Insert password here
        time.sleep(3)
        dr.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
        time.sleep(3)
        dr.get(self._URL)
        return dr.page_source


def remove_alphanumeric(string):
    return string[:string.find('&usg=')]


def static_page_extract(html_source):
    url_ls = []
    for link in BeautifulSoup(html_source, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            url_str = link['href']
            if url_str[0:7] == "/url?q=":
                url_ls.append(remove_alphanumeric(url_str[7:]))
    return url_ls


def write_to_file(ls, file_name):
    """ Write the extracted text into a file for annotating"""
    file = open(file_name, "a")
    for i in range(len(ls)):
        file.write(ls[i] + '\n')
    file.close()


def main():
    url_extractor = UrlExtractor("https://www.google.com/collections/s/list/qMTmb5xJRq-EnCOmXXjhHg/daaGT3tkSNI") # Google collection from which initial URLS are extracted

    source = url_extractor.dynamic_web_scrape()
    static_page_extract(source)
    url_ls = static_page_extract(source)
    write_to_file(url_ls, "ner/urls.txt")


if __name__ == '__main__':
    main()