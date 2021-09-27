#
# Mini Project 1 - Lucius Latham, Hugh Hamilton
#

import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import statistics
import nltk
import re
import matplotlib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go

page = requests.get("https://www.espn.com/")

soup = BeautifulSoup(page.content, "html.parser")
headlinesDiv = soup.find('div', {'class': 'headlineStack'})

# Follow top headline to get full list of top headlines.
link = "https://www.espn.com" + headlinesDiv.find('a', {'data-mptype': 'headline'})['href']
storyPage = requests.get(link)
storyPageSoup = BeautifulSoup(storyPage.content, "html.parser")

totalWords = []
words = []
subpageLinks = set()
i = 0

for a in storyPageSoup.find_all('a', {'class': 'story-link'}):
    if i >= 20:
        break
    subpageLink = "https://www.espn.com" + a['href']
    if subpageLink in subpageLinks:
        continue
    else:
        subpageLinks.add(subpageLink)
    subpage = requests.get(subpageLink)
    subpageSoup = BeautifulSoup(subpage.content, "html.parser")
    articleBody = subpageSoup.find('div', {'class': 'article-body'})

    text_p = (''.join(s.findAll(text=True)) for s in articleBody.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    print("Title: " + subpageSoup.find('title').getText())
    totalWords.append(len(c_p.values()))
    words.append(' '.join([''.join(x.findAll(text=True)) for x in articleBody.findAll('p')]))
    i += 1

print("Mean Words: " + str(statistics.mean(totalWords)))
print("Median Words: " + str(statistics.median(totalWords)))

ENGLISH_RE = re.compile(r'[a-z]+')

nltk.download(['stopwords', 'punkt'])
totalText = ' '.join(words)
tokenized: list[str] = nltk.word_tokenize(totalText)
tokenizedNotStopWords = [w for w in tokenized if w.lower() not in nltk.corpus.stopwords.words("english") and ENGLISH_RE.match(w.lower())]
fd = nltk.FreqDist(tokenizedNotStopWords)
most_common = fd.most_common(15)

wordcloud = WordCloud(max_words=50, background_color="white").generate(' '.join(tokenizedNotStopWords))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

fig = go.Figure(data=[go.Bar(
    x=[i[0] for i in most_common],
    y=[i[1] for i in most_common],
    textposition='auto'
)])
fig.show()
