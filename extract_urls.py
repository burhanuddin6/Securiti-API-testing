from lib.methods import Browser

import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
    URL2 = "https://qa.securiti.xyz"
    browser = Browser()
    # # please see the docstring of the extract_links function for more information on parameters
    # browser.extract_links_securiti(url=URL, xpath_for_urls="//a[contains(@href, 'data-intelligence-target')]", 
    #                                file_name="lib/data_intelligence_links.txt",
    #                                xpath_for_redirect_load="//li", 
    #                                link_format_func=lambda x: x.split("#")[0])
    # browser.extract_links_securiti(url=URL2, xpath_for_urls="//a[@href]", file_name="lib/securiti_links.txt")
    
    browser.open_securiti_page(URL2)
    # divs_with_text_only = browser.get_all_elements(By.XPATH, "//div[not(*) and normalize-space()]")
    # print([i.get_attribute("outerHTML") for i in divs_with_text_only])
    
    xpaths = ["//input", "//button", "//a[@href]", "//div[contains(@class, 'clickable')]"]
    browser.traverse_site(xpaths)
    
    # xpath = "//button[@class='f-feedback-button f-btn-white ma-0 v-btn theme--light']"
    # browser.click_element(By.XPATH, xpath)
    # browser.check_and_close_modal()
    time.sleep(10)
    browser.close_browser()
    

if __name__ == "__main__":
    main()