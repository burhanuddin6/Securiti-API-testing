from lib.methods import Browser

import json

from selenium.webdriver.common.by import By

URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
CLASSNAME = "ld-tab-content"

def extract_doc_links():
    # read data.json as a dictionary
    with open("lib/data.json", 'r') as file:
        data = json.load(file)
    
    browser = Browser()
    browser.open_page(URL)
    # login and wait for the page to load (wait for the li element to be present)
    browser.login_securiti(data["email"], data["password"], "//li")
    
    li = browser.get_all_elements(By.XPATH, "//a[contains(@href, 'data-intelligence-target')]")
    links = [i.get_attribute("href").split("#")[0] for i in li]
    links = list(set(links))

    # write to data_intelligence_links.txt
    with open("lib/data_intelligence_links.txt", 'w') as file:
        for link in links:
            file.write(link + "\n")

    browser.close_browser()

def main():
    extract_doc_links()

if __name__ == "__main__":
    main()