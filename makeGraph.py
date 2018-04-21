'''
Documentation Quick Links
TF Variable https://www.tensorflow.org/api_docs/python/tf/Variable
'''

import sys
import numpy as np
#import plotly
#import plotly.plotly as py
#from plotly.graph_objs import *
#import networkx as nx
#plotly.tools.set_credentials_file(username='talhankoc', api_key='k8lhtIVuXtG90WkEUvsC')

global _vertices
global _vertCount
_vertices = []
_vertCount = 0
_inputLayerLen = 784
_outputLayerLen = 10


def main(argv):
	pass


# Plots to plotly domain

def plot():
	#TODO
	return

def graphToAdjacencyMatrix(G):
	#TODO
	return 

################################################

def makeGraph(Weights, Biases, cutoff):
	#print(Weights, '\n',Biases)
	global _vertices
	global _vertCount
	_edges = []
	_vertices = []
	_vertCount = 0
	for w,b in zip(Weights,Biases):
		#print(w, '\n',b)
		#print('w and b shape : ', w.shape, b.shape )
		shape, edges = getEdgesWithCutoff(w, b, cutoff)
		_edges += edges
	# get edges layer by layer
	addVertices(_outputLayerLen)
	return (_vertices, _edges)

# Assumes vertices for bottom layer have been created
# Creates vertices for the next layer (top)
# Returns shape of matrix and list of edges
# NOTE: Edges are formatted with nodes numbered 0 to (n-1) and 0 to (m-1) for bottom and top layer
def getEdgesWithCutoff(weights, biases, cutoff):
	m = np.concatenate((weights,biases), 0) #if (biases.any()) else weights

	addVertices(m.shape[0]) #bottom nodes
	bottom_offset = _vertices[-m.shape[0]]
	top_offset = _vertices[-1] + 1

	makeAbsolute(m)
	highest = getHighest(m)
	#print("Highest =",highest)
	normalize(m,highest)
	indices = getWeightsByStrength(m,cutoff)
	indices = [(x[0]+bottom_offset, x[1]+top_offset) for x in indices]
	#for i in indices:
		#print(i)
	return (m.shape, indices)

#starts counting from 1
def addVertices(l):
	for _ in range(l):
		c = len(_vertices) + 1
		_vertices.append(c)

def makeAbsolute(m):
	for i in range(m.shape[0]):
		for j in range(m.shape[1]):
			m[i,j] = abs(m[i,j])

def getHighest(m):
	highest = 0
	for x in np.nditer(m):
		if highest < x:
			highest = x
	return highest

def normalize(m,val):
	for i in range(m.shape[0]):
		for j in range(m.shape[1]):
			m[i,j] /= val

def getWeightsByStrength(m,strength):
	#i shows which node it's going to
	#j shows which node it's coming from
	ret = []
	for i in range(m.shape[0]):
		for j in range(m.shape[1]):
			if m[i,j] > strength:
				ret.append((i,j))
	return ret



if __name__ == "__main__":
    main(sys.argv)
