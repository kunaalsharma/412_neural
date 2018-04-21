import sys
import makeGraph
import makeGraphNoBias
import numpy as np



path = 'snapshots/'
savePathUnweighted = 'unweightedAdjacencyMatrices'
savePathWeighted = 'weightedAdjacencyMatrices'
number_of_models = 10



def main(argv):
	cutoff = 0.5
	saveName = None
	graphs = []

	if len(argv) > 1:
		cutoff = float(argv[1])
	else:
		print('No cutoff value was given. Default is 0.5')

	if len(argv) > 2:
		saveName = str(argv[2])
	else:
		print('No filename was given for saving. Adjacency matrix will not be saved.')

	

	if len(argv) > 3 and argv[3] == '-nb':
		print('Creating graphs without including the biases')
		graphs = nobiases(cutoff)
	else:
		print('Creating graphs including the biases')
		graphs = withbiases(cutoff)

	if saveName != None:
		i = 0
		for graph in graphs:
			saveReadable(graphToAdjacencyMatrix(graph), saveName+str(i))
			i+=1




def nobiases(cutoff):
	
	graphs = []
	for i in range(number_of_models):
		print('\nITERATION:' + str(i))
		w1 = np.loadtxt(path+'W1-' + str(i)+'.npy', delimiter=',')
		w2 = np.loadtxt(path+'W2-' + str(i)+'.npy', delimiter=',')
		G = makeGraphNoBias.makeGraph([w1,w2], cutoff)
		graphs.append(G)

		print('Vertices:', len(G[0]),'\tEdges:',len(G[1]))
	
	return graphs		


def withbiases(cutoff):
	
	graphs = []
	for i in range(number_of_models):
		print('\nITERATION:' + str(i))
		w1 = np.loadtxt(path+'W1-' + str(i)+'.npy', delimiter=',')
		w2 = np.loadtxt(path+'W2-' + str(i)+'.npy', delimiter=',')
		b1 = np.loadtxt(path+'b1-' + str(i)+'.npy', delimiter=',')
		b2 = np.loadtxt(path+'b2-' + str(i)+'.npy', delimiter=',')
		b1 = np.reshape(b1, (1, -1))
		b2 = np.reshape(b2, (1, -1))
		G = makeGraph.makeGraph([w1,w2],[b1,b2], cutoff)
		graphs.append(G)
		print('Vertices:', len(G[0]),'\tEdges:',len(G[1]))
		
	return graphs

def intersect(a,b):
	return None#[x for x,y in zip(a,b) if (x[0] == y[0] and x[1] == y[1])]

def graphToAdjacencyMatrix(G):
	dim = len(G[0])
	print('dim =',dim)
	m = np.zeros((dim,dim))
	for edge in G[1]:
		m[edge[0]-1,edge[1]-1] = 1
		m[edge[1]-1,edge[0]-1]
	assert adjacencyErrorCheck(m), 'Error in Adjacency Matrix'
	return m

def adjacencyErrorCheck(m):
	#make sure no node is connected to self
	for i in range(m.shape[0]):
		if m[i,i] != 0:
			return False
	#785th node is bias1
	#1086th node is boas2
	#TODO check that no node from below is connected to these
	return True


def save(m, filename):
	saveBinary(m,filename)
	saveReadable(m,filename)

def saveBinary(m, filename):
	#Binary data
	np.save(savePathUnweighted+'/'+filename+'.npy', m)

def saveReadable(m, filename):

	#Human readable data
	np.savetxt(savePathUnweighted+'/'+filename+'.txt', m)

if __name__ == '__main__':
	main(sys.argv)