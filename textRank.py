import pprint
import math
from preprocess import readData
import operator
import sys

min_delta=0
data=[]
final_list=[]
finaldata=[]

class Node:
	def __init__(self,name,count,p_dist):
		self.name=name
		self.position=count
		self.PRscore=0
		self.position_dist=p_dist

	def __repr__(self):
		return self.name

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)



class Graph:
	def __init__(self):
		self.structure={}
		self.threshold=0
		self.window=2
		self.nodeList=[]
		self.nodeHash = {}

	def set_threshold(self,thresh):
		self.threshold=thresh

	def set_window(self,win):
		self.window=win

	def printStructure(self):
		pprint.pprint(self.structure)

	def find(self,curr_node):
		for obj in self.structure:
			if obj==curr_node:
				return True
		return False
	def pd_calculator(self,position):
		# print position
		return 1.0/(math.pi*math.sqrt(position*(1-position)))
	

	def setNode(self,word,count):
		# print count,count/float(countWords+1)
		if word in self.nodeHash:

			node = self.nodeHash[word]

			if(node.position_dist<self.pd_calculator(count/float(countWords+1))):
				node.position_dist=self.pd_calculator(count/float(countWords+1))
		else:
			node = Node(word,count,self.pd_calculator(count/float(countWords+1)))
			self.nodeHash[word] = node

		return node

	def set_structure(self,wordlist):
		count=0
		structure=self.structure
		window=self.window
		#nodeList=self.nodeList
		for sentence in wordlist:
			for index in range(len(sentence)):
				count+=1
				curr_word=sentence[index]
				next_words=sentence[index+1:index+window]

				curr_node = self.setNode(curr_word,count)
				#curr_node=Node(curr_word)
				#print "current node ",curr_node
				if(len(structure)==0):
					#print "first time"
					structure[curr_node]={}
					for word in next_words:
						next_node = self.setNode(word,count+next_words.index(word)+1)
						#next_node=Node(word)

						structure[curr_node][next_node]=(curr_node.position_dist+next_node.position_dist)/2
				else:

					if(self.find(curr_node)):
						#print "present ",curr_node
						for word in next_words:
							#next_node=Node(word)
							next_node = self.setNode(word,count+next_words.index(word)+1)
							structure[curr_node][next_node]=(curr_node.position_dist+next_node.position_dist)/2

					else:
						structure[curr_node]={}
						for word in next_words:
							next_node = self.setNode(word,count+next_words.index(word)+1)
							#next_node=Node(word)
							structure[curr_node][next_node]=(curr_node.position_dist+next_node.position_dist)/2

		# self.printStructure()

	

	


	def sort_nodes_textrank(self,n):
		global final_list
		#print self.structure.keys()
		# print "sorted n list "
		final_list = sorted(self.structure.keys(), key=operator.attrgetter('PRscore'),reverse=True)[:n]
		#print final_list
		# for each in final_list:
		# 	print each.name,each.PRscore,each.position

		position_sorted=sorted(final_list)
		# print 
		# print "sorted on position"
		sorted_x = sorted(final_list, key=operator.attrgetter('position'))
		# for each in sorted_x:
		# 	print each.name,each.PRscore,each.position
		return sorted_x

	def textRank(self):
		# print "inside "
		for k in range(10000):
			# print k
			prev_PRscore={}
			#store current Page Rank scores
			for p in self.structure:
				if p not in prev_PRscore:
					prev_PRscore[p]={}
					prev_PRscore[p]=p.PRscore
				else:
					prev_PRscore[p]=p.PRscore
			#update all PR scores
			for p in self.structure:
				#print " p is ",p
				incomingEdges=[]
				for key in self.structure:
					for innerkey in self.structure[key]:
						if(innerkey.name==p.name):
							incomingEdges.append(key)
				#print " incomingEdges ",incomingEdges
				innerScore=0
				for q in incomingEdges:
					weightTot=0
					for r in self.structure[q]:
						weightTot+=self.structure[q][r]
					innerScore += (self.structure[q][p]*q.PRscore)/weightTot
				p.PRscore=0.15+(0.85*(innerScore))
				delta=0
				for key in self.structure:
					delta+=abs(prev_PRscore[key] - key.PRscore)
				#print("Delta:",delta)
				if delta==min_delta:
					# for each in self.structure:
					# 	print(each.name," ",each.PRscore)
					return

	def summarize(self):
		finalScores={}
		for i in range(0,len(data)):
			pd=self.pd_calculator((i+1)/float(len(data)+1))
			#print "pd",pd
			sum_keywords=0
			for word in final_list:
				if word.name in data[i]:
					sum_keywords+=word.PRscore

			finalScores[i]=pd*sum_keywords
			#print "final scores", sum_keywords
		sorted_finalScores = sorted(finalScores.items(), key=operator.itemgetter(1),reverse=True)
		# print sorted_finalScores

		# for (i,j) in sorted_finalScores:
		# 	print finaldata[i]


def textRankMain(input_data,n):
	global countWords,data,finaldata
	graph=Graph()
	data,finaldata,countWords=readData(input_data,'english')
	# print countWords
	graph.set_structure(data)
	graph.textRank()
	answer=graph.sort_nodes_textrank(n)
	result=[]
	for i in range(0,len(answer)):
		result.append(answer[i].name)

	return result
	# graph.summarize()
	
# textRankMain(int(sys.argv[1]))
