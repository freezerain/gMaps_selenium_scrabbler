import traceback
from time import sleep

from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from selenium_bundle import SeleniumBundle
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SeleniumDriver:
    bundle: SeleniumBundle = SeleniumBundle()

    def __init__(self, bundle: SeleniumBundle, browser: WebDriver):
        self.bundle = bundle
        self.browser = browser
        self.wait = WebDriverWait(browser, timeout=10, poll_frequency=0.5,
                                  ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])

    def get_all_reviews(self):
        return self._get_review_list()

    def _get_review_list(self):

        review_scroll_list_element = WebDriverWait(self.browser, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.bundle.review_scroll_list_class)))

        review_index_counter = 1
        review_list = []
        while True:
            try:  # Load review block
                current_review = self.wait.until(
                    lambda d: review_scroll_list_element.
                    find_element(By.XPATH,
                                 f"(.//div[{self.bundle.cl_templ.format(c=self.bundle.review_block_class)}])[{str(review_index_counter)}]"))
                try:
                    ActionChains(self.browser).scroll_to_element(current_review).perform()
                except StaleElementReferenceException as e:
                    pass
                # sleep to sync api calls
                review_list.append(self._parse_review(current_review))
                sleep(0.1)
                try:  # scroll review list to load more reviews
                    scroll_origin = ScrollOrigin.from_element(current_review)
                    ActionChains(self.browser).scroll_from_origin(scroll_origin, 0, 2000).perform()
                except StaleElementReferenceException as e:
                    pass
                sleep(0.1)
                review_index_counter += 1
            except TimeoutException as e:
                print(f"No more reviews found. Last count:{review_index_counter}")
                break
        return review_list

    # function-extension of base_element.find_element
    # that return None if element not found

    def _parse_review(self, current_review: WebElement):
        try:
            # click translate/more button to expand
            self._expand_review(current_review)
            # collect respond and click translate/expand of respond
            respond = self._get_response_text(current_review)

            # parse rest of the data
            author = current_review.find_element(By.CLASS_NAME, self.bundle.review_author_class).text
            stars = current_review.find_element(By.CLASS_NAME, self.bundle.review_stars_class).get_attribute(
                "aria-label")
            date = current_review.find_element(By.CLASS_NAME, self.bundle.review_date_class).text
            review_text = ""
            try:
                review_text = current_review.find_element(By.XPATH,
                                                          f".//span[{self.bundle.cl_templ.format(c=self.bundle.text_span_class)}]").text
            except NoSuchElementException as e:
                pass
            return {"author": author, "stars": stars, "date": date, "review": review_text, "respond": respond}
        except Exception as e:
            print(traceback.format_exc())
            print("---Parse failed---")

    def _expand_review(self, current_review: WebElement):

        try:
            current_review.find_element(By.XPATH,
                                        f".//button[{self.bundle.cl_templ.format(c=self.bundle.translate_btn_class)}]").click()
        except NoSuchElementException as e:
            try:
                current_review.find_element(By.XPATH,
                                            f".//button[{self.bundle.cl_templ.format(c=self.bundle.more_btn_class)}]").click()
            except NoSuchElementException as e:
                pass
        finally:
            try:
                ActionChains(self.browser).scroll_to_element(current_review).perform()
            except StaleElementReferenceException as e:
                pass

    def _get_response_text(self, current_review: WebElement):
        respond = ""
        # translate respond if possible
        try:
            current_review.find_element(By.XPATH,
                                        f".//div[{self.bundle.cl_templ.format(c=self.bundle.response_block_class)}]//button[{self.bundle.cl_templ.format(c=self.bundle.translate_btn_class)}]").click()
        except NoSuchElementException as e:
            # expand respond if possible
            try:
                current_review.find_element(By.XPATH,
                                            f".//div[{self.bundle.cl_templ.format(c=self.bundle.response_block_class)}]//button[{self.bundle.cl_templ.format(c=self.bundle.more_btn_class)}]").click()
            except NoSuchElementException as e:
                pass
        finally:
            try:
                ActionChains(self.browser).scroll_to_element(current_review).perform()
            except StaleElementReferenceException as e:
                print("---Cant scroll - stale element---")
            try:
                # parse respond if possible
                # wait for text update???
                # sleep(0.1)
                respond = current_review.find_element(By.XPATH,
                                                      f".//div[{self.bundle.cl_templ.format(c=self.bundle.response_block_class)}]//div[{self.bundle.cl_templ.format(c=self.bundle.text_span_class)}]").text
            except NoSuchElementException as e:
                # print("---respond not found---")
                pass
        return respond


def _find_element_with_exception(base_element, xpath):
    try:
        return base_element.find_element(By.XPATH, xpath)
    except NoSuchElementException as e:
        return None
