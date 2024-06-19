from lib.methods import get_all_html_elements, Browser

import json

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