import os
import subprocess
import sys

def install_chrome() -> str:
    '''Installs chrome if not already installed and returns version'''
    try: 
        output = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8").strip()
    except: # FileNotFoundError
        print("Not found")
        # Install Chrome and ChromeDriver
        os.system("sudo apt-get update")
        os.system("sudo apt-get install libxss1 libappindicator1 libindicator7")
        os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        os.system("sudo apt install ./google-chrome*.deb")
        output = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8").strip()

    version = output.split()[-1]
    return version

###############################################################################
# # Just download the chromedriver that is compatible with the current Chrome version (or be geeky and automate it)
# # here: https://developer.chrome.com/docs/chromedriver/downloads

def install_chrome_driver(version: str):
    """Installs chrome driver from the version given. Note that this straightforward way is not rigorous"""
    os.system(f"wget -N https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip")
    os.system("unzip chromedriver-linux64.zip -d chromedriver")
    os.system("rm chromedriver-linux64.zip")
    os.system("sudo mv chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver")
    os.system("rm -r chromedriver")


# def check_and_install_chrome_driver() -> bool:
#     """Checks if chrome web driver is installed. If not installs it.
#     """
#     try:
#         output = subprocess.check_output(["chromedriver", "--version"]).decode("utf-8").strip()
#         return True
#     except FileNotFoundError:
#         version = install_chrome()
#         install_chrome_driver(version)

# better to use device-agnostic library
def check_and_install_chrome_driver():
    '''Check if chromedriver is installed, if not install it.'''
    try:
        # Check if chromedriver is already installed
        subprocess.run(["chromedriver", "--version"], check=True)
    except: # subprocess.CalledProcessError:
        # If chromedriver is not installed, install it
        subprocess.run([sys.executable, "-m", "pip", "install", "chromedriver-autoinstaller"])
        import chromedriver_autoinstaller
        chromedriver_autoinstaller.install()
        