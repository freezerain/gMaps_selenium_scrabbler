# Import the library Selenium

import pandas as pd

from selenium_controller import SeleniumController
from selenium_driver import SeleniumDriver

sc = SeleniumController()

reviews = sc.start_scrapping()

df = pd.DataFrame(reviews)

df.to_csv("reviews.csv")
print("Finished")
quit()
