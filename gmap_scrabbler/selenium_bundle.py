class SeleniumBundle:
    cl_templ = "contains(concat(' ', normalize-space(@class), ' '), ' {c} ')"
    more_btn_class = "w8nwRe"
    translate_btn_class = "WOKzJe"
    text_span_class = "wiI7pd"
    review_block_class = "jJc9Ad"
    review_scroll_list_class = "DxyBCb"

    review_author_class = "d4r55 "
    review_stars_class = "kvMYJc "
    review_date_class = "rsqaWe "

    response_block_class = "CDe7pd"
    decline_cookie_class = "//button[@jsname='tWT92d']"

    driver_path = "C:/chromedriver_win32/chromedriver.exe"
    driver_args = []
    experimental_args = {}

    url = "https://www.google.com/maps/place/Bas%C3%ADlica+de+la+Sagrada+Fam%C3%ADlia/@41.4058614,2.1789467,13z/data=!4m8!3m7!1s0x12a4a2dcd83dfb93:0x9bd8aac21bc3c950!8m2!3d41.4036299!4d2.1743558!9m1!1b1!16zL20vMGc2bjM?entry=ttu"
    max_review_limit = 1000

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
