import textRank
import math
import textSummarize
import sys
import string
import api
import evalSummary
import csv
csv_file = open('result.csv', 'w+')
writerCsv = csv.writer(csv_file)

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
		reference0List=[]
		reference1List=[]
		reference2List=[]
		reference3List=[]
		reference4List=[]
		reference5List=[]
		candidateList=[]
		reference0=textSummarize.textSummarizeMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',10)
		reference1=api.klReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		reference2=api.lexrankReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		reference3=api.lsaReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		reference4=api.sumbasicReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		reference5=api.textrankReferenceSummary('spanishdata/2010-2013/2010-13c'+str(i)+'.txt')
		candidate=textRank.textRankMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',n,10)
		for indexValue in range(len(reference0)):
			for j in reference0[indexValue].split():
				reference0List.append(j)

			for j in reference1[indexValue].split():
				reference1List.append(j)

			for j in reference2[indexValue].split():
				reference2List.append(j)

			for j in reference3[indexValue].split():
				reference3List.append(j)

			for j in reference4[indexValue].split():
				reference4List.append(j)

			for j in reference5[indexValue].split():
				reference5List.append(j)

			for j in candidate[indexValue].split():
				candidateList.append(j)
			
			
		#print reference1List
		result=evalSummary.BLEU.compute(candidateList, [reference0List,reference1List,reference2List,reference3List,reference4List,reference5List], weights)
		result1=evalSummary.BLEU.compute(reference0List, [reference1List,reference2List,reference3List,reference4List,reference5List], weights)
		writerCsv.writerow((i,result,result1,((result-result1)/result1)*100))
		print result,result1,((result-result1)/result1)*100
		

		'''
		The candidate summary is obtained using the new flavor of the
		TextRank algorithm v2.0.

		The new version uses keyword extraction as opposed to sentence extraction.
		Using these keywords, the sentences are then extracted using a calculated
		"sentence score"
		'''

		# html_model="<html><head><title>model"+str(i)+"</title></head><body>"
		# html_peer="<html><head><title>peer"+str(i)+"</title></head><body>"
		# for j in range(0,len(reference)):
		# 	reference[j]="<a name='"+str(j)+"'>["+str(j)+"]</a><a href='#"+str(j)+"' id="+str(j)+">"+reference[j]+"</a>"
		# 	html_model+=reference[j]
		# for k in range(0,len(candidate)):
		# 	candidate[k]="<a name='"+str(k)+"'>["+str(k)+"]</a><a href='#"+str(k)+"' id="+str(k)+">"+candidate[k]+"</a>"
		# 	html_peer+=candidate[k]
		# html_model+="</body></html>"
		# html_peer+="</body></html>"
		# f1=open('summarized_text/models/2010-13model-'+str(i)+'.html','w')
		# f2=open('summarized_text/systems/2010-13peer-'+str(i)+'.html','w')
		# f1.write(html_model.encode('utf-8'))
		# f2.write(html_peer.encode('utf-8'))
		# f1.close()
		# f2.close()

if __name__ == '__main__':
	main()
