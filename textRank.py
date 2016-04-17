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
		return 1.0/(math.pi*math.sqrt(position*(1-position)))
	

	def setNode(self,word,count):
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
		for sentence in wordlist:
			for index in range(len(sentence)):
				count+=1
				curr_word=sentence[index]
				next_words=sentence[index+1:index+window]
				curr_node = self.setNode(curr_word,count)
				if(len(structure)==0):
					structure[curr_node]={}
					for word in next_words:
						next_node = self.setNode(word,count+next_words.index(word)+1)
						structure[curr_node][next_node]=(curr_node.position_dist+next_node.position_dist)/2
				else:
					if(self.find(curr_node)):
						for word in next_words:
							next_node = self.setNode(word,count+next_words.index(word)+1)
							structure[curr_node][next_node]=(curr_node.position_dist+next_node.position_dist)/2
					else:
						structure[curr_node]={}
						for word in next_words:
							next_node = self.setNode(word,count+next_words.index(word)+1)
							structure[curr_node][next_node]=(curr_node.position_dist+next_node.position_dist)/2


	def sort_nodes_textrank(self,n):
		global final_list
		final_list = sorted(self.structure.keys(), key=operator.attrgetter('PRscore'),reverse=True)[:n]
		position_sorted=sorted(final_list)
		sorted_x = sorted(final_list, key=operator.attrgetter('position'))
		return sorted_x

	def textRank(self):
		for k in range(10000):
			prev_PRscore={}
			for p in self.structure:
				if p not in prev_PRscore:
					prev_PRscore[p]={}
					prev_PRscore[p]=p.PRscore
				else:
					prev_PRscore[p]=p.PRscore
			for p in self.structure:
				incomingEdges=[]
				for key in self.structure:
					for innerkey in self.structure[key]:
						if(innerkey.name==p.name):
							incomingEdges.append(key)
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
				if delta==min_delta:
					return

	def summarize(self,m):
		finalScores={}
		for i in range(0,len(data)):
			pd=self.pd_calculator((i+1)/float(len(data)+1))
			sum_keywords=0
			for word in final_list:
				if word.name in data[i]:
					sum_keywords+=word.PRscore
			finalScores[i]=pd*sum_keywords
		sorted_finalScores = sorted(finalScores.items(), key=operator.itemgetter(1),reverse=True)[:m]
		# print sorted_finalScores
		sorted_finalScores = sorted(sorted_finalScores, key=operator.itemgetter(0),reverse=False)
		# print sorted_finalScores
		# print "summary!! "
		# for i in range(0,len(sorted_finalScores)):
		# 	print finaldata[sorted_finalScores[i][0]]


#n - number of nodes; m - number of sentences needed
def textRankMain(input_file,n,m):
	global countWords,data,finaldata
	graph=Graph()
	data,finaldata,countWords=readData(input_file,'english')
	graph.set_structure(data)
	graph.textRank()
	answer=graph.sort_nodes_textrank(n)
	graph.summarize(m)

# input_file="/home/nlp/project/englishdata/reuters3.txt"
# textRankMain(input_file,int(sys.argv[1]),int(sys.argv[2]))
