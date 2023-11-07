from typing import Optional

import pandas as pd
import typer
from typer import Typer
from typing_extensions import Annotated

from gmap_scrabbler.selenium_bundle import SeleniumBundle
from selenium_controller import SeleniumController

test_url = "https://www.google.com/maps/place/Bas%C3%ADlica+de+la+Sagrada+Fam%C3%ADlia/@41.4058614,2.1789467,13z/data=!4m8!3m7!1s0x12a4a2dcd83dfb93:0x9bd8aac21bc3c950!8m2!3d41.4036299!4d2.1743558!9m1!1b1!16zL20vMGc2bjM?entry=ttu"
app = Typer(no_args_is_help=True)


@app.command()
def get_reviews(
        url: Annotated[str, typer.Argument()],
        lang: Annotated[Optional[str], typer.Option()] = None
) -> None:
    """
    provide URL of place on google map.
    the language is important, English by default
    :param url: URL of place
    :param lang: language
    :return:
    """
    bundle = SeleniumBundle()
    bundle.url = url
    if lang is None or 'es':
        bundle.driver_args = ['--lang=es', '--accept-lang=es']
        bundle.experimental_args = {'prefs': {'intl.accept_languages': 'es,es_ES'}}

    sc = SeleniumController(bundle=bundle)
    reviews = sc.start_scrapping()
    df = pd.DataFrame(reviews)
    df.to_csv("reviews.csv")
    print("Finished")


if __name__ == "__main__":
    typer.run(get_reviews(test_url))
