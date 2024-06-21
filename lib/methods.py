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
import json

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

        # set the driver to wait for every page to fully load
        # self.driver.implicitly_wait(10)

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
    
    def extract_links_securiti(self, url: str, xpath_for_redirect_load: str, xpath_for_urls: str, file_name: str, link_format_func: callable = lambda x: x):
        '''Goes to the securities website and extracts all the links from the page
        and writes them to a file.
        xpath_for_urls: xpath for the urls based on the target page
        file_name: name of the file to write the urls to
        '''
        # read data.json as a dictionary
        with open("lib/data.json", 'r') as file:
            data = json.load(file)
        
        self.open_page(url)
        # login and wait for the page to load (wait for the li element to be present)
        if not self.is_logged_in():
            self.login_securiti(data["email"], data["password"], xpath_for_redirect_load)
            time.sleep(5)
        else:
            time.sleep(5)
            # this is not working
            # TODO: fix this. Doesn't always want to wait for 10s if the page is already loaded
            # WebDriverWait(self.driver, 10).until(
            #     lambda driver: driver.execute_script("return document.readyState") == "complete"
            # )

        li = self.get_all_elements(By.XPATH, xpath_for_urls)
        print([i.get_attribute("outerHTML") for i in li])
        links = [link_format_func(i.get_attribute("href")) for i in li]
        links = list(set(links))

        # write to data_intelligence_links.txt
        with open(file_name, 'a') as file:
            for link in links:
                file.write(link + "\n")

if __name__ == "__main__":
    pass
