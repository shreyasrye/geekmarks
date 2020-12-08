from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
import time

URL = "https://www.google.com/collections/s/list/UxLbhnEFTYylpfNwzYqSiA/tWCgSg5YIMY?q=AI-ML&sa=X&ved=2ahUKEwjFkMShnbvtAhVDVmMKHYaPAlAQ4r8DKAB6BAgAEAc"


def driver(browser):
    if browser == 'firefox':
        return webdriver.Firefox()
    if browser == 'chrome':
        return webdriver.Chrome(executable_path='C:/Users/Shreyas/Documents/misc/chromedriver.exe')
    if browser == 'opera':
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\\Program Files\\Opera\\launcher.exe"
        return webdriver.Opera(executable_path='operadriver.exe')
    if browser == 'ie':
        return webdriver.Ie()
    if browser == 'edge':
        return webdriver.Edge(executable_path='C:/Users/Shreyas/Documents/misc/msedgedriver.exe')
    if browser == 'phantom':
        return webdriver.PhantomJS()
    raise Exception("The browser is not supported on webdriver")


def dynamic_web_scrape(url):
    dr = driver('chrome')

    dr.get('https://stackoverflow.com')
    # dr.find_element_by_name('identifier').send_keys('peeyush.rai@gmail.com')
    dr.find_element_by_xpath('/html/body/header/div/ol[2]/li[2]/a[1]').click()
    time.sleep(3)
    dr.implicitly_wait(5)
    dr.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    time.sleep(3)
    dr.find_element_by_name('identifier').send_keys('shreyasrai23@gmail.com')
    dr.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
    dr.find_element_by_name('password').send_keys('')
    time.sleep(3)
    dr.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
    time.sleep(3)
    dr.get(url)
    return dr.page_source


def static_page_extract(html_source):
    # html_page = urllib.request.urlopen("https://arstechnica.com")  # Static page
    soup = BeautifulSoup(html_source, features="html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        print(link.get('href'))


def main():
    source = dynamic_web_scrape(URL)
    static_page_extract(source)


if __name__ == '__main__':
    main()