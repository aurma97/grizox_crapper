import requests
from bs4 import BeautifulSoup
import re
# Models
movies_categories = []
movies_list = []
movies = []

# Make a request
base_url = "http://grizox.com"
page = requests.get(base_url + "/ok8du6yjsz2o/home/grizox")
soup = BeautifulSoup(page.content, 'html.parser')

categories = soup.select('div.content > div.column4 > div.menu1')

for cat in categories:
    for item in cat.select('ul > li'):
        movies_categories.append({
            "title": item.text,
            "link": base_url + item.get('onclick').replace('window.location.href=', '').replace("'", "")
        })

# Fetching films per categories

for movie in movies_categories:
    # print(movie.get("title"))
    cat_page = requests.get(movie.get("link"))
    cat_soup = BeautifulSoup(cat_page.content, 'html.parser')
    
    cat_body = cat_soup.select('div.content > div.row > div.column1 > center > a')

    for item in cat_body:
        if item.get('style'):
            link = base_url + item.get('href')

            _cat_page = requests.get(link)
            _cat_soup = BeautifulSoup(_cat_page.content, 'html.parser')
            _cat_movies_paginated = _cat_soup.select('div.content > div.row > div.column1 > div#hann > p > span')

            for item_p in _cat_movies_paginated:
                for elt in item_p.select('a'):
                    movies_list.append({
                        "title": item_p.text.strip(),
                        "link": base_url + elt.get('href'),
                        "category": movie.get("title")
                    })

# Fetching films videos details

def lastWord(string):
    
    # taking empty string
    newstring = ""
      
    # calculating length of string
    length = len(string)
      
    # traversing from last
    for i in range(length - 1, 0, -1):
        
        # if space is occured then return
        if(string[i] == " "):
            
            # return reverse of newstring
            return newstring[::-1]
        else:
            newstring = newstring + string[i]
  
for movie in movies_list:
    film_title = movie.get('title')
    film_quality = "HD" #lastWord(film_title)

    film_link = movie.get('link')

    film_page = requests.get(film_link)
    film_soup = BeautifulSoup(film_page.content, 'html.parser')

    film_poster = film_soup.select('div.content > div.row > div.column1 > p > img')[0].get('src')
    film_description = film_soup.find_all('p', {"style": "text-align: left;"})

    for item in film_description:
        film_description = item.text.strip()

    # film_iframe = film_soup.select('div.content > div.row > div.column1 > p > iframe')[0].get('src')

    film_year = re.match(r'.*([1-3][0-9]{3})', film_title)
    if film_year is not None:
        film_year = film_year.group(1)

    movies.append({
        "title": film_title,
        "description": film_description,
        "link": film_link,
        # "iframe": film_iframe,
        "year": film_year,
        "poster": film_poster,
    })

print(movies)