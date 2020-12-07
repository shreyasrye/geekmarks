from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
import time


def driver(browser):
    if browser == 'firefox':
        return webdriver.Firefox()
    if browser == 'chrome':
        return webdriver.Chrome('chromedriver.exe')
    if browser == 'opera':
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\\Program Files\\Opera\\launcher.exe"
        return webdriver.Opera(executable_path='operadriver.exe')
    if browser == 'ie':
        return webdriver.Ie()
    if browser == 'edge':
        return webdriver.Edge(executable_path='/path/to/MicrosoftWebDriver.exe')
    if browser == 'phantom':
        return webdriver.PhantomJS()
    raise Exception("The browser is not supported on webdriver")


def dynamic_web_scrape():
    dr = driver('edge')
    dr.get("https://www.tripadvisor.com/Airline_Review-d8729157-Reviews-Spirit-Airlines#REVIEWS")
    more_buttons = driver.find_elements_by_class_name("moreLink")
    for x in range(len(more_buttons)):
        if more_buttons[x].is_displayed():
            dr.execute_script("arguments[0].click();", more_buttons[x])
            time.sleep(1)
    p_source = dr.page_source
    return p_source


def static_page_extract(html_source):
    # html_page = urllib.request.urlopen("https://arstechnica.com")  # Static page
    soup = BeautifulSoup(html_source, features="html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        print(link.get('href'))


def main():
    source = dynamic_web_scrape()
    static_page_extract(source)


if __name__ == '__main__':
    main()