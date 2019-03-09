import urllib.request
from bs4 import BeautifulSoup
import csv
import re
import time
import random

# Scraper writes to {cityname}-results.csv
writer = csv.writer(open("sj-results.csv", "w"), delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)

# Yelp url
i=0

city = str(input())
formatted_city = city.replace(' ', '+')
keywoard = str(input())

url = ['https://www.yelp.com/search?find_desc='+keyword+'&find_loc'+formatted_city]

# Scraper function
def scrape(cur_url):
    html = urllib.request.urlopen(cur_url).read()
    html1 = re.sub('<br>', '. ', str(html))
    html2 = html1.replace('\\n', '')
    soup = BeautifulSoup(html2, 'html.parser')
    divs = soup.find_all("li", {"class" : "regular-search-result"})
    
    for div in divs:
        title = div.find('a', class_="biz-name js-analytics-click")
        address = div.find('address')
        phone = div.find('span',class_="biz-phone")
        reviews = div.find('span', class_="review-count rating-qualifier")
        bizsite = "None"

        if title['href']:
            html_web = urllib.request.urlopen("https://www.yelp.com"+title['href']).read()
            soup_web = BeautifulSoup(html_web, 'html.parser')
            div_web = soup_web.find("span", {"class" : "biz-website"})
            if div_web:
                a = div_web.find('a')
                if "www" not in a.text:
                    bizsite = "www."+a.text.strip()
                else:
                    bizsite = a.text.strip()

        if address is None:
            address = div.find('div', class_="service-area")

        if title is not None:
            biztitle = title.text.strip()
        else:
            biztitle = "None"

        if address is not None:
            bizaddress = address.text.strip()
        else:
            bizaddress = "No address"

        if phone is not None:
            bizphone = phone.text.strip()
        else:
            bizphone = "000-000-0000"

        if reviews is not None:
            bizreviews = reviews.text.strip()
        else:
            bizreviews = 0

        writer.writerow([biztitle, bizaddress, bizphone, bizreviews, bizsite])


# Get the first 100 pages
while i<100:
    print (str(i) + "\n")
    start = i * 10
    sleep = random.randint(3, 7)
    time.sleep(sleep) # Need this so we don't trigger DDOS alerts
    scrape(url[0]+'&start=' + str(start))
    i=i+1
