# Simple scrapper of job offers from OLX.pl.
# It includes very basic blacklist mechanism and saves data to a Google Spreadsheet
# Require: BeautifullSoup4, Selenium, requests, gspread, oauth2client

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class OfferObject:
    def __init__(self, url):
        self.url = url

    def connection(self):
        r = requests.get(self.url)
        payload = r.text
        soup = BeautifulSoup(payload, 'html.parser')
        return soup

    def gettitle(self):
        title = self.connection().h1.string
        return title.lstrip()

    def getdescription(self):
        description = self.connection().find_all('p', class_='pding10 lheight20 large')
        description_formated = description[0].text
        return description_formated.lstrip()

    def getmoney(self):
        try:
            price = self.connection().find_all('strong', class_='x-large not-arranged')
            return price[0].text
        except IndexError:
            return 'Nie podano'

    def getconditions(self):
        condition = self.connection().find('ul', class_='offer-parameters')
        conditions_list = []
        for li in condition.find_all('li'):
            conditions_list.append(li.a.strong.text)
        return conditions_list


# generate list of links
def getlinks():
    for link in sel_soup.find_all('a', attrs={'href': re.compile("^https://www.olx.pl/oferta/")}):
        yield (link.get('href')[:-11])


# config
start_value = 2
total_pages = 5
page = 1
city = 'wroclaw'

# Phrases banned from description
ban_wordy = ()

# gspread settings
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open('').sheet1 #insert Spreedsheet name here

while page <= total_pages:
    site = 'https://www.olx.pl/praca/{}/?page={}'.format(city, page)
    print('Dumping page: {} of {} - {}'.format(page, total_pages, site))
    dupe_link = sheet.col_values(5)

    # Selenium
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(site)
    time.sleep(5)
    html = driver.execute_script('return document.documentElement.innerHTML')
    sel_soup = BeautifulSoup(html, 'html.parser')
    driver.stop_client()
    driver.close()

    # Check where Spreadsheet ended
    while True:
            starter = sheet.acell('A{}'.format(start_value)).value
            if starter:
                start_value += 1
            else:
                break


    # Check for dupes / blacklisted terms - dump rest to Spreadsheet
    for offer_link in getlinks():
        offer = OfferObject(offer_link)
        if any(ban in offer.getdescription() for ban in ban_wordy):
            print('Odrzucona - {}'.format(offer_link))
        elif offer_link in dupe_link:
            print('Duplikat - {}'. format(offer_link))
        else:
            sheet.update_acell('A{}'.format(start_value), offer.gettitle())
            sheet.update_acell('B{}'.format(start_value), offer.getconditions()[1])
            sheet.update_acell('C{}'.format(start_value), offer.getconditions()[0])
            sheet.update_acell('D{}'.format(start_value), offer.getmoney())
            sheet.update_acell('E{}'.format(start_value), offer_link)
            print('Dodana - {}'.format(offer_link))
            start_value += 1
    page += 1
    print('---')
