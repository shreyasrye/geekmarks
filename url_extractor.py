from bs4 import BeautifulSoup
import urllib.request
import re
from selenium import webdriver
import time

URL = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fwww.google.com%2Fcollections%2Fs%2Flist%2FUxLbhnEFTYylpfNwzYqSiA%2FtWCgSg5YIMY%3Fq%3DAI-ML%26sa%3DX%26ved%3D2ahUKEwjFkMShnbvtAhVDVmMKHYaPAlAQ4r8DKAB6BAgAEAc&sacu=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"


def driver(browser):
    if browser == 'firefox':
        return webdriver.Firefox()
    if browser == 'chrome':
        return webdriver.Chrome(executable_path='C:/Users/Shreyas/Documents/misc/msedgedriver.exe''chromedriver.exe')
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
    dr.get(url)
    time.sleep(5)
    username = dr.find_element_by_id("identifierId")
    username.send_keys("shreyasrai23@gmail.com")
    username.send_keys(u'\ue007')
    # dr.find_element_by_name("identifierNext").click()
    password = dr.find_element_by_id("password")
    password.send_keys("v1N$m0ke_785anji222")
    dr.find_element_by_name("passwordNext").click()
    time.sleep(5)
    html = dr.page_source
    return html


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