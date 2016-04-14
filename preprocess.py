import re
import os
import nltk.data
from nltk.corpus import stopwords

def readData(filename):
    sentList = []
    with open(filename,'r') as fp:
        for line in fp:
            line = line.strip()
            sentList = cleanLine(line,sentList)

    return sentList


def cleanLine(line,finalList):
    tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

    line = line.decode('utf-8').lower()
    words = line.split(' ')
    impWords = filter(lambda x: x not in stopwords.words('spanish'), words)
    line = ' '.join(impWords)

    sentList = tokenizer.tokenize(line)

    for sent in sentList:
        words = re.findall(r'\w+', sent,flags = re.UNICODE | re.LOCALE)
        finalList.append(words)

    return finalList
