import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.espn.com/")

soup = BeautifulSoup(page.content, "html.parser")
for a in soup.find_all('a', class_='contentItem__padding'):
    subpage = requests.get(a['href'])