from lib.methods import Browser

import json

from selenium.webdriver.common.by import By

def extract_links_securiti(url: str, xpath_for_redirect_load: str, xpath_for_urls: str, file_name: str, link_format_func: callable = lambda x: x):
    '''Goes to the securities website and extracts all the links from the page
    and writes them to a file.
    xpath_for_urls: xpath for the urls based on the target page
    file_name: name of the file to write the urls to
    '''
    # read data.json as a dictionary
    with open("lib/data.json", 'r') as file:
        data = json.load(file)
    
    browser = Browser()
    browser.open_page(url)
    # login and wait for the page to load (wait for the li element to be present)
    if not browser.is_logged_in():
        browser.login_securiti(data["email"], data["password"], xpath_for_redirect_load)

    li = browser.get_all_elements(By.XPATH, xpath_for_urls)
    print([i.get_attribute("outerHTML") for i in li])
    links = [link_format_func(i.get_attribute("href")) for i in li]
    links = list(set(links))

    # write to data_intelligence_links.txt
    with open(file_name, 'a') as file:
        for link in links:
            file.write(link + "\n")

    browser.close_browser()

def main():
    URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
    URL2 = "https://qa.securiti.xyz"
    # extract_links_securiti(URL, "//li", "//a[contains(@href, 'data-intelligence-target')]", "lib/data_intelligence_links.txt", lambda x: x.split("#")[0])
    extract_links_securiti(URL2, "//div[contains(@class, 'c-brand-logo')]", "//a[@href]", "lib/securiti_links.txt")
if __name__ == "__main__":
    main()