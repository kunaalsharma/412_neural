import sys
import makeGraph
import makeGraphNoBias
import numpy as np



path = 'snapshots/'
savePathUnweighted = 'unweightedAdjacencyMatrices'
savePathWeighted = 'weightedAdjacencyMatrices'
number_of_models = 10



def main(argv):
	assert len(argv) >= 4, 'ERROR: Please enter required paramters. See readme.txt ...'
	cutoff = float(argv[1])
	saveName = None
	matrices = []

	if argv[2] == '-w':
		if argv[3] == '-nb':
			print('Creating weighted adjacency matrix without including the biases')
			matrices = getWeightedAdjacencyMatrixNoBias()
		elif argv[3] == '-b':
			print('Creating weighted adjacency matrix, including the biases')
			matrices = getWeightedAdjacencyMatrix()
		else:
			print('ERROR: incorrect flag. Please specify -b to include biases and -nb for no biases.')
	elif argv[2] == '-uw':
		if argv[3] == '-nb':
			print('Creating graphs without including the biases')
			matrices = nobiases(cutoff)
		elif argv[3] == '-b':
			print('Creating graphs including the biases')
			matrices = withbiases(cutoff)
		else:
			print('ERROR: incorrect flag. Please specify -b to include biases and -nb for no biases.')

	else:
		print('ERROR: incorrect flag. Please specify -w for weighted and -uw for unweighted as the second parameter.')

	

	if len(argv) > 4:
		saveName = str(argv[4])
	else:
		print('No filename was given for saving. Adjacency matrix will not be saved.')
	
	if saveName != None:
		i = 0
		for m in matrices:
			saveReadable(m, saveName+str(i))
			i+=1




def nobiases(cutoff):
	
	matrices = []
	for i in range(number_of_models):
		print('\nITERATION:' + str(i))
		w1 = np.loadtxt(path+'W1-' + str(i)+'.npy', delimiter=',')
		w2 = np.loadtxt(path+'W2-' + str(i)+'.npy', delimiter=',')
		G = makeGraphNoBias.makeGraph([w1,w2], cutoff)
		matrices.append(graphToAdjacencyMatrix(G))
		print('Vertices:', len(G[0]),'\tEdges:',len(G[1]))

	return matrices		


def withbiases(cutoff):
	
	matrices = []
	for i in range(number_of_models):
		print('\nITERATION:' + str(i))
		w1 = np.loadtxt(path+'W1-' + str(i)+'.npy', delimiter=',')
		w2 = np.loadtxt(path+'W2-' + str(i)+'.npy', delimiter=',')
		b1 = np.loadtxt(path+'b1-' + str(i)+'.npy', delimiter=',')
		b2 = np.loadtxt(path+'b2-' + str(i)+'.npy', delimiter=',')
		b1 = np.reshape(b1, (1, -1))
		b2 = np.reshape(b2, (1, -1))
		G = makeGraph.makeGraph([w1,w2],[b1,b2], cutoff)
		matrices.append(graphToAdjacencyMatrix(G))
		print('Vertices:', len(G[0]),'\tEdges:',len(G[1]))
		
	return matrices

def getWeightedAdjacencyMatrix():
	graphs = []
	for i in range(number_of_models):
		print('\nITERATION:' + str(i))
		w1 = np.loadtxt(path+'W1-' + str(i)+'.npy', delimiter=',')
		w2 = np.loadtxt(path+'W2-' + str(i)+'.npy', delimiter=',')
		b1 = np.loadtxt(path+'b1-' + str(i)+'.npy', delimiter=',')
		b2 = np.loadtxt(path+'b2-' + str(i)+'.npy', delimiter=',')
		b1 = np.reshape(b1, (1, -1))
		b2 = np.reshape(b2, (1, -1))

		dim = w1.shape[0] + 1 + w2.shape[0] + 1 + w2.shape[1]
		m = np.zeros((dim,dim))

		inputLayerOffset = w1.shape[0] # +1 for bias layer and +1 for next starting point
		hiddenLayerOffset = inputLayerOffset + 1 + w2.shape[0]
		
		#place w1
		placeSmallerInBiggerMatrix(0, inputLayerOffset + 1, w1,m)
		print('successfully placed w1')

		#place b1
		placeSmallerInBiggerMatrix(inputLayerOffset, inputLayerOffset + 1, b1,m)
		print('successfully placed b1')

		#place w2
		placeSmallerInBiggerMatrix(inputLayerOffset+1, hiddenLayerOffset + 1, w2, m)
		print('successfully placed w2')
		#place b2
		placeSmallerInBiggerMatrix(hiddenLayerOffset, hiddenLayerOffset + 1, b2, m)
		print('successfully placed b2')

		assert check_symmetric(m)
		graphs.append(m)

	return graphs

def getWeightedAdjacencyMatrixNoBias():
	graphs = []
	for i in range(number_of_models):
		print('\nITERATION:' + str(i))
		w1 = np.loadtxt(path+'W1-' + str(i)+'.npy', delimiter=',')
		w2 = np.loadtxt(path+'W2-' + str(i)+'.npy', delimiter=',')
		b1 = np.loadtxt(path+'b1-' + str(i)+'.npy', delimiter=',')
		b2 = np.loadtxt(path+'b2-' + str(i)+'.npy', delimiter=',')
		b1 = np.reshape(b1, (1, -1))
		b2 = np.reshape(b2, (1, -1))

		dim = w1.shape[0] + w2.shape[0] + w2.shape[1]
		m = np.zeros((dim,dim))

		inputLayerOffset = w1.shape[0] # +1 for bias layer and +1 for next starting point
		hiddenLayerOffset = inputLayerOffset + w2.shape[0]

		#place w1
		placeSmallerInBiggerMatrix(0, inputLayerOffset, w1,m)
		print('successfully placed w1')

		#place w2
		placeSmallerInBiggerMatrix(inputLayerOffset, hiddenLayerOffset, w2, m)
		print('successfully placed w2')

		assert check_symmetric(m)
		graphs.append(m)

	return graphs

def placeSmallerInBiggerMatrix(rowOffset,colOffset, smaller,bigger):
	for i in range(0, smaller.shape[0]):
		for j in range(0, smaller.shape[1]):			
			bigger[i+rowOffset,j+colOffset] = smaller[i,j]
			bigger[j+colOffset, i+rowOffset] = smaller[i,j]


def check_symmetric(a, tol=1e-8):
    return np.allclose(a, a.T, atol=tol)



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