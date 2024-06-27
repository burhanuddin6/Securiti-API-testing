from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote
import requests
import pandas as pd

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Set up ChromeDriver service
service = Service('/usr/local/bin/chromedriver')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

#-----------------------------------------------------Login Page--------------------------------------------------------------------#

login_url = 'https://qa.securiti.xyz/#/login?redirect=%2Fhelp-center'  
driver.get(login_url)

username = ''
password = ''

# locating username element
username_elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'email'))
)
username_elem.send_keys(username)

# Locate and click "Continue" button using type attribute
continue_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))  # Adjust CSS selector as per your HTML
)
continue_button.click()

# locating password element
password_elem = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]'))
)
password_elem.send_keys(password)

# Locate and click "submit" button using type attribute
submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))  # Adjust CSS selector as per your HTML
)
submit_button.click()

expected_url_after_submit = 'https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/data-intelligence-target.html'  
WebDriverWait(driver, 10).until(EC.url_to_be(expected_url_after_submit))

#--------------------------------------------------API Documentation-------------------------------------------------------------#
next_page_url = 'https://qa-helpcenter.securiti.xyz/modules/data-intelligence/en/sensitive-data-intelligence-api-reference.html'
driver.get(next_page_url)
WebDriverWait(driver, 10).until(EC.url_to_be(next_page_url))

external_url_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//a[@class="link"]'))  
)
external_url = external_url_element.get_attribute('href')
driver.get(external_url)
WebDriverWait(driver, 10).until(EC.url_to_be(external_url))


# print(driver.current_url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="sc-cKRKFl cLybRg"]'))
)

#------------------------------------------------------------Scraping------------------------------------------------------------#
# Extract page source
page_source = driver.page_source

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

def extract_text_from_single_div(div_section):
    return ' '.join(div_section.stripped_strings)

def extract_data_from_all_divs(soup, div_classes):
    all_data = {div_class: [] for div_class in div_classes}
    
    for div_class in div_classes:
        div_sections = soup.find_all(div_class[0], class_=div_class[1])
        if div_class[1] == 'sc-hKFxyN gHYYBK':
            div_sections=div_sections[11:]
        elif div_class[1] == 'sc-pNWdM loDKCl':
            div_sections=div_sections[8:]

        class_data = []
        for div_section in div_sections:
            text = extract_text_from_single_div(div_section)
            class_data.append(text)
           
        all_data[div_class] = class_data
    return all_data

div_classes = [('h2', 'sc-pNWdM loDKCl'), ('div','sc-eWnToP jGgSbx'), ('div', 'redoc-json')]
data = extract_data_from_all_divs(soup, div_classes)

max_len = max(map(len, data.values()))
for key, value in data.items():
    if len(value) < max_len:
        value.extend([''] * (max_len - len(value)))

df = pd.DataFrame(data)

# Store data in a CSV/Excel file
df.to_csv('extracted_data.csv', index=False, header = False)


print('Data extraction and storage completed successfully.')

# Close the WebDriver
driver.quit()

