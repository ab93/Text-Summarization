import pprint
import math
from preprocess import readData
import operator
import sys

min_delta=0

class Node:
	def __init__(self,name,count):
		self.name=name
		self.auth_score=1
		self.hub_score=1
		self.HITS_score=0
		self.position=count
		self.PRscore=0

	def __repr__(self):
		return self.name

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)

	def __cmp__(self, other):
		if self.HITS_score < other.HITS_score:
			return 1
		elif self.HITS_score > other.HITS_score:
			return -1
		else:
			return 0


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

	def printNodes(self):
		for key in self.structure:
			print "\ntext ",key.name
			print "hub_score ",key.hub_score
			print "auth_score ",key.auth_score
			print("Inside:")
			for key2 in self.structure[key]:
				print "text ",key2.name
				print "hub_score ",key2.hub_score
				print "auth_score ",key2.auth_score

	def setNode(self,word,count):
		if word in self.nodeHash:
			node = self.nodeHash[word]
		else:
			node = Node(word,count)
			self.nodeHash[word] = node

		return node

	def set_structure(self,wordlist):
		count=-1
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

						structure[curr_node][next_node]=1
				else:

					if(self.find(curr_node)):
						#print "present ",curr_node
						for word in next_words:
							#next_node=Node(word)
							next_node = self.setNode(word,count+next_words.index(word)+1)
							structure[curr_node][next_node]=1

					else:
						structure[curr_node]={}
						for word in next_words:
							next_node = self.setNode(word,count+next_words.index(word)+1)
							#next_node=Node(word)
							structure[curr_node][next_node]=1

		# self.printStructure()

	def hubs_and_authorities(self):
		for k in range(1000):
			# print k
			norm = 0.0
			prev_hub_score={}
			#update all authority scores
			for p in self.structure:
				#print " p is ",p
				p.auth_score = 0.0
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

			for p in self.structure:
				if p not in prev_hub_score:
					prev_hub_score[p]={}
					prev_hub_score[p]=p.hub_score
				else:
					prev_hub_score[p]=p.hub_score

			norm = 0.0
			#update hub scores
			for p in self.structure:
				p.hub_score = 0.0
				for r in self.structure[p]:
					#print r, r.auth_score
					p.hub_score += r.auth_score
				norm += math.pow(p.hub_score,2)
			norm = math.sqrt(norm)
			#print "norm:",norm
			for p in self.structure:
				p.hub_score = p.hub_score / norm
			delta=0
			for key in self.structure:
				delta+=abs(prev_hub_score[key] - key.hub_score)
			#print("Delta:",delta)
			if delta==min_delta:
				# for each in self.structure:
				# 	print(each.name," ",each.auth_score," ",each.hub_score)
				return


		#self.printNodes()

	def HITS(self):
		for key in self.structure:
			key.HITS_score=(key.hub_score+key.auth_score)/2
		#print("HITS")
		# for key in self.structure:
			# print(key.name," ",key.HITS_score," ",key.position)

	def sort_nodes_hits(self,n):
		#print self.structure.keys()
		# print "sorted n list "
		final_list = sorted(self.structure.keys())[:n]
		#print final_list
		# for each in final_list:
			# print each.name,each.HITS_score,each.position

		position_sorted=sorted(final_list)
		# print
		# print "sorted on position"
		sorted_x = sorted(final_list, key=operator.attrgetter('position'))
		# for each in sorted_x:
			# print each.name,each.HITS_score,each.position
		return sorted_x

	def sort_nodes_textrank(self,n):
		#print self.structure.keys()
		# print "sorted n list "
		final_list = sorted(self.structure.keys(), key=operator.attrgetter('PRscore'),reverse=True)[:n]
		#print final_list
		# for each in final_list:
			# print each.name,each.PRscore,each.position

		position_sorted=sorted(final_list)
		# print
		# print "sorted on position"
		sorted_x = sorted(final_list, key=operator.attrgetter('position'))
		# for each in sorted_x:
			# print each.name,each.PRscore,each.position
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

def hitsMain(input_data,n):
	graph=Graph()
	# print input_data
	data=readData(input_data,'english')
	#graph.set_structure([["d1","d2"],["d1","d3"],["d2","d1"],["d2","d3"],["d3","d2"],["d3","d4"],["d4","d2"]])
	# print data
	graph.set_structure(data)
	# graph.hubs_and_authorities()
	# graph.HITS()
	# answer=graph.sort_nodes_hits(n)
	graph.textRank()
	answer=graph.sort_nodes_textrank(n)
	result=[]
	for item in answer:
		result.append(item.name)
	return result


#hitsMain(int(sys.argv[1]))
