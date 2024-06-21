from lib.methods import Browser

import json
import time
from selenium.webdriver.common.by import By



def main():
    URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
    URL2 = "https://qa.securiti.xyz"
    browser = Browser()
    browser.extract_links_securiti(URL, "//li", "//a[contains(@href, 'data-intelligence-target')]", "lib/data_intelligence_links.txt", lambda x: x.split("#")[0])
    browser.extract_links_securiti(URL2, "//div[contains(@class, 'c-brand-logo')]", "//a[@href]", "lib/securiti_links.txt")
    browser.close_browser()

if __name__ == "__main__":
    main()