from lib.drivers import check_and_install_chrome_driver

# Selenium script to extract links
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

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



def main():
    check_and_install_chrome_driver()
    get_all_links(URL, "links.txt")

if __name__ == "__main__":
    main()