# Google News SEO Tool

## Background
This project was created in 2020 to assist an SEO analyst. The challenge faced involved manually searching a list of keywords to determine if they appeared in Google's Top Stories box—a time-consuming task. This tool was developed to automate the process, significantly reducing the manual effort involved by automatically searching for the keywords and recording the results. The automation provided by this tool has proven to be a valuable asset in SEO analysis and efficiency.

One of the main reasons this codebase is deprecated is due to changes in Google's schema for Top Stories search results. The original search patterns and methods for scraping pages and locating elements no longer align with these updates, rendering the existing automation less effective.


## Overview
This project automates the gathering of data from Google Stories using web scraping techniques, leveraging the power of Selenium for web automation and gspread for Google Sheets interaction. Designed with a PyQt5-based graphical user interface, it aims to simplify data acquisition and management processes for users.

## Key Features
- **Automated Web Scraping:** Harness Selenium to scrape Google Stories efficiently. Utilizes Beautiful Soup to assist Selenium in parsing and extracting data, providing a powerful combination for web scraping.
- **Google Sheets Integration:** Easily export and manage scraped data within Google Sheets using gspread.
- **Graphical User Interface:** Utilize a PyQt5 GUI for straightforward project interaction.
- **Threading for Enhanced Performance:** Implements threading to make the user interface more responsive and speed up task execution by performing web scraping operations in the background. This allows for parallel processing of multiple keywords, significantly improving the tool's efficiency.


## Prerequisites
To run this project, you'll need:
- Python 3.6 or later.
- Selenium WebDriver for browser automation.
- gspread and PyQt5 for Python for Google Sheets interaction and the graphical interface, respectively.

## Setup and Installation
Follow these steps to get the project up and running on your system:

### 1. Environment Setup
Ensure Python 3.6 or newer is installed along with Pip for managing Python packages.

### 2. Dependencies Installation
Install all required dependencies using the following command:
```bash 
pip install -r requirements.txt
```

## Selenium WebDriver
This project uses geckodriver for Firefox to automate web browsing actions. Make sure to download geckodriver and note its path for setup.
* Download geckodriver from Mozilla's GitHub repository.
* Extract the downloaded file and place it in a known directory.

## Environment Variables
Configure the following environment variables:
* WEBDRIVER_PATH: Path to the geckodriver executable.
* GOOGLE_CREDENTIALS_PATH: Path to your Google service account credentials file.

## Deprecation Notice
Please be aware that as of [Insert Date], this codebase is deprecated and is no longer actively maintained. The project's dependencies, APIs, and tools may have evolved or become unavailable. This project should be used for reference or educational purposes only.

## Usage
Launch the project by executing:
```bash 
python main.py
```
The GUI will guide you through importing keywords and starting the scraping process.

## Contributing
While this project is deprecated, we welcome contributions or forks that update or adapt its functionality for current use.

### Detailed Environment Variable Usage

- **WEBDRIVER_PATH**: This environment variable should be set to the full path of the `geckodriver` executable. It is used in the `setup_driver` function to specify the executable path for the Firefox WebDriver:
```python
path = os.getenv("WEBDRIVER_PATH")
```

- **GOOGLE_CREDENTIALS_PATH**: This environment variable should be set to the full path of your Google service account credentials file. It is utilized in the `setup_sheets` function to authenticate with Google APIs:
```python
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_CREDENTIALS_PATH"), scope)
```
This detail is crucial for ensuring the application can interact with Google Sheets and the Selenium WebDriver as intended.
