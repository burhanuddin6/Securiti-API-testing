from lib.drivers import check_and_install_chrome_driver

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
    
    
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle
import os

URL = "https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html"
CLASSNAME = "ld-tab-content"
COOKIES_FILE = "cookies.pkl"

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
    
    def get_element(self, by:By, value: str):
        return self.driver.find_element(by, value)

    def get_all_elements(self, by:By, value: str):
        return self.driver.find_elements(by, value)

    def add_input(self, by: By, value: str, input_text: str):
        element = self.driver.find_element(by, value)
        element.send_keys(input_text)
        time.sleep(1)

    def click_element(self, by: By, value: str):
        element = self.driver.find_element(by, value)
        element.click()
        time.sleep(1)

    def is_logged_in(self):
        try:
            self.driver.find_element(By.XPATH, "//input[@id='email']")
            return False
        except:
            return True

    def login_securiti(self, email: str, password: str, xpath_after_login: str):
        wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds

        self.add_input(by=By.ID, value="email", input_text=email)
        self.click_element(by=By.XPATH, value="//button[@type='submit']")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        
        self.add_input(by=By.XPATH, value="//input[@type='password']", input_text=password)
        self.click_element(by=By.XPATH, value="//button[@type='submit']")
        
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_after_login)))
        
        self.save_cookies()


    def save_cookies(self):
        with open(COOKIES_FILE, 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self):
        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

    # def get_all_html_elements(self, by: str, value: str):
    #     '''Find all HTML elements by a certain attribute (class, id, name, etc.)'''
    #     try:
    #         # Get the page source
    #         html = self.driver.page_source

    #         # Parse the HTML with BeautifulSoup
    #         soup = BeautifulSoup(html, 'html.parser')

    #         # Find elements based on the 'by' and 'value' provided
    #         if by == 'tag':
    #             elements = soup.find_all(value)
    #         elif by == 'class':
    #             elements = soup.find_all(class_=value)
    #         elif by == 'id':
    #             elements = soup.find_all(id=value)
    #         else:
    #             elements = soup.find_all(attrs={by: value})
        
    #         return elements
        
    #     except:
    #         raise ValueError("An Exception Occurred. Cannot complete the operation get_all_html_elements")
    

if __name__ == "__main__":
    pass
