from drivers import check_and_install_chrome_driver

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import time

URL = "https://education.securiti.ai/certifications/privacyops/introduction/privacyops-overview/"
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

        time.sleep(5)

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


def main():
    print(get_all_html_elements(URL, "tag", 'a'))

if __name__ == "__main__":
    main()