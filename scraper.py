import os
import subprocess
import sys

# Install Selenium

# Install Chrome and ChromeDriver
# os.system("sudo apt-get update")
##### These lines do not work in the current environment #####
# os.system("sudo apt-get install libxss1 libappindicator1 libindicator7")
# os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
# os.system("sudo apt install ./google-chrome*.deb")
# os.system("CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)")
###############################################################################
# # Just download the chromedriver that is compatible with the current Chrome version (or be geeky and automate it)
# # here: https://developer.chrome.com/docs/chromedriver/downloads
# os.system("wget -N https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.141/linux64/chromedriver-linux64.zip")
# os.system("unzip chromedriver-linux64.zip -d chromedriver")
# os.system("rm chromedriver-linux64.zip")
# os.system("sudo mv chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver")
# os.system("rm -r chromedriver")

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import google.generativeai as genai

URL = "https://education.securiti.ai/certifications/privacyops/introduction/privacyops-overview/"
CLASSNAME = "ld-tab-content"

def get_all_links(url: str, output_file: str) -> None:
    # file
    file_handle = open(output_file, 'w')
    

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Set up ChromeDriver service
    webdriver_service = Service("/usr/local/bin/chromedriver")

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Open a website
    driver.get(url)

    # Get the page source
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all 'a' tags
    links = soup.find_all('a')

    # Print all the links
    for link in links:
        file_handle.write(link.get('href') + '\n')

    # Close the browser
    driver.quit()


def get_full_html_element(page_url: str, element_class: str, save_path: str) -> list:
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Set up ChromeDriver service
    webdriver_service = Service("/usr/local/bin/chromedriver")

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Open a website
    driver.get(page_url)

    # Get the page source
    html = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with the specified class
    elements = soup.find_all(class_=element_class)
    file = open(save_path, 'w')
    for element in elements:
        file.write(str(element))

    # Close the browser
    driver.quit()

    return elements


def ai_file_prompt(prompt, file_path) -> None:
    text_file = genai.upload_file(path=file_path)

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

    response = model.generate_content([prompt, text_file])
    output_path = [file_path.split('.')[0] + '_correct.' + file_path.split('.')[1]]
    print(response)
    with open(output_path[0], 'w') as f:
        f.write(response.text)

# genai.configure(api_key="AIzaSyDejoy5ri5frO5JR_PLkQtvShyDBFiYEtE")
# prompt = "Correct the grammatical errors in the the text inside html tags and return the whole text."
# file_path = 'output.txt'
# ai_file_prompt(prompt, file_path)


get_all_links(URL, "links.txt")
