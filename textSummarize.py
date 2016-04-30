
import math
from preprocess import readData
import operator
import sys


data=[]
final_list=[]
finaldata=[]
sorted_x=[]

class Node:
	'''
	Represents a node of a graph.

	Member Variables are:
	name: text of the sentence;
	position: position of the sentence in the document;
	PRscore: PageRank score for the sentence;
	'''

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
	'''
	Represents a document as a Graph.

	Member variables are:
	structure: A dictionary consisting of the mapping of nodes and edges;
	nodeHash: Dictionary of node references;
	'''
	def __init__(self):
		self.structure={}
		self.nodeHash = {}

	def printStructure(self):
		for key in self.structure:
			print key.name.encode('utf-8'),key.PRscore

	def similarity(self,si,sj):
		'''
		Arguments: 2 sentences
		Returns: Similarity score value

		Compute similarity score between 2 sentences
		'''
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
		'''
		Argument: List of sentences in the document
		creates nodes of sentences and edges between the nodes based on similarity
		'''
		count=0
		structure=self.structure
		for sentence in wordlist:
			count+=1
			curr_node=self.setNode(sentence,count)
			for j in range(len(wordlist)):
				next_node=self.setNode(wordlist[j],j+1)
				#print next_node, curr_node
				if(next_node == curr_node):
					continue
				if curr_node not in structure:
					structure[curr_node]={}
					structure[curr_node][next_node]=self.similarity(sentence,wordlist[j])
					#print self.similarity(sentence,wordlist[j])
				else:
					structure[curr_node][next_node]=self.similarity(sentence,wordlist[j])
				# 	print self.similarity(sentence,wordlist[j])
				# raw_input()
		# for key in self.structure:
		# 	for value in self.structure[key]:
		# 		print key.name.encode('utf-8'),value.name.encode('utf-8'),self.structure[key][value]


	def sort_nodes_textsummarize(self,m):
		'''
		Argument: number of sentences to extract

		Sorts the nodes based on pr score and picks the top m nodes
		'''
		global final_list,sorted_x
		final_list = sorted(self.structure.keys(), key=operator.attrgetter('PRscore'),reverse=True)[:m]
		sorted_x = sorted(final_list, key=operator.attrgetter('position'))
		# print
		result=[]
		for i in range(1,len(sorted_x)):
			result.append(sorted_x[i].name)

		#print result
		return result


	def textSummarize(self, max_iter=1000, min_delta=0):
		'''
		Argument: Maximum number of iterations (default 10000), minimum difference in PR score between
		consecutive iterations (default 0)

		Implements the main TextRank algorithm for sentence extraction. Calculates the PR score per node till convergence
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
						#print r.name.encode('utf-8')
						weightTot+=self.structure[q][r]
					innerScore += (self.structure[q][p]*q.PRscore)/weightTot
				p.PRscore=0.15+(0.85*(innerScore))
				delta=0
				for key in self.structure:
					delta+=abs(prev_PRscore[key] - key.PRscore)
				if delta <= min_delta:
					return


def textSummarizeMain(input_file,m):
	global countWords,data,finaldata

	print "Running default TextRank on", input_file,"...."

	graph=Graph()
	data,finaldata,countWords=readData(input_file)
	# print finaldata
	# print countWords
	# raw_input()
	countWords=len(finaldata)
	graph.set_structure(finaldata)
	graph.textSummarize()
	print "Finished TextRank."
	return graph.sort_nodes_textsummarize(m)
