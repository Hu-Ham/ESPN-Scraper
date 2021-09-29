#
# Mini Project 1 - Lucius Latham, Hugh Hamilton
# This code scrapes the text of the top 20 articles on ESPN.com,
# beginning with the articles indexed under NFL, and advancing until twenty have been collated.
# The text is subsequently analyzed for its mean and modal number of words, and Python data visualization
# packages are used to graphically display the most common words used in all of the articles, excluding
# "stop words". Some data cleaning extends the list of stop words from NLTK's default package.
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

# Arrays of the total number of words and of all words used, in all articles
totalWords = []
words = []
# The set data structure allows links to be added without adding the same link twice, by a hashed reference.
subpageLinks = set()
noOfPages = 0

espnUrl = input("Enter the url (https://www.espn.com): ")
if espnUrl[-1] == '/':
    espnUrl = espnUrl[:-1]


# Method to traverse from the main URL to subpages, and to continue traversing until 20 unique articles
# have been aggregated.
def parseMainpage(link):
    global noOfPages, espnUrl

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    headlinesDiv = soup.find('div', {'class': 'headlineStack'})

    # Follow top headline to get full list of top headlines.
    link = espnUrl + headlinesDiv.find('a', {'data-mptype': 'headline'})['href']
    storyPage = requests.get(link)
    storyPageSoup = BeautifulSoup(storyPage.content, "html.parser")

    for a in storyPageSoup.find_all('a', {'class': 'story-link'}):
        if noOfPages >= 20:
            break
        subpageLink = espnUrl + a['href']
        parseSubpage(subpageLink)
        noOfPages += 1


# Method to add individual page links into the set data structure of all links, and to tokenize all article
# content in order to count the total number of words and aggregate all words in the words[] array
def parseSubpage(link):
    global words, totalWords, subpageLinks

    if link in subpageLinks:
        return
    else:
        subpageLinks.add(link)
    subpage = requests.get(link)
    subpageSoup = BeautifulSoup(subpage.content, "html.parser")
    articleBody = subpageSoup.find('div', {'class': 'article-body'})

    # Tokenize all words
    text_p = (''.join(s.findAll(text=True)) for s in articleBody.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    print("Title: " + subpageSoup.find('title').getText())
    totalWords.append(len(c_p.values()))
    words.append(' '.join([''.join(x.findAll(text=True)) for x in articleBody.findAll('p')]))


page = requests.get(espnUrl)
soup = BeautifulSoup(page.content, "html.parser")
menuLinks = soup.find_all('a', {'itemprop': 'url'})

for link in menuLinks:
    if noOfPages < 20:
        parseMainpage(espnUrl + link['href'])

# Print basic data
print("Number of Articles: " + str(noOfPages))
print("Mean Words: " + str(statistics.mean(totalWords)))
print("Median Words: " + str(statistics.median(totalWords)))

# Use of the NLTK package to "clean" data by removing stop-words, and then assess most common remaining words
ENGLISH_RE = re.compile(r'[a-z]+')
stop_words = nltk.corpus.stopwords.words("english")
stop_words.append('said')  # Removal of the word "said", a common stop-word not in the stop word corpus
nltk.download(['stopwords', 'punkt'])
totalText = ' '.join(words)
tokenized = nltk.TweetTokenizer().tokenize(totalText)
tokenizedNotStopWords = [w for w in tokenized if w.lower() not in stop_words and ENGLISH_RE.match(w.lower())]
fd = nltk.FreqDist(tokenizedNotStopWords)
most_common = fd.most_common(15)

# Print out the results as a word cloud
wordcloud = WordCloud(max_words=50, background_color="white").generate(' '.join(tokenizedNotStopWords))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Print out the results as a bar chart
fig = go.Figure(data=[go.Bar(
    x=[i[0] for i in most_common],
    y=[i[1] for i in most_common],
    textposition='auto'
)])
fig.show()
