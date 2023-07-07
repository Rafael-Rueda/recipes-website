from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / 'chromedriver.exe'


chrome_options = webdriver.ChromeOptions()
# Options
# chrome_options.add_argument('--headless')

chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))

def make_browser():
    web_browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return web_browser
