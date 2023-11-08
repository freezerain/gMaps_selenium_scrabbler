# Google Map Reviews Web Scrabbler 🗺️

The Google Map Reviews Web Scrabbler is a specialized tool designed to extract Google Maps reviews to a .CSV file. 📜

Please note that this tool is configured to perform a specific task and may not be suitable for customizing to your
specific requirements. ⚙️

## Installation & Usage Instructions 🚀

To use this tool, you'll need to set up the necessary components. Here are the installation steps:

1. **Web/Chrome Driver 🌐**: This tool utilizes Selenium, which requires a web driver to interact with your chosen web
   browser. Web drivers serve as intermediaries between Selenium and the browser, facilitating communication through a
   common wire protocol. To get started, follow these steps:

    - Download the Chrome Driver from [here](https://chromedriver.chromium.org/home).
    - Once downloaded, copy or cut the driver file from your downloads folder.
    - Paste the driver file into your C drive, typically located at `C:\chromedriver_win32\chromedriver.exe`. Please
      ensure you follow this path to avoid any path-related errors. 🚗

2. **Pip installation 🐍**: Ensure you have installed the package by running the following command:

    ```bash
    python -m pip install gmap_scrabbler
    ```

3. **Usage**: Run the following command in the CLI window and provide necessary arguments:
   ```
   python -m gmap_scrabbler
   ```
4. **Arguments⚙️**: You will be prompted to enter the following information:

- **url**: The URL of the Google Maps reviews page you want to scrape.
- **export_path**: The path where the extracted reviews will be saved as a CSV file. The specified folder should already
  exist. You can customize the export path, but if none is provided, the default path is set to "D:/".
- **lang**: The browser locale for viewing the Google Maps page. By default, it is set to "en" (English), but you can
  specify other supported locales like "es" (Spanish). You will be prompted to enter this value.
- **review_limit**: The maximum number of reviews you want to extract. You can specify the limit, but if none is
  provided, the default limit is set to 1000. You will be prompted to enter this value.

5. **Output 📦**:

    The script will initiate a web browser, load the Google Maps reviews page, scroll through the reviews, and extract the
    specified number of reviews.
    Once the extraction is complete, the reviews will be saved to a CSV file in the specified export path. 📂
    
    Please keep in mind that this tool is intended for a specific purpose, and customization beyond its predefined
    functionality may require additional development efforts. 🔧👨‍💻

## Technologies and Libraries Used 🛠️

- Python 3.7+
- Typer
- Selenium
- Pandas
- Published to PyPi using GitHub actions and Twine 📦🔗
