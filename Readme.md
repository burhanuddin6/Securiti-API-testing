### Sanity
- Please make sure that exceptions are handled (please used named exceptions like selenium.exceptions.staleelementerror)
- Please use better naming

### Please create a virtual environment and install dependencies:
```
python3 -m venv env # create a folder named env
```
```
source env/bin/activate # this activates virtual environment
```
Install dependencies after activating virtual environment
```
python3 -m pip install -r requirements.txt
```
For deactivating virtual environment:
```
deactivate
```
Make sure to run all the files in this repo with virtual environemnt activated. After installing any external library, make sure to add it in requirements.txt:
```
python -m pip freeze > requirements.txt
```
### Please create data.json file before running sraper.py:
```
{
    "email": "your email",
    "password": "your password"
}
```
### Known Issues (need to be fixed later)

-  The click_element_and_handle_new_tab function in methods.py line shown below causes stale element reference error for one webelement which is unexpected (this may be caused by an issue in the application itself). This issue can be mitigated by passing just the location and size of the div (storing those values before the first click) to the click_element_at_coordinates function but that causes the whole program to behave unexpectedly. Therefore its better that an exception is raised for that single webelement and handling that exception in a way that the program progresses without affecting other parts.
```
self.click_element_at_coordinates(div)
```
```
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
                    self.click_element_at_coordinates(div)
            time.sleep(5) # wait for close modal or interaction
        return ret_dict
    except Exception as e:
        raise e

```