import hits

keywords_list=[None]*1000
headlines=[None]*1000
for i in range(0,1000):
	try:
		f=open('englishdata/reuters'+str(i)+'.txt','r')
		headlines[i]=f.readline().split(" ")
		f.close()
	except:
		headlines[i]=None

for i in range(0,1000):
	try:
		keywords_list[i]=hits.hitsMain('englishdata/reuters'+str(i)+'.txt',60)
	except:
		keywords_list[i]=None

count=0
for i in range(0,1000):
	if i%100==0:
		print "Processed till "+str(i)
	threshold=0
	if headlines[i] is not None:
		# print headlines[i]
		for j in range(0,len(headlines[i])):
			# print keywords_list[i]
			if headlines[i][j].lower() in keywords_list[i]:
				threshold+=1.0
		if (threshold/len(headlines[i]))>=0.5:
			count+=1

print "Count is "+str(count)
