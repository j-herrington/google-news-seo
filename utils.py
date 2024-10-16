from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from oauth2client.service_account import ServiceAccountCredentials
import gspread


def setup_driver():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument("--headless")
    firefox_options.add_argument('--incognito')
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) "
        "Version/6.0 Mobile/10A5376e Safari/8536.25")
    path = os.getenv("WEBDRIVER_PATH")
    driver = webdriver.Firefox(executable_path=path, options=firefox_options)
    return driver


def setup_sheets(sheet_index):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_CREDENTIALS_PATH"), scope)
    client = gspread.authorize(creds)
    sheet = client.open('google_stories')
    wks = sheet.get_worksheet(sheet_index)
    return wks
