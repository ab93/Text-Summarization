import textRank
import math
keywords_list=[None]*1000
headlines=[None]*1000
content=[None]*1000
length=[None]*1000
fp=open('keywordscount.txt','w')
for i in range(0,1000):
	try:
		f=open('englishdata/reuters'+str(i)+'.txt','r')
		headlines[i]=f.readline().split(" ")
		content[i]=f.readline()
		length[i]=len(content[i])
		f.close()
	except:
		headlines[i]=None
		content[i]=None
		length[i]=None

for i in range(0,1000):
	n=math.ceil(min(0.1*length[i],7*math.log(length[i])))
	fp.write(str(n)+"\n")
	try:
		keywords_list[i]=textRank.textRankMain('englishdata/reuters'+str(i)+'.txt',n)
	except:
		keywords_list[i]=None

count=0
for i in range(0,1000):
	if i%100==0:
		print "Processed till "+str(i)
	threshold=0
	if headlines[i] is not None and keywords_list[i] is not None:
		# print headlines[i]
		for j in range(0,len(headlines[i])):
			# print keywords_list[i]
			if headlines[i][j].lower() in keywords_list[i]:
				threshold+=1.0
		if (threshold/len(headlines[i]))>=0.7:
			count+=1

print "Count is "+str(count)
