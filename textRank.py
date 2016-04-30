import pprint
import math
from preprocess import readData
import operator
import sys

data=[]
final_list=[]
finaldata=[]

class Node:
	'''
	Represents a node of a graph.

	Member Variables are:
	name: text of the word;
	position: position of the word in the document;
	PRscore: PageRank score for the word;
	position_dist: position based probability distribution value
	'''
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
	'''
	Represents a document as a Graph.

	Member variables are:
	structure: A dictionary consisting of the mapping of nodes and edges;
	window: A value that defines the co-occurance relation between the nodes;
	nodeHash: Dictionary of node references;
	'''
	def __init__(self):
		self.structure={}
		self.window=2
		self.nodeHash = {}

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
		'''
		Calculates Arc Sine probability distribution
		'''
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
		'''
		Argument: List of words in the document

		Creates nodes of words and edges between the nodes based on window size
		'''
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
		'''
		Argument: number of keywords to extract

		Sorts the nodes based on pr score and picks the top n nodes
		'''
		global final_list
		final_list = sorted(self.structure.keys(), key=operator.attrgetter('PRscore'),reverse=True)[:n]
		position_sorted=sorted(final_list)
		#sorted_x = sorted(final_list, key=operator.attrgetter('position'))


	def textRank(self, max_iter=1000, min_delta=0):
		'''
		Argument: Maximum number of iterations (default 10000), minimum difference in PR score between
		consecutive iterations (default 0)

		Implements the main TextRank algorithm. Calculates the PR score per node till convergence
		'''
		for k in range(max_iter):
			#print k
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
				if delta <= min_delta:
					return

	def summarize(self,m):
		'''
		Arguments: Number of sentences summary should have

		Returns: Summary (String)

		Calculates sentence scores based on the keywords and positional distribution of the sentence.
		Sorts based on sentence score. It picks the top m sentences, and forms the summary based on
		the positional order.
		'''
		finalScores={}

		for i in range(0,len(data)):
			pd=self.pd_calculator((i+1)/float(len(data)+1))
			sum_keywords=0
			for word in final_list:
				if word.name in data[i]:
					sum_keywords+=word.PRscore
			finalScores[i]=pd*sum_keywords
		sorted_finalScores = sorted(finalScores.items(), key=operator.itemgetter(1),reverse=True)[:m]
		sorted_finalScores = sorted(sorted_finalScores, key=operator.itemgetter(0),reverse=False)
		result=[]

		#print len(sorted_finalScores)
		for i in range(len(sorted_finalScores)):
			try:
				result.append(finaldata[sorted_finalScores[i][0]])
			except:
				return result
		return result


def textRankMain(input_file,n,m):
	global countWords,data,finaldata

	print "Running TextRank v2.0 on", input_file,"...."

	graph=Graph()
	data,finaldata,countWords=readData(input_file)
	graph.set_structure(data)
	graph.textRank()
	graph.sort_nodes_textrank(n)

	print "Finished TextRank v2.0"
	return graph.summarize(m)
