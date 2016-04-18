import textRank
import math
import textSummarize
content=[None]*322
length=[0]*322
for i in range(0,322):
	try:
		f=open('spanishdata/2010-2013/2010-13c'+str(i)+'.txt','r')
		f.readline()
		content[i]=f.readline()
		length[i]=len(content[i])
		f.close()
	except:
		print "came into except"
		content[i]=None
		length[i]=None

for i in range(0,322):
	n=int(math.ceil(min(0.1*length[i],7*math.log(length[i]))))
	try:
		reference=textSummarize.textSummarizeMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',10)
		print "reference done"
		candidate=textRank.textRankMain('spanishdata/2010-2013/2010-13c'+str(i)+'.txt',n,10)
		print "candidate done"
		f1=open('newdata/reference/2010-13c'+str(i)+'.txt','w')
		f2=open('newdata/candidate/2010-13c'+str(i)+'.txt','w')
		f1.write(reference)
		f2.write(candidate)
		f1.close()
		f2.close()
	except:
		pass

# count=0
# for i in range(0,1000):
# 	if i%100==0:
# 		print "Processed till "+str(i)
# 	threshold=0
# 	if headlines[i] is not None and keywords_list[i] is not None:
# 		# print headlines[i]
# 		for j in range(0,len(headlines[i])):
# 			# print keywords_list[i]
# 			if headlines[i][j].lower() in keywords_list[i]:
# 				threshold+=1.0
# 		if (threshold/len(headlines[i]))>=0.7:
# 			count+=1

# print "Count is "+str(count)
