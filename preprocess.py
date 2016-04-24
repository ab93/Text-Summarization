import re
import os
import nltk.data
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

def readData(filename,lang='spanish'):
	'''
	Arguments: Name of file, language (default: Spanish)

	Returns: List of List of sentence words, unfiltered sentence list and
	length of doc

	Returns the [ s1[w1,w2,w3..], s2[w1,w2,w3..] ...], [s1,s2,...]
	and length of doc.
	'''

	sentWordList = []
	sentList = []
	lenDoc = 0
	with open(filename,'r') as fp:
		for line in fp:
			line = line.strip()
			sentWordList, sentList, lenDoc = cleanLine(line,sentWordList,sentList,lenDoc,lang)

	return sentWordList,sentList,lenDoc


def cleanLine(line,finalList,sentList,lenDoc,lang):
	'''
	Arguments: each line, existing sentence word list, existing unfiltered sentence
	list, length of the document and language.

	Returns: appended sentence word list, appended unfiltered sentence list, and
	length of the document seen so far.

	Performs preprocessing task. Removes stopwords, punctuations and numeric values
	'''

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
	decimal = re.compile(r'\d+.\d+')

	stemmer = SnowballStemmer('spanish')

	line = decimal.sub('',line)
	line = notNum.sub('',line)
	words = line.split(' ')
	impWords = filter(lambda x: x not in stopwords.words(lang), words)
	stemmedWords = [stemmer.stem(word) for word in impWords]

	line = ' '.join(stemmedWords)
	sentWordList = tokenizer.tokenize(line)

	for sent in sentWordList:
		words = re.findall(r'\w+', sent,flags = re.UNICODE | re.LOCALE)
		finalList.append(words)
		lenDoc += len(words)

	return finalList, sentList, lenDoc
