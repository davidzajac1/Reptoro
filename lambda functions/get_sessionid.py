from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json, os, shutil, uuid, boto3, time


#Enables Selenium Webdriver to run on Lambda
class WebDriver(object):

    def __init__(self):
        self.options = Options()

        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver


#Gets the SessionID and Number of Results Pages for this Scraping Interval
def lambda_handler(event, context):

    instance_ = WebDriver()
    driver = instance_.get()
    driver.get(f"https://www.morphmarket.com/us/search?epoch=2&layout=list&sort=nfs&min_price={str(event['min_price'])}&max_price={str(event['max_price'])}&page=1")

    time.sleep(4)
    try:
        driver.find_element_by_xpath('//*[@id="CookielawBanner"]/div/p/a').click()
    except:
        pass

    try:
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id_login"]').send_keys(event['user'])
        time.sleep(2)

        driver.find_element_by_xpath('//*[@id="id_password"]').send_keys(event['pass'])
        time.sleep(2)

        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/form/button').click()
    except:
        pass

    time.sleep(2)

    cookies = driver.get_cookies()

    for cookie in cookies:
        if cookie['name'] == 'sessionid':
            sessionid = cookie['value']
            break

    print(sessionid)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    num_entries = int(soup.find('div', {'class':'result-count'}).strong.text.strip().replace('1-50 of ',''))

    num_pages = int(num_entries / 50) + (num_entries % 50 > 0)

    print(num_pages)

    driver.quit()

    return {'sessionid': sessionid,'num_pages': num_pages}
