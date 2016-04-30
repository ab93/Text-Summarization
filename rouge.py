#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import nltk.data

def getNGrams(n, text):
    ngram_set = set()
    text_length = len(text)
    max_index_ngram_start = text_length - n
    for i in range (max_index_ngram_start + 1):
        ngram_set.add(tuple(text[i:i+n]))
        #ngram_set.add(text[i])
    return ngram_set


def splitIntoWords(sentences):
	fullTextWords = sentences.strip().split(' ')
	#for s in sentences:
	#	fullTextWords.extend(s.words)
	return fullTextWords


def getWordNGrams(n, sentences):
	assert (len(sentences) > 0)
	assert (n > 0)

	words = splitIntoWords(sentences)
	return getNGrams(n, words)


def filterText(text):
    notNum = re.compile(r'[^0-9a-zA-Z ]+')
    text = notNum.sub('',text)
    return text

def Rouge_n(candidate_sentences, reference_sentences, n=3):
    candidate_sentences = filterText(candidate_sentences)
    reference_sentences = filterText(reference_sentences)

    if len(candidate_sentences) <= 0 or len(reference_sentences) <= 0:
		raise (ValueError("Collections must contain at least 1 sentence."))

    candidate_ngrams = getWordNGrams(n, candidate_sentences)
    reference_ngrams = getWordNGrams(n, reference_sentences)
    reference_count = float(len(reference_ngrams))

    # Gets the overlapping ngrams between candidate and reference
    overlapping_ngrams = candidate_ngrams.intersection(reference_ngrams)
    overlapping_count = float(len(overlapping_ngrams))

    return overlapping_count / reference_count


def writeRougeScore(id,score_1,score_2,increase,fp):
	fp.write(str(id) + '\t' + str(score_1) + '\t' + str(score_2) + '\t' + str(increase) + '\n')

#reference_sentences = 'Ese héroe de la Patria que se sacrificó precisamente, para que nosotros podamos cumplirle al pueblo colombiano y hacer realidad los sueños que desde hace dos siglos tiene el pueblo colombiano, de tener cada vez más un país justo, un país moderno, un país seguro, a eso aspira cualquier sociedad, a eso aspira cualquier país.Y que hoy ya podemos decir que no ocupamos ese segundo vergonzoso lugar entre los países más desiguales de toda la región, después de Haití.No hay un camino más efectivo para conseguir un país más justo que la educación.Si a Daniel José o cualquier niño o a cualquier niña le da uno una buena educación, inmediatamente se nivela el punto de partida y vamos a tener un país mucho más justo.Ninguna familia en Colombia, ningún padre o madre tiene por qué pagar un solo peso por la educación de sus hijos, del grado cero al grado once, eso es una revolución ya de por sí.Porque, qué hay más importante para una sociedad que los niños y las niñas, que van a ser el futuro, aprendan bien.'
#candidate_sentences = 'Maritza Frías es la rectora de una institución que se llama Almirante Padilla, yo también estuve en una institución que se llama Almirante Padilla, en la Escuela Naval en Cartagena, de allá me gradúe y por eso es tan importante cumplirle al Almirante Padilla, que nos está viendo en este momento.Ese héroe de la Patria que se sacrificó precisamente, para que nosotros podamos cumplirle al pueblo colombiano y hacer realidad los sueños que desde hace dos siglos tiene el pueblo colombiano, de tener cada vez más un país justo, un país moderno, un país seguro, a eso aspira cualquier sociedad, a eso aspira cualquier país.Y hemos puesto en marcha iniciativas para generar cada vez más empleos, óigase bien, Colombia ha sido el país de América Latina que en estos dos últimos años más empleos ha generado, más de dos millones de empleos, un número similar de empleos ha creado Brasil, pero Brasil tiene cuatro veces la población nuestra.'
#print Rouge_n(filterText(candidate_sentences),filterText(reference_sentences))
