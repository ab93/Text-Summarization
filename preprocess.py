import re
import os
import nltk.data
from nltk.corpus import stopwords

def readData(filename,lang='spanish'):
    sentList = []
    with open(filename,'r') as fp:
        for line in fp:
            line = line.strip()
            sentList = cleanLine(line,sentList,lang)

    return sentList


def cleanLine(line,finalList,lang):
    try:
        tokenizer = nltk.data.load('tokenizers/punkt/'+ lang + '.pickle')
    except:
        "language not supported!!"
        return None

    line = line.decode('utf-8').lower()
    words = line.split(' ')
    impWords = filter(lambda x: x not in stopwords.words(lang), words)
    line = ' '.join(impWords)

    sentList = tokenizer.tokenize(line)

    for sent in sentList:
        words = re.findall(r'\w+', sent,flags = re.UNICODE | re.LOCALE)
        finalList.append(words)

    return finalList

#readData('data/2010-2013/2010-13c0.txt','english')
