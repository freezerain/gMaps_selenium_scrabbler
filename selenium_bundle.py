# this class will contain all default params of another class
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
    driver_args = ['--lang=es', '--accept-lang=es']
    experimental_args = {'prefs': {'intl.accept_languages': 'es,es_ES'}}

    url = "https://www.google.es/maps/place/RESTAURANT+TORRE+MIRONA/@41.9675449,2.7828756,16z/data=!4m8!3m7!1s0x12baddfe6c57ccbb:0x6558d8c865e0e3bd!8m2!3d41.9669495!4d2.7737607!9m1!1b1!16s%2Fg%2F11c1qlc0np?entry=ttu"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
