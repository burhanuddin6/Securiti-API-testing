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

username = 'batool@shan.stack'
password = 'Dino@23sxc077173'

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


# Create output directory if it doesn't exist
output_dir = 'extracted_elements'
os.makedirs(output_dir, exist_ok=True)
image_dir = os.path.join(output_dir, 'images')
os.makedirs(image_dir, exist_ok=True)

# Initialize files for different elements
header_file = open(os.path.join(output_dir, 'headers.txt'), 'w', encoding='utf-8')
paragraph_file = open(os.path.join(output_dir, 'paragraphs.txt'), 'w', encoding='utf-8')
list_file = open(os.path.join(output_dir, 'lists.txt'), 'w', encoding='utf-8')
table_file = open(os.path.join(output_dir, 'tables.txt'), 'w', encoding='utf-8')
image_file = open(os.path.join(output_dir, 'images.txt'), 'w', encoding='utf-8')
link_file = open(os.path.join(output_dir, 'links.txt'), 'w', encoding='utf-8')
code_file = open(os.path.join(output_dir, 'codes.txt'), 'w', encoding='utf-8')

# Extract and format the text content
for element in soup.find_all(True):  # True matches all tags

    if element.name in ['h1', 'h2', 'h3']:
        paragraph_file.write(f'{element.get_text()}\n')

    elif element.name == 'p':
        paragraph_file.write(f'{element.get_text()}\n')

    elif element.name in ['ul', 'ol']:
        list_items = element.find_all('li')
        for li in range(len(list_items)):
            paragraph_file.write(f' {li}. {list_items[li].get_text()}\n')
        paragraph_file.write('\n')

    elif element.name == 'table':
        rows = element.find_all('tr')
        table_text = ''
        for row in rows:
            cells = row.find_all(['td', 'th'])
            cell_text = [cell.get_text().strip() for cell in cells]
            table_text += ' | '.join(cell_text) + '\n'
        table_file.write(table_text + '\n')

    elif element.name == 'a':
        link_href = element.get('href')
        link_text = element.get_text().strip()
        if link_href:
            link_file.write(f'{link_text} ({link_href})\n')
          
    elif element.name == 'img':
        img_src = element.get('src')
        image_file.write(img_src + '\n')
  
    elif element.name == 'code':
        code_file.write(element.get_text()+'/n'+'/n')
        

# Close all files
header_file.close()
paragraph_file.close()
list_file.close()
table_file.close()
image_file.close()
link_file.close()
code_file.close()

print(f'text content saved to {output_dir}')

# Close the WebDriver
driver.quit()
