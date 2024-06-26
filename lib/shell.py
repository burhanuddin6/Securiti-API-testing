import cmd
from lib.web_element_node import WebElementNode, save_tree_to_file, load_tree_from_file
from anytree import RenderTree
from lib.config import config
from lib.browser_methods import Browser
from anytree.exporter import UniqueDotExporter
import time

class MyShell(cmd.Cmd):
    intro = "Welcome to the Securiti UI Automation shell. Type help or ? to list commands.\n"
    prompt = "(securiti-automation) "

    def __init__(self):
        super().__init__()
        self.current_tree = None
        self.current_node = None
        self.browser = Browser()

    def do_load(self, arg):
        """Loads tree from a Json file 
        Usage: load filename
        """
        try:
            self.current_tree = load_tree_from_file(arg)
            self.current_node = self.current_tree
            print(f"Tree loaded from {arg}")
        except Exception as e:
            print(f"Error loading tree: {e}")

    def do_save(self, arg):
        "Save the current tree to a file: save filename"
        if self.current_tree:
            try:
                save_tree_to_file(self.current_tree, arg)
                print(f"Tree saved to {arg}")
            except Exception as e:
                print(f"Error saving tree: {e}")
        else:
            print("No tree to save.")

    def do_self_discover(self, arg):
        "Discover the current tree"
        ret = False
        necessary_variables = [
            'clickable_xpaths', 
            'close_modal_xpaths', 
            'credentials_file', 
            'traverse_site_logfile', 
            'max_depth', 
            'url'
            ]
        
        for var in necessary_variables:
            if not config[var]:
                print(f"Please define {var} variable in config.yaml")
                ret = True
                
        if ret:
            return
        
        try:
            self.current_tree = WebElementNode(name="root", curr_url=config['url'])
            self.browser.open_securiti_page(config['url'])

            self.browser.traverse_site(xpaths=config['clickable_xpaths'], root=self.current_tree, urls_explored=set(), depth=1)
            time.sleep(10)

            # display the tree in an image UniqueDotExporter
            UniqueDotExporter(self.current_tree, nodeattrfunc=WebElementNode.nodeattrfunc).to_picture("tree.svg")
            save_tree_to_file(self.current_tree, "tree.json")
            
        except Exception as e:
            print(f"Error discovering url {arg}:\n{e}")


    def do_show(self, arg):
        "Show the current tree"
        if self.current_tree:
            for pre, fill, node in RenderTree(self.current_tree):
                print("%s%s" % (pre, node.name))
        else:
            print("No tree to show.")

    def do_exit(self, arg):
        """Exit the shell
        Usage: exit
        """
        print("Exiting...")
        return True

