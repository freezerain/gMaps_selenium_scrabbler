import os
from pathlib import Path, PurePath
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
        url: Annotated[str, typer.Option(prompt=True)],
        export_path: Annotated[str, typer.Option(prompt=True)] = "d:/",
        lang: Annotated[Optional[str], typer.Option(prompt=True)] = 'en',
        review_limit: Annotated[Optional[int], typer.Option(prompt=True)] = 1000
) -> None:
    """
    Open browser and scroll through reviews saving them to review.csv
    :param url: URL to reviews on google map
    :param export_path: where to save reviews.csv. The folder should be already exist
    :param lang: browser locale. By default: en, also supported es
    :param review_limit: limit of reviews to save
    :return:
    """
    bundle = SeleniumBundle()
    bundle.url = url
    bundle.max_review_limit = review_limit
    if lang == 'es':
        bundle.driver_args = ['--lang=es', '--accept-lang=es']
        bundle.experimental_args = {'prefs': {'intl.accept_languages': 'es,es_ES'}}
    elif lang is None or 'en':
        bundle.driver_args = ['--lang=en', '--accept-lang=en']
        bundle.experimental_args = {'prefs': {'intl.accept_languages': 'en,en_US'}}

    sc = SeleniumController(bundle=bundle)
    reviews = sc.start_scrapping()
    df = pd.DataFrame(reviews)
    Path(export_path).mkdir(parents=True, exist_ok=True)
    path = Path(export_path).joinpath("reviews.csv")
    df.to_csv(path)
    print("Finished")


if __name__ == "__main__":
    app()
