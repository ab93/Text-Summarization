from __future__ import division
from nltk.util import ngrams
import math
import nltk

class BLEU(object):
    """

    1. Test with an instance:

    >>> weights = [0.25, 0.25, 0.25, 0.25]
    >>> candidate1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
    ...               'ensures', 'that', 'the', 'military', 'always', 
    ...               'obeys', 'the', 'commands', 'of', 'the', 'party', '.']

    >>> candidate2 = ['It', 'is', 'to', 'insure', 'the', 'troops',  
    ...               'forever', 'hearing', 'the', 'activity', 'guidebook', 
    ...               'that', 'party', 'direct', '.']

    >>> reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that', 
    ...               'ensures', 'that', 'the', 'military', 'will', 'forever', 
    ...               'heed', 'Party', 'commands', '.'] 

    >>> reference2 = ['It', 'is', 'the', 'guiding', 'principle', 'which',  
    ...               'guarantees', 'the', 'military', 'forces', 'always', 
    ...               'being', 'under', 'the', 'command', 'of', 'the', 
    ...               'Party', '.']

    >>> reference3 = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the', 
    ...     'army', 'always', 'to', 'heed', 'the', 'directions', 
    ...     'of', 'the', 'party', '.']

    >>> BLEU.compute(candidate1, [reference1, reference2, reference3], weights)
    0.0555662774619807

    >>> BLEU.compute(candidate2, [reference1, reference2, reference3], weights)
    0.04211415110983725

    2. Test with two corpus that one is a reference and another is 
    an output from translation system:

    >>> weights = [0.25, 0.25, 0.25, 0.25]
    >>> ref_file = open('newstest2012-ref.en')
    >>> candidate_file = open('newstest2012.fr-en.cmu-avenue')

    >>> total = 0.0
    >>> count = 0

    >>> for candi_raw in candidate_file:
    ...     ref_raw = ref_file.readline()
    ...     ref_tokens = nltk.word_tokenize(ref_raw)
    ...     candi_tokens = nltk.word_tokenize(candi_raw)
    ...     total = BLEU.compute(candi_tokens, [ref_tokens], weights)
    ...     count += 1

    >>> total/count
    2.787504437460048e-05

    """

    @staticmethod
    def compute(candidate, references, weights):

        candidate = map(lambda x: x.lower(), candidate) 
        references = map(lambda x: [c.lower() for c in x], references)

        n = len(weights)

        bp = BLEU.brevity_penalty(candidate, references)

        s = 0.0
        i = 1
        for weight in weights:          
            p_n = BLEU.modified_precision(candidate, references, i)
            if p_n != 0:
                s += weight * math.log(p_n)
            i += 1

        return bp * math.exp(s)
    
    @staticmethod
    def modified_precision(candidate, references, n):
        candidate_ngrams=[]
        candidate_n = ngrams(candidate, n)
        
        for x in candidate_n:
            #print x
            candidate_ngrams.append(x)
        # print candidate_ngrams
        #print type(candidate_ngrams)
            #length+=1
            
        
        if len(candidate_ngrams) == 0:
            return 0
        
        #raw_input()
        c_words = set(candidate_ngrams)
        #print c_words
        for word in c_words:
            count_w = candidate_ngrams.count(word) + 1
            #print count_w

            count_max = 0
            for reference in references:
                reference_ngrams=[]
                reference_n = ngrams(reference, n)
                for x in reference_n:
                    reference_ngrams.append(x)

                count = reference_ngrams.count(word) + 1
                if count > count_max:
                    count_max = count

        return min(count_w, count_max) / (len(candidate) + len(c_words))

    @staticmethod
    def brevity_penalty(candidate, references):
        c = len(candidate)

        lengthes_ref = map(lambda x: abs(len(x) - c), references)

        r = reduce(lambda x, y: min(x,y), lengthes_ref)

        if c > r:
            return 1
        else:
            return math.exp(1 - r/c)

# run doctests
# if __name__ == "__main__":
#     weights = [0.25, 0.25, 0.25, 0.25]
#     candidate1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which','ensures', 'that', 'the', 'military', 'always', 'obeys', 'the', 'commands', 'of', 'the', 'party', '.']

#     candidate2 = ['It', 'is', 'to', 'insure', 'the', 'troops','forever', 'hearing', 'the', 'activity', 'guidebook', 'that', 'party', 'direct', '.']

#     reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that', 'ensures', 'that', 'the', 'military', 'will', 'forever', 'heed', 'Party', 'commands', '.'] 

#     reference2 = ['It', 'is', 'the', 'guiding', 'principle', 'which', 'guarantees', 'the', 'military', 'forces', 'always', 'being', 'under', 'the', 'command', 'of', 'the', 'Party', '.']

#     reference3 = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the', 'army', 'always', 'to', 'heed', 'the', 'directions', 'of', 'the', 'party', '.']

#     print BLEU.compute(candidate1, [reference1, reference2, reference3], weights)


#     print BLEU.compute(candidate2, [reference1, reference2, reference3], weights)

