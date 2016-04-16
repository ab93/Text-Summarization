import re
import os
import nltk.data
from nltk.corpus import stopwords

def readData(filename,lang='spanish'):
	'''
	Return the [ s1[w1,w2,w3..], s2[w1,w2,w3..] ...], unfiltered sentence list
	and length of doc.
	'''
	sentWordList = []
	sentList = []     #Unfiltered sentence list
	lenDoc = 0
	with open(filename,'r') as fp:
		for line in fp:
			line = line.strip()
			sentWordList, sentList, lenDoc = cleanLine(line,sentWordList,sentList,lenDoc,lang)

	return sentWordList,sentList,lenDoc


def cleanLine(line,finalList,sentList,lenDoc,lang):
	try:
		tokenizer = nltk.data.load('tokenizers/punkt/'+ lang + '.pickle')
	except:
		print "Language not Supported"
		return None

	tempList = tokenizer.tokenize(line.decode('utf-8'))
	for sent in tempList:
		sentList.append(sent)

	line = line.decode('utf-8').lower()
	notNum = re.compile(r'[0-9]+')
	line = notNum.sub('',line)
	words = line.split(' ')
	impWords = filter(lambda x: x not in stopwords.words(lang), words)
	line = ' '.join(impWords)

	sentWordList = tokenizer.tokenize(line)

	for sent in sentWordList:
		words = re.findall(r'\w+', sent,flags = re.UNICODE | re.LOCALE)
		finalList.append(words)
		lenDoc += len(words)

	return finalList, sentList, lenDoc


readData('data/data/2010-2013/2010-13c0.txt')
#readData('englishdata/reuters0.txt','english')
