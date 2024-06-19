from drivers import check_and_install_chrome_driver

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import json

import time

URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
CLASSNAME = "ld-tab-content"


def get_all_html_elements(url: str, by: str, value: str):
    '''Find all HTML elements by a certain attribute (class, id, name, etc.)'''

    # Check if chromedriver is installed, if not install it
    check_and_install_chrome_driver()

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the website
        driver.get(url)  

        # Get the page source
        html = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find elements based on the 'by' and 'value' provided
        if by == 'tag':
            elements = soup.find_all(value)
        elif by == 'class':
            elements = soup.find_all(class_=value)
        elif by == 'id':
            elements = soup.find_all(id=value)
        elif by == 'name':
            elements = soup.find_all(attrs={"name": value})
        else:
            elements = soup.find_all(attrs={by: value})
        
        return elements

    except:
        return ValueError("An Exception Occurred. Cannot complete the operation get_all_html_elements")
    finally:
        # Close the WebDriver
        driver.quit()


class Browser():
    def __init__(self) -> None:
        # Check if chromedriver is installed, if not install it
        check_and_install_chrome_driver()

        # Set up Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def open_page(self, url: str):
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()

    def add_cookie(self, cookie: dict):
        self.driver.add_cookie(cookie)
    
    def add_input(self, by: By, value: str, input_text: str):
        element = self.driver.find_element(by, value)
        element.send_keys(input_text)
        time.sleep(1)

    def click_element(self, by: By, value: str):
        element = self.driver.find_element(by, value)
        element.click()
        time.sleep(1)

    def login_securiti(self, email: str, password: str):
        self.add_input(by=By.ID, value="email", input_text=email)
        self.click_element(by=By.XPATH, value="//button[@type='submit']")
        self.add_input(by=By.XPATH, value="//input[@type='password']", input_text=password)
        self.click_element(by=By.XPATH, value="//button[@type='submit']")
        time.sleep(50)
    

def main():
    # read data.json as a dictionary
    with open("lib/data.json", 'r') as file:
        data = json.load(file)
    # print(get_all_html_elements(URL, "tag", 'input'))
    browser = Browser()
    browser.open_page(URL)
    browser.login_securiti(data["email"], data["password"])
    browser.close_browser()
if __name__ == "__main__":
    main()