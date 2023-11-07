from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_bundle import SeleniumBundle
from selenium_driver import SeleniumDriver


class SeleniumController:

    def __init__(self, bundle: SeleniumBundle = SeleniumBundle()):
        self.bundle = bundle
        self.options = webdriver.ChromeOptions()
        [self.options.add_argument(arg) for arg in self.bundle.driver_args]
        [self.options.add_experimental_option(key, value) for key, value in self.bundle.experimental_args.items()]
        self.service = Service(executable_path=self.bundle.driver_path)
        self.browser = webdriver.Chrome(
            options=self.options,
            service=self.service
        )

    def start_scrapping(self) -> []:
        self.browser.get(self.bundle.url)
        # Closing google consent window
        WebDriverWait(self.browser, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, self.bundle.decline_cookie_class))).click()
        sd = SeleniumDriver(self.bundle, self.browser)
        return sd.get_all_reviews()
