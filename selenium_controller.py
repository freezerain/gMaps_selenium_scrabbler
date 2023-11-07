from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
# Make browser open in background
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_bundle import SeleniumBundle


class SeleniumController:

    def __init__(self, bundle: SeleniumBundle = SeleniumBundle()):
        self.bundle = bundle
        self.options = webdriver.ChromeOptions()
        [self.options.add_argument(arg) for arg in self.bundle.driver_args]
        [self.options.add_experimental_option(key, value) for key, value in self.bundle.experimental_args]
        self.service = Service(executable_path=self.bundle.driver_path)
        self.browser = webdriver.Chrome(
            options=self.options,
            service=self.service
        )

    def start_scrapping(self):
        self.browser.get(self.bundle.url)
        # Closing google consent window
        WebDriverWait(self.browser, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, self.bundle.decline_cookie_class))).click()
