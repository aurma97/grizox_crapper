import requests
from bs4 import BeautifulSoup
# Models
list_foot = []

# Make a request
base_url = "https://www.jackstream.com/livesport/football/"
page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Getting foot list
htmlfootcontent = soup.select('div.page-container > div.content > div.table > table.table > tbody > tr')

for item in htmlfootcontent:
    if item['style'] == 'background-color:#2C3034':
        matchtime = item.select('tr.paneldefaulthulk > td.matchtime')[0].text
        for content in item.select('tr.paneldefaulthulk > td'):
            for elt in content.select('a'):
                if elt.text.strip() is not "WATCH":
                    list_foot.append({
                        "time": matchtime,
                        "link": elt.get('href'),
                        "title": elt.text.strip()
                    })
# Get iframes per match
test_url = "http://www.jackstream.net/livestreamhd/football/france-ligue-1/psg-vs-montpellier/20210925/1/"
page = requests.get(test_url)
soup = BeautifulSoup(page.content, 'html.parser')
 
footcontent = soup.select('div.page-container > div.content > div.panel > div.bg-black')

othersources = []

for item in footcontent:
    links = item.select('div#accordion > div.card > div#collapseOne > div.card-body > a ')

    for link in links:
        othersources.append({
            "link": link.get('href'),
            "title": link.text
        })
    
    iframe = item.select('div.bg-dark > iframe')

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/lib/chromium/chromium", chrome_options=options)

driver.get("https://www.tripadvisor.com/Airline_Review-d8729157-Reviews-Spirit-Airlines#REVIEWS")
more_buttons = driver.find_elements_by_class_name("moreLink")
for x in range(len(more_buttons)):
  if more_buttons[x].is_displayed():
      driver.execute_script("arguments[0].click();", more_buttons[x])
      time.sleep(1)
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')
reviews = []
reviews_selector = soup.find_all('div', class_='reviewSelector')
for review_selector in reviews_selector:
    review_div = review_selector.find('div', class_='dyn_full_review')
    if review_div is None:
        review_div = review_selector.find('div', class_='basic_review')
    review = review_div.find('div', class_='entry').find('p').get_text()
    review = review.strip()
    reviews.append(review)
    