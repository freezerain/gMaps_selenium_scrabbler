# Import the library Selenium
import traceback
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Make browser open in background
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument("−−lang=es")
options.add_argument("−−accept-lang=es")
options.add_experimental_option('prefs', {'intl.accept_languages': 'es,es_ES'})

# Create the webdriver object
service = Service(executable_path="C:/chromedriver_win32/chromedriver.exe")
browser = webdriver.Chrome(
    options=options,
    service=service
)

# Obtain the Google Map URL
url = "https://www.google.es/maps/place/RESTAURANT+TORRE+MIRONA/@41.9675449,2.7828756,16z/data=!4m8!3m7!1s0x12baddfe6c57ccbb:0x6558d8c865e0e3bd!8m2!3d41.9669495!4d2.7737607!9m1!1b1!16s%2Fg%2F11c1qlc0np?entry=ttu"
browser.get(url)

wait = WebDriverWait(browser, timeout=10, poll_frequency=0.5,
                     ignored_exceptions=[NoSuchElementException, StaleElementReferenceException])
# Closing google consent window
declineButtonXpath = "//button[@jsname='tWT92d']"
btnDiv = WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, declineButtonXpath)))
btnDiv.click()

cl_templ = "contains(concat(' ', normalize-space(@class), ' '), ' {c} ')"


def get_review_list():
    # Element classes to lookup
    review_block_class = "jJc9Ad"
    review_scroll_list_class = "DxyBCb"
    review_scroll_list_element = WebDriverWait(browser, timeout=10).until(
        EC.presence_of_element_located((By.CLASS_NAME, review_scroll_list_class)))

    review_index_counter = 1
    review_list = []
    while True:
        try:  # Load review block
            print(f"Searching for next review, index: {review_index_counter}")
            current_review = wait.until(
                lambda d: review_scroll_list_element.
                find_element(By.XPATH,
                             f"(.//div[{cl_templ.format(c=review_block_class)}])[{str(review_index_counter)}]"))
            try:
                ActionChains(browser).scroll_to_element(current_review).perform()
            except StaleElementReferenceException as e:
                print("---Cant scroll - stale element---")
            # sleep to sync api calls
            review_list.append(parse_review(current_review))
            sleep(0.1)
            try:  # scroll review list to load more reviews
                scroll_origin = ScrollOrigin.from_element(current_review)
                ActionChains(browser).scroll_from_origin(scroll_origin, 0, 2000).perform()
            except StaleElementReferenceException as e:
                print("---Cant scroll - stale element---")
            sleep(0.1)
            review_index_counter += 1
        except TimeoutException as e:
            print(f"No more reviews found. Last count:{review_index_counter}")
            break
    return review_list


def parse_review(current_review: WebElement):
    print("Parsing begins...")
    try:
        # click translate/more button to expand
        expand_review(current_review)
        # collect respond and click translate/expand of respond
        respond = get_response_text(current_review)

        # parse rest of the data
        author = current_review.find_element(By.CLASS_NAME, "d4r55 ").text
        stars = current_review.find_element(By.CLASS_NAME, "kvMYJc ").get_attribute("aria-label")
        date = current_review.find_element(By.CLASS_NAME, "rsqaWe ").text
        # replace implicit wait with this but fix XPATH
        # WebDriverWait(browser, timeout=10).until(lambda k: True if find_element_with_exception(current_review, "//*[@class='wiI7pd ']//") is None else False)
        review_text = ""
        try:
            review_text = current_review.find_element(By.XPATH, f".//span[{cl_templ.format(c='wiI7pd')}]").text
        except NoSuchElementException as e:
            print("---Empty review---")
        print(f"Parse complete, author: {author}, text: {review_text}")
        return {"author": author, "stars": stars, "date": date, "review": review_text, "respond": respond}
    except Exception as e:
        print(traceback.format_exc())
        print("---Parse failed---")


def expand_review(current_review: WebElement):
    print("...trying to expand review...")
    translation_button_class = "WOKzJe"
    # show more button for long reviews
    more_button_class = "w8nwRe"
    text_span_class = "wiI7pd"
    try:
        current_review.find_element(By.XPATH, f".//button[{cl_templ.format(c=translation_button_class)}]").click()
        #wait.until(EC.staleness_of(current_review.find_element(By.XPATH, f"//span[{cl_templ.format(c=text_span_class)}]")))
        print("..!translate button clicked!..")
    except NoSuchElementException as e:
        try:
            current_review.find_element(By.XPATH,
                                        f".//button[{cl_templ.format(c=more_button_class)}]").click()
            #wait.until(EC.staleness_of(current_review.find_element(By.XPATH, f"//span[{cl_templ.format(c=text_span_class)}]")))
            print("..!more button clicked!...")
        except NoSuchElementException as e:
            pass
    finally:
        try:
            ActionChains(browser).scroll_to_element(current_review).perform()
        except StaleElementReferenceException as e:
            print("---Cant scroll - stale element---")


def get_response_text(current_review: WebElement):
    block_class = "CDe7pd"
    text_class = "wiI7pd"
    translate_button_class = "WOKzJe"
    more_button_class = "w8nwRe"
    print("...trying to get respond...")
    respond = ""
    try:
        # expand respond if possible
        current_review.find_element(By.XPATH,
                                    f".//div[{cl_templ.format(c=block_class)}]//button[{cl_templ.format(c=translate_button_class)}]").click()
        #wait.until(EC.staleness_of(current_review.find_element(By.XPATH, f"//div[{cl_templ.format(c=block_class)}]//*[{cl_templ.format(c=text_class)}]")))
        print("..!translate button clicked!..")
    except NoSuchElementException as e:
        try:
            current_review.find_element(By.XPATH,
                                        f".//div[{cl_templ.format(c=block_class)}]//button[{cl_templ.format(c=more_button_class)}]").click()
            #wait.until(EC.staleness_of(current_review.find_element(By.XPATH, f"//div[{cl_templ.format(c=block_class)}]//*[{cl_templ.format(c=text_class)}]")))
            print("..!more button clicked!..")
        except NoSuchElementException as e:
            pass
    finally:
        try:
            ActionChains(browser).scroll_to_element(current_review).perform()
        except StaleElementReferenceException as e:
            print("---Cant scroll - stale element---")
        try:
            # parse respond if possible
            # wait for text update???
            # sleep(0.1)
            respond = current_review.find_element(By.XPATH,
                                                  f".//div[{cl_templ.format(c=block_class)}]//div[{cl_templ.format(c=text_class)}]").text
        except NoSuchElementException as e:
            print("---respond not found---")
    return respond


def find_element_with_exception(base_element, xpath):
    try:
        return base_element.find_element(By.XPATH, xpath)
    except NoSuchElementException as e:
        return None


reviews = get_review_list()

df = pd.DataFrame(reviews)

df.to_csv("reviews.csv")
print("Finished")
quit()
