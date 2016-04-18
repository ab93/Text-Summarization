import pprint
import math
from preprocess import readData
import operator
import sys

min_delta=0
data=[]
final_list=[]
finaldata=[]
sorted_x=[]

class Node:
	def __init__(self,name,count):
		self.name=name
		self.position=count
		self.PRscore=0
		

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
		for key in self.structure:
			print key.name,key.PRscore

	def find(self,curr_node):
		for obj in self.structure:
			if obj==curr_node:
				return True
		return False

	
	def similarity(self,si,sj):
		si1=set(si)
		sj1=set(sj)
		return len(si1.intersection(sj1))/(math.log(len(si))+math.log(len(sj)))

	def setNode(self,word,count):
		if word in self.nodeHash:
			node = self.nodeHash[word]
		else:
			node = Node(word,count)
			self.nodeHash[word] = node
		return node

	def set_structure(self,wordlist):
		count=0
		structure=self.structure
		window=self.window
		for sentence in wordlist:
			count+=1
			curr_node=self.setNode(sentence,count)
			for j in range(len(wordlist)):
				next_node=self.setNode(wordlist[j],j+1)
				if(next_node == curr_node):
					continue
				if curr_node not in structure:
					structure[curr_node]={}
					structure[curr_node][next_node]=self.similarity(sentence,wordlist[j])
				else:
					structure[curr_node][next_node]=self.similarity(sentence,wordlist[j])


	def sort_nodes_textsummarize(self,m):
		global final_list,sorted_x
		final_list = sorted(self.structure.keys(), key=operator.attrgetter('PRscore'),reverse=True)[:m]
		sorted_x = sorted(final_list, key=operator.attrgetter('position'))
		# print 
		result=""
		for i in range(1,len(sorted_x)):
			result+=sorted_x[i].name
		return result
		

	def textSummarize(self):
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


#m - number of sentences needed
def textSummarizeMain(input_file,m):
	global countWords,data,finaldata
	graph=Graph()
	data,finaldata,countWords=readData(input_file)
	countWords=len(finaldata)
	graph.set_structure(finaldata)
	graph.textSummarize()
	return graph.sort_nodes_textsummarize(m)

# input_file="/home/saurbh/nlp/project/englishdata/reuters3.txt"
# textSummarizeMain(input_file,int(sys.argv[1]))
