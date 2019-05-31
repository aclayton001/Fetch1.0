import os
import newspaper
import nltk
from newspaper import fulltext
from newspaper import Article
from collections import Counter
import re, string
from urllib.parse import urlparse

# Clear text files on startup
open("goodarticles.txt", "w").close()
open("commonwords.txt", "w").close()
open("filteredwords.txt", "w").close()

# Function to write article text to file
def writetofile(txt):

    # Opens, writes article text to, and closes goodarticles.txt
    f = open("goodarticles.txt", "a")
    f.write(txt)
    f.close()

# Function to build article and return article text
def buildarticle(url):
    # Builds the article
    a = Article(url, language='en')
    a.download()
    a.parse()

    # Sets article_txt equal to the raw article text from url
    article_txt = a.text
    
    # Returns article_txt
    return article_txt

# Function to filter out certain words
def filterarticle(article_txt):
    # Opens the filterwords.txt file
    filter_words = open("filterwords.txt", "r")
    
    # Makes the article text lowercase and removes punctuation
    filtered_txt = article_txt.lower()
    regex = re.compile('[^a-zA-Z -]')
    filtered_txt = regex.sub('',filtered_txt)
    
    # Removes any filter words
    for line in filter_words:
        for word in line.split():
            filtered_txt = re.sub(r"\b%s\b" % word,"",filtered_txt)

    # Close the filter_words.txt file
    filter_words.close()

    # Opens, writes filtered_txt to, and closes filteredwords.txt
    f = open("filteredwords.txt", "a")
    f.write(filtered_txt)
    f.close()

# Function to write most common words to file
def writecommontofile():

    # Reads the filteredwords.txt file
    words = re.findall(r'\w+', open("filteredwords.txt").read())

    # Finds the 50 most common words in the filteredwords.txt file
    c = Counter(words).most_common(20)

    # Opens, writes the 50 most common words to, and closes commonwords.txt
    f = open("commonwords.txt", "a")
    f.write('\n'.join('%s %s' % x for x in c))
    f.close()

# Opens goodurls.txt file for urls to analyze
t = open("goodurls.txt")

# For every url in urls.txt, builds the article, writes raw text to goodarticles.txt,
# and then filters the article
for url in t:
    article = buildarticle(url)
    writetofile(article)
    filterarticle(article)

# Writes the 50 most commmon words to commonwords.txt
writecommontofile()

# Exits the program
exit()

# Need to write all urls to file first, then count most commmon words, write that to different file

