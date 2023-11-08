from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.MD"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.MD")
if os.path.exists(readme_path):
    with codecs.open(readme_path, encoding="utf-8") as fh:
        long_description = "\n" + fh.read()
else:
    print("README.MD file not found")
    print("here path: "+here)
    print("Readme path: " +readme_path)
setup(
    name="gmap_scrabbler",
    version='{{VERSION_PLACEHOLDER}}',
    author="Ilia Rodikov",
    author_email="rain-ilia@rambler.ru",
    description="The Google Map Reviews Web Scrabbler is a specialized tool designed to extract Google Maps reviews to a .CSV file.",
    url = "https://github.com/freezerain/gMaps_selenium_scrabbler",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)