import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from anytree import NodeMixin, RenderTree, Node

class WebElementNode(NodeMixin):
    def __init__(self, name, curr_url: str, element: WebElement=None, parent=None, children=None):
        super(WebElementNode, self).__init__()
        self.name = name
        self.url = curr_url
        if element is not None:
            self.tag_name = element.tag_name
            self.attributes = self.extract_attributes(element)
            self.innerHTML = element.get_attribute("innerHTML")
            self.outerHTML = element.get_attribute("outerHTML")
            self.location = element.location
            self.element_size = element.size
        else:
            # a special node. Maybe root?
            self.tag_name = None
            self.attributes = {}
            self.innerHTML = None
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return f"WebElementNode(name={self.name}, url={self.url}, tag_name={self.tag_name}, attributes={self.attributes})"

    def relocate_element(self, driver: webdriver.Chrome):
        if driver.current_url != self.url:
            print(driver.current_url, self.url)
            raise ValueError("The current url does not match the url of this node")
        xpath = self._generate_xpath()
        elements = driver.find_elements(By.XPATH, xpath)
        if len(elements) == 1:
            return elements[0]
        else:
            for element in elements:
                # if element.location == self.location and element.size == self.element_size:
                if element.get_attribute("outerHTML") == self.outerHTML:
                    return element
        raise ValueError("Could not find the element with the same outerHTML")

    def _generate_xpath(self):
        xpath = f"//{self.tag_name}"
        conditions = [f"@{key}='{value}'" for key, value in self.attributes.items()]
        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"
        return xpath

    @staticmethod
    def extract_attributes(element):
        return {attr['name']: attr['value'] for attr in element.get_property("attributes")}
    
    def __repr__(self):
        return f"WebElementNode(name={self.name}, url={self.url}, tag_name={self.tag_name}, attributes={self.attributes})"
    
    def __str__(self) -> str:
        return f"WebElementNode(name={self.name}, url={self.url}, tag_name={self.tag_name}, attributes={self.attributes})"

    @staticmethod
    def nodeattrfunc(node):
        return f'label="{node.name}\n{node.url}\n{node.tag_name}\n{node._generate_xpath()}", shape=box, style=filled, fillcolor=lightblue'


if __name__ == "__main__":

    # Creating nodes
    root = WebElementNode("root", "https://qa.securiti.xyz")
    child1 = WebElementNode("child1", "https://qa.securiti.xyz")
    child2 = WebElementNode("child2", "https://qa.securiti.xyz")
    grandchild1 = WebElementNode("grandchild1", "https://qa.securiti.xyz", parent=child1)
    root.children = [child1, child2]

    # Displaying the using render
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))