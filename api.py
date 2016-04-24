#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer 
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer



from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "spanish"
SENTENCES_COUNT = 10


#if __name__ == "__main__":

def klReferenceSummary(path):	
	sentencesList=[]
	parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = KLSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		#print(sentence._text)
		sentencesList.append(sentence._text)

	return sentencesList

def lexrankReferenceSummary(path):	
	sentencesList=[]
	parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = LexRankSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		#print(sentence._text)
		sentencesList.append(sentence._text)

	return sentencesList

def lsaReferenceSummary(path):	
	sentencesList=[]
	parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = LsaSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		#print(sentence._text)
		sentencesList.append(sentence._text)

	return sentencesList

def luhnReferenceSummary(path):	
	sentencesList=[]
	parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = LuhnSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		#print(sentence._text)
		sentencesList.append(sentence._text)

	return sentencesList

def sumbasicReferenceSummary(path):	
	sentencesList=[]
	parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = SumBasicSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		#print(sentence._text)
		sentencesList.append(sentence._text)

	return sentencesList

def textrankReferenceSummary(path):	
	sentencesList=[]
	parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = TextRankSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		#print(sentence._text)
		sentencesList.append(sentence._text)

	return sentencesList
