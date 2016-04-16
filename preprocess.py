import re
import os
import nltk.data
from nltk.corpus import stopwords

def readData(filename,lang='spanish'):
	'''
	Return the [ s1[w1,w2,w3..], s2[w1,w2,w3..] ...] and length of doc
	'''
	sentList = []
	lenDoc = 0
	with open(filename,'r') as fp:
		for line in fp:
			line = line.strip()
			sentList, lenDoc = cleanLine(line,sentList,lenDoc,lang)

	return sentList,lenDoc


def cleanLine(line,finalList,lenDoc,lang):
	try:
		tokenizer = nltk.data.load('tokenizers/punkt/'+ lang + '.pickle')
	except:
		"language not supported!!"
		return None

	line = line.decode('utf-8').lower()
	notNum = re.compile(r'[0-9]+')
	line = notNum.sub('',line)
	words = line.split(' ')
	impWords = filter(lambda x: x not in stopwords.words(lang), words)
	line = ' '.join(impWords)

	sentList = tokenizer.tokenize(line)

	for sent in sentList:
		words = re.findall(r'\w+', sent,flags = re.UNICODE | re.LOCALE)
		finalList.append(words)
		lenDoc += len(words)

	return finalList, lenDoc


#readData('data/data/2010-2013/2010-13c0.txt')
#readData('englishdata/reuters0.txt','english')
