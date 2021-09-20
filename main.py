import requests
from bs4 import BeautifulSoup
import re

URL = input("Enter a URL to scrape for pizza: ")
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
title = soup.find('title').getText()
results = soup.find_all('p')
count = 0
for i in results:
    if "pizza" in i.getText().lower():
        count += 1
links = soup.find_all('a', attrs={'href': re.compile("^http://")})
print("Title: " + title)
print("Number of times 'pizza' occurs: " + str(count))
print("All web links:")
for i in links:
    print(i.get('href'))