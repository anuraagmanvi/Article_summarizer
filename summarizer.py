# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 19:32:20 2019

@author: Anuraag
"""

import bs4 as bs
import urllib.request
import re
import nltk
import heapq

while(True):
    topic = input("What would you like to know today?")
    if topic.lower() == 'quit':
        exit(0)
    topic = topic.title()
    topic = re.sub(' ', '_', topic)
    url = "https://en.wikipedia.org/wiki/" + topic
    try:
        source = urllib.request.urlopen(url).read()
    except:
        print("Looks like Wikipedia has not yet covered " + topic)
        continue

    soup = bs.BeautifulSoup(source, 'lxml')

    text = ""
    for para in soup.find_all('p'):
        text += para.text

    text = re.sub(r"\[[0-9]*\]", "", text)
    text = re.sub(r"\s+", " ", text)

    clean_text = text.lower()
    clean_text = re.sub(r"\W", " ", clean_text)
    clean_text = re.sub(r"\d", "", clean_text)

    sent = nltk.sent_tokenize(text)

    stop_words = nltk.corpus.stopwords.words('english')

    word_to_count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
                if word not in word_to_count.keys():
                    word_to_count[word] = 1
                else:
                    word_to_count[word] += 1

    for key in word_to_count.keys():
        word_to_count[key] = word_to_count[key]/max(word_to_count.values())

    sent_to_score = {}
    for sentence in sent:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_to_count.keys():
                if len(sentence.split(' ')) < 25:
                    if sentence not in sent_to_score.keys():
                        sent_to_score[sentence] = word_to_count[word]
                    else:
                        sent_to_score[sentence] += word_to_count[word]

    best_sent = heapq.nlargest(7, sent_to_score, key=sent_to_score.get)

    print('---------------------------')
    for sentence in best_sent:
        print(sentence)
    print('---------------------------')
    print()
