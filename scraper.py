from lib.methods import get_all_html_elements

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
CLASSNAME = "ld-tab-content"

def get_all_links(url: str, output_file: str, ) -> None:
    # get all list item html elements
    li_elements = get_all_html_elements(URL, "tag", "body")

    print(li_elements)
    # file
    file_handle = open(output_file, 'w')
    file_handle.write(str(li_elements[0]))

def main():
    get_all_links(URL, "links.txt")

if __name__ == "__main__":
    main()