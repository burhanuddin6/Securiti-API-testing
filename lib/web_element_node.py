from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from anytree import NodeMixin, RenderTree
import json
from selenium.webdriver.remote.webelement import WebElement

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
            self.outerHTML = None
            self.location = None
            self.element_size = None

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

    def to_dict(self):
        """Convert the node and its children to a dictionary."""
        data = {
            "name": self.name,
            "url": self.url,
            "tag_name": self.tag_name,
            "attributes": self.attributes,
            "innerHTML": self.innerHTML,
            "outerHTML": self.outerHTML,
            "location": self.location,
            "element_size": self.element_size,
            "children": [child.to_dict() for child in self.children] if self.children else []
        }
        return data

    @staticmethod
    def from_dict(data, parent=None):
        """Create a WebElementNode from a dictionary."""
        node = WebElementNode(
            name=data["name"],
            curr_url=data["url"],
            parent=parent
        )
        node.tag_name = data["tag_name"]
        node.attributes = data["attributes"]
        node.innerHTML = data["innerHTML"]
        node.outerHTML = data["outerHTML"]
        node.location = data["location"]
        node.element_size = data["element_size"]
        if "children" in data:
            for child_data in data["children"]:
                WebElementNode.from_dict(child_data, parent=node)
        return node

    @staticmethod
    def nodeattrfunc(node):
        return f'label="{node.name}\n{node.url}\n{node.tag_name}\n{node._generate_xpath()}", shape=box, style=filled, fillcolor=lightblue'

def save_tree_to_file(root, file_path):
    """Save the tree to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(root.to_dict(), f, indent=4)

def load_tree_from_file(file_path):
    """Load the tree from a JSON file and return the root node."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return WebElementNode.from_dict(data)

# Example usage
if __name__ == "__main__":

    # Creating nodes
    root = WebElementNode("root", "https://qa.securiti.xyz")
    child1 = WebElementNode("child1", "https://qa.securiti.xyz", parent=root)
    child2 = WebElementNode("child2", "https://qa.securiti.xyz", parent=root)
    grandchild1 = WebElementNode("grandchild1", "https://qa.securiti.xyz", parent=child1)

    # Displaying the tree using RenderTree
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    # Save the tree to a file
    save_tree_to_file(root, "tree.json")

    # Load the tree from the file
    loaded_root = load_tree_from_file("tree.json")

    # Display the loaded tree using RenderTree
    for pre, fill, node in RenderTree(loaded_root):
        print("%s%s" % (pre, node.name))
