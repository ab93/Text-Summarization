import textRank
import math
import textSummarize
import sys
import string
import api
import evalSummary
import csv
from rouge import Rouge_n, writeRougeScore

Rouge_file = open('result'+sys.argv[1]+'-'+sys.argv[2]+'.txt', 'w+')


content=[None]*322
length=[0]*322
weights = [0.25, 0.25, 0.25, 0.25]


def main():
	for i in range(322):
		'''
		Reads each spanish document and counts the length of the file.
		'''
		try:
			f=open('spanishdata/2010-2013/2010-13c'+str(i)+'.txt','r')
			content[i]=f.read()
			content[i]=content[i].replace("\n"," ")
			content[i]=content[i].split(" ")
			content[i]=[x for x in content[i] if x]
			length[i]=len(content[i])
			f.close()
		except:
			content[i]=None
			length[i]=None

	#Rouge_fp = open('Rouge_eval.txt','w+')

	for i in range(int(sys.argv[1]),int(sys.argv[2])):
		'''
		Computes the n value (the number of keywords) that TextRank must compute.
		This is calculated based on the below formula which was derived expermientally.
		'''
		n=int(math.ceil(min(0.1*length[i],7*math.log(length[i]))))
		print n
		'''
		The reference summary is obtained using the vanilla TextRank algorithm
		proposed by Prof. Rada Mihalcea of Univ of Michigan
		'''
		#reference_0List=[]
		#reference_1List=[]
		#reference_2List=[]
		#reference_3List=[]
		#reference_4List=[]
		#reference_5List=[]
		#candidateList=[]
		#reference_0=textSummarize.textSummarizeMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',10)
		#reference_1=api.klReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		#reference_2=api.lexrankReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		#reference_3=api.lsaReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		#reference_4=api.sumbasicReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		#reference_5=api.textrankReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')

		references = api.klReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		references.extend(api.lexrankReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt'))
		references.extend(api.lsaReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt'))
		references.extend(api.sumbasicReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt'))
		references.extend(api.textrankReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt'))

		candidate_1 = textRank.textRankMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',n,10)
		candidate_2 = textSummarize.textSummarizeMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',10)

		candidate_1 = ' '.join(candidate_1)
		candidate_2 = ' '.join(candidate_2)
		references = ' '.join(references)

		Rouge_score_1 = Rouge_n(candidate_1,references)
		Rouge_score_2 = Rouge_n(candidate_2,references)
		change = ((Rouge_score_1 - Rouge_score_2)/Rouge_score_2) * 100.0

		change = "%.3f" % change
		Rouge_score_2="%.4f"%Rouge_score_2
		Rouge_score_1="%.4f"%Rouge_score_1
		print "Rouge score of Text Rank v2.0:",Rouge_score_1
		print "Rouge score of Original Text Rank:",Rouge_score_2
		print "Percentage increase:",change

		writeRougeScore(i,Rouge_score_1,Rouge_score_2,change,Rouge_file)


		'''
		or indexValue in range(len(reference_0)):
			for j in reference_0[indexValue].split():
				reference_0List.append(j)

			for j in reference_1[indexValue].split():
				reference_1List.append(j)

			for j in reference_2[indexValue].split():
				reference_2List.append(j)

			for j in reference_3[indexValue].split():
				reference_3List.append(j)

			for j in reference_4[indexValue].split():
				reference_4List.append(j)

			for j in reference_5[indexValue].split():
				reference_5List.append(j)

			for j in candidate[indexValue].split():
				candidateList.append(j)
		'''

		#print reference_1List
		#result=evalSummary.BLEU.compute(candidateList, [reference_0List,reference_1List,reference_2List,reference_3List,reference_4List,reference_5List], weights)
		#result1=evalSummary.BLEU.compute(reference_0List, [reference_1List,reference_2List,reference_3List,reference_4List,reference_5List], weights)
		#writerCsv.writerow((i,result,result1,((result-result1)/result1)*100))
		#print result,result1,((result-result1)/result1)*100


		'''
		The candidate summary is obtained using the new flavor of the
		TextRank algorithm v2.0.

		The new version uses keyword extraction as opposed to sentence extraction.
		Using these keywords, the sentences are then extracted using a calculated
		"sentence score"
		'''


if __name__ == '__main__':
	main()
