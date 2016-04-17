import json
count=0
countNoTitle=0
json_data=open('2007-10.json').read()

jsoncontents = json.loads(json_data,strict=False)

print len(jsoncontents['items']['item'])
for i in range(0,len(jsoncontents['items']['item'])):
	content=jsoncontents['items']['item'][i]['discurso']
	content=content.encode('utf-8')
	print "content ",content
	f = open('2007-10c'+str(count)+'.txt','wb')
	#content=content.encode('utf-8')
	try:
		title=jsoncontents['items']['item'][i]['titulo']
		print count
		raw_input()
	except:
		#print count
		countNoTitle+=1
	
	f.write(content)
	count+=1
	f.close()
print count
print countNoTitle

