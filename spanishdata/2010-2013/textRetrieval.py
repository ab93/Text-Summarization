import json
import csv
count=0
countNoTitle=0
json_data=open('2010-13.json').read()
csv_file = open('2010-13.csv','wb')
csv_writer = csv.writer(csv_file)
jsoncontents = json.loads(json_data,strict=False)

print len(jsoncontents['items']['item'])

for i in range(0,len(jsoncontents['items']['item'])):
	temp=[]
	content=jsoncontents['items']['item'][i]['discurso']
	content=content.encode('utf-8')
	print "content ",content
	f = open('2010-13c'+str(count)+'.txt','wb')
	temp.append(count)
	try:
		title=jsoncontents['items']['item'][i]['titulo']
		title=title.encode('utf-8')
		temp.append(title)
		f.write(content)
		csv_writer.writerow(temp)
		count+=1
	except:
		title=""
		countNoTitle+=1
	
	f.close()
	print count
	print countNoTitle
