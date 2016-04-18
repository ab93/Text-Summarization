import textRank
import math
import textSummarize

content=[None]*322
length=[0]*322

def main():
	for i in range(322):
		'''
		Reads each spanish document and counts the length of the file.
		'''
		try:
			f=open('spanishdata/2010-2013/2010-13c'+str(i)+'.txt','r')
			f.readline()
			content[i]=f.readline()
			length[i]=len(content[i])
			f.close()
		except:
			content[i]=None
			length[i]=None

	for i in range(322):
		'''
		Computes the n value (the number of keywords) that TextRank must compute.
		This is calculated based on the below formula which was derived expermientally.
		'''
		n=int(math.ceil(min(0.1*length[i],7*math.log(length[i]))))

		'''
		The reference summary is obtained using the vanilla TextRank algorithm
		proposed by Prof. Rada Mihalcea of Univ of Michigan
		'''
		candidate=textRank.textRankMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',n,10)
		reference=textSummarize.textSummarizeMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',10)

		'''
		The candidate summary is obtained using the new flavor of the
		TextRank algorithm v2.0.

		The new version uses keyword extraction as opposed to sentence extraction.
		Using these keywords, the sentences are then extracted using a calculated
		"sentence score"
		'''
		f1=open('summarized_text/reference/2010-13ref'+str(i)+'.txt','w')
		f2=open('summarized_text/candidate/2010-13can'+str(i)+'.txt','w')
		f1.write(reference.encode('utf-8'))
		f2.write(candidate.encode('utf-8'))
		f1.close()
		f2.close()

if __name__ == '__main__':
	main()
