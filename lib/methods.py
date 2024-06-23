from lib.drivers import check_and_install_chrome_driver
from lib.node import WebElementNode

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
    
    
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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

    def open_securiti_page(self, url: str, xpath_for_redirect_load: str=None):
        self.driver.get(url)
        # read data.json as a dictionary
        with open("lib/data.json", 'r') as file:
            data = json.load(file)
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

    def login_securiti(self, email: str, password: str, xpath_after_login: str=None):
        wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds

        self.add_input(by=By.ID, value="email", input_text=email)
        self.click_element(by=By.XPATH, value="//button[@type='submit']")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        
        self.add_input(by=By.XPATH, value="//input[@type='password']", input_text=password)
        self.click_element(by=By.XPATH, value="//button[@type='submit']")
        
        if xpath_after_login:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath_after_login)))
        else:
            time.sleep(10)
        
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
    def check_and_close_modal(self):
        '''Checks all close buttons and returns after one
        successful click. It can be the case that no close buttons
        are found or none are clickable.
        '''
        close_xpath = "//*[contains(@class, 'close')] | //*[contains(text(), 'Close')]"
        closures = self.get_all_elements(By.XPATH, close_xpath)
        # check if any is clickable and then click
        for closure in closures:
            try:
                closure.click()
                return True # close if a single close button is clicked
            except Exception as e:
                print(str(e).split("\n")[0])
        return False
    

    def extract_links_securiti(self, url: str, xpath_for_urls: str, file_name: str, xpath_for_redirect_load: str=None, link_format_func: callable = lambda x: x):
        '''Goes to the securities website and extracts all the links from the page
        and writes them to a file.
        url: url of the page to open and extract links from
        xpath_for_urls: xpath for the urls based on the target page
        file_name: name of the file to write the urls to
        xpath_for_redirect_load: xpath for the element to wait for before proceeding. If not provided, it will wait for 10s
        link_format_func: function to format the link before writing to the file
        '''
        
        self.open_securiti_page(url, xpath_for_redirect_load)

        li = self.get_all_elements(By.XPATH, xpath_for_urls)
        links = [link_format_func(i.get_attribute("href")) for i in li]
        links = list(set(links))

        # write to data_intelligence_links.txt
        with open(file_name, 'a') as file:
            for link in links:
                file.write(link + "\n")
    
    def click_element_at_coordinates(self, location, size):
        '''Clicks on an element at its specific coordinates, bypassing any overlays'''
        action = ActionChains(self.driver)
        x = location['x'] + size['width'] / 2
        y = location['y'] + size['height'] / 2
        action.move_by_offset(x, y).click().perform()
        action.reset_actions()  # Reset the action to prevent offset issues in further actions
        time.sleep(1)  # Wait for the click to be processed

    def click_element_and_handle_new_tab(self, div, urls_explored: set):
        ret_dict = {'reload_elements': False}
        try:
            curr_page_url = self.driver.current_url
            urls_explored.add(curr_page_url)
            # check if div is interactable
            if not div.is_displayed():
                return ret_dict
            # extract location and size before clicking
            location = div.location
            size = div.size
            div.click()
            time.sleep(5)  
            # check if url has changed
            new_page_url = self.driver.current_url
            if new_page_url != curr_page_url:
                time.sleep(5)
                # there can be multiple redirects so we need to go back to the original page
                while self.driver.current_url != curr_page_url:
                    self.driver.back()
                    time.sleep(5)
                ret_dict['reload_elements'] = True
                # if new_page_url in urls_explored:
                #     # use browser back button
                #     self.driver.back()
                #     return
                # else:
                #     self.traverse_site() # Recursively handle the new page
                # pass
            else:
                if not self.check_and_close_modal():
                # add logic of interacting with the elemnet in try except block
                    try:
                        div.click()
                    except:
                        self.click_element_at_coordinates(dive)
                time.sleep(5) # wait for close modal or interaction
            return ret_dict
        except Exception as e:
            raise e

    def handle_modal_or_interaction(self):
        '''Implement handling of modals or other interactions if needed'''
        pass
    
    def traverse_site(self, xpaths: list[str], root: WebElementNode=None):
        '''Traverse the site by clicking on all divs that contain only text'''
        clickable_elements = []
        [(clickable_elements.extend(self.get_all_elements(By.XPATH, xpath))) for xpath in xpaths]
        # print all html attributes
        # automatically attaches these nodes to root
        [WebElementNode(name=(str(root.name) + '_' + str(i)), curr_url=self.driver.current_url, element=element, parent=root) for i, element in enumerate(clickable_elements)]
        # write outer html of all elemnts to traverse_site.temp.txt 
        with open("traverse_site.temp.txt", 'w') as file:
        
            page_urls = set()
            for node in root.children:
                try:
                    # incase the url changes, reload the elements in order to avoid stale element exception
                    # this assumes that the original page is restored by click_element_and_handle_new_tab function
                    # through the browser back button
                    # not that value of i does not change so the loop will continue from the same index
                    element = node.relocate_element(self.driver)
                    file.write(element.get_attribute("outerHTML") + "\n\n")
                    self.click_element_and_handle_new_tab(element, page_urls)
                except Exception as e:
                    # write the exception title to file
                    file.write(f"Exception occurred: {str(e).split('\n')[0]}\n\n")


if __name__ == "__main__":
    pass
