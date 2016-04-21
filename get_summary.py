import textRank
import math
import textSummarize
import sys

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

	for i in range(int(sys.argv[1]),int(sys.argv[2])):
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

		html_model="<html><head><title>model"+str(i)+"</title></head><body>"
		html_peer="<html><head><title>peer"+str(i)+"</title></head><body>"
		for j in range(0,len(reference)):
			reference[j]="<a name='"+str(j)+"'>["+str(j)+"]</a><a href='#"+str(j)+"' id="+str(j)+">"+reference[j]+"</a>"
			html_model+=reference[j]
		for k in range(0,len(candidate)):
			candidate[k]="<a name='"+str(k)+"'>["+str(k)+"]</a><a href='#"+str(k)+"' id="+str(k)+">"+candidate[k]+"</a>"
			html_peer+=candidate[k]
		html_model+="</body></html>"
		html_peer+="</body></html>"
		f1=open('summarized_text/models/2010-13model-'+str(i)+'.html','w')
		f2=open('summarized_text/systems/2010-13peer-'+str(i)+'.html','w')
		f1.write(html_model.encode('utf-8'))
		f2.write(html_peer.encode('utf-8'))
		f1.close()
		f2.close()

if __name__ == '__main__':
	main()
