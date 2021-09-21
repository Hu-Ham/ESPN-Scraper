import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import statistics
import nltk

page = requests.get("https://www.espn.com/")

soup = BeautifulSoup(page.content, "html.parser")
headlinesDiv = soup.find('div', {'class': 'headlineStack'})

# Follow top headline to get full list of top headlines.
link = "https://www.espn.com" + headlinesDiv.find('a', {'data-mptype': 'headline'})['href']
storyPage = requests.get(link)
storyPageSoup = BeautifulSoup(storyPage.content, "html.parser")

totalWords = []

for a in storyPageSoup.find_all('a', {'class': 'story-link'}):
    subpageLink = "https://www.espn.com" + a['href']
    subpage = requests.get(subpageLink)
    subpageSoup = BeautifulSoup(subpage.content, "html.parser")
    articleBody = subpageSoup.find('div', {'class': 'article-body'})

    text_p = (''.join(s.findAll(text=True)) for s in articleBody.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    print("Title: " + subpageSoup.find('title').getText())
    totalWords.append(len(c_p.values()))

print("Mean Words: " + str(statistics.mean(totalWords)))
print("Median Words: " + str(statistics.median(totalWords)))