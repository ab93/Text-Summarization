import pprint
import math

class Node:
	def __init__(self,name):
		self.name=name
		self.auth_score=1
		self.hub_score=1
		self.HITS_score=0

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

	def printNodes(self):
		for key in self.structure:
			print "text ",key.name
			print "hub_score ",key.hub_score
			print "auth_score ",key.auth_score
			


	def set_structure(self,wordlist):
		structure=self.structure
		window=self.window
		#nodeList=self.nodeList
		for sentence in wordlist:
			for index in range(len(sentence)):
				curr_word=sentence[index]
				next_words=sentence[index+1:index+window]
				curr_node=Node(curr_word)
				#print "current node ",curr_node
				if(len(structure)==0):
					#print "first time"
					structure[curr_node]={}
					for word in next_words:
						next_node=Node(word)
						
						structure[curr_node][next_node]=1
				else:
					
					if(self.find(curr_node)):
						#print "present ",curr_node
						for word in next_words:
							next_node=Node(word)
							structure[curr_node][next_node]=1
						
					else:
						structure[curr_node]={}
						for word in next_words:
							next_node=Node(word)
							structure[curr_node][next_node]=1

		self.printStructure()
		
	def hubs_and_authorities(self):
		for k in range(10000):
			norm = 0
			#update all authority scores
			for p in self.structure:
				#print " p is ",p
				p.auth_score = 0
				incomingEdges=[]
				for key in self.structure:
					for innerkey in self.structure[key]:
						if(innerkey.name==p.name):
							incomingEdges.append(key)
				#print " incomingEdges ",incomingEdges
				for q in incomingEdges:
					p.auth_score += q.hub_score
				norm += math.pow(p.auth_score,2)
			norm = math.sqrt(norm)
			#normalize
			for p in self.structure:
				p.auth_score = p.auth_score / norm
			norm = 0
			#update git scores
			for p in self.structure:
				p.hub_score = 0
				for r in self.structure[p]:
					p.hub_score += r.auth_score
				norm += math.pow(p.hub_score,2)
			norm = math.sqrt(norm)
			for p in self.structure:
				p.hub_score = p.hub_score / norm
		print k
		self.printNodes()






graph=Graph()
graph.set_structure([["d1","d2"],["d1","d3"],["d2","d1"],["d2","d3"],["d3","d2"],["d3","d4"],["d4","d2"]])
graph.hubs_and_authorities()
