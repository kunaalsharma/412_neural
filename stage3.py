import numpy,sys,os

'''
Computes betti 0 and betti1 for an abstract graph saved as an adjacency matrix.
argv = ["", filename] where filename is a file with a numpy saved adjacency matrix in it

'''

def main(argv):
	global b_mat
	global b_size
	global lowest_ones
	lowest_ones=[]
	if len(argv)<1:
		print("Please run with arguments\n")
		return (-1,-1)
	matrix = get_adjacency_matrix(argv[0])
	(vertices,edges,edge_list) = count_edges(matrix)
	b_mat = make_boundary(vertices,edges,edge_list)
	b_size = b_mat.shape[0]
	get_lowest_ones()
	reduce_matrix()
	return compute_homology(vertices)


#return the adjacency matrix from file
def get_adjacency_matrix(filename):
	matrix = numpy.loadtxt(filename)
	return matrix

#returns the number of faces along with a list of all edges
def count_edges(matrix):
	vertices = matrix.shape[0]
	edges = 0
	edge_list = []
	for i in range(0,vertices):
		for j in range(i,vertices):
			if matrix.item(i,j)==1:
				edges+=1
				edge_list.append((i,j))
	return (vertices,edges,edge_list)

#makes the boundary matrix and returns it
def make_boundary(vertices,edges,edge_list):
	b_matrix = numpy.zeros((vertices+edges,vertices+edges),dtype=numpy.int)
	for num, (i,j) in enumerate(edge_list):
		index = num + vertices
		b_matrix[i,index] = 1
		b_matrix[j,index] = 1
	return b_matrix

def get_lowest_ones():
	global lowest_ones
	for i in range(0,b_size):
		lowest_ones.append(get_low(i))


#returns the index of the lowest 1 in a column
def get_low(j):
	for i in range(b_size-1,-1,-1):
		if b_mat.item(i,j)==1:
			return i
	return -1

#checks to see if there is a lower 1 and returns the index
def has_lower(j):
	if j==0 or lowest_ones[j]==-1:
		return -1
	for i in range(0,j):
		if lowest_ones[i]==lowest_ones[j]:
			return i
	return -1

#adds two columns modulo 2 
def add_column(low,high):
	global b_mat
	global lowest_ones
	for i in range(0,b_size):
		if b_mat.item(i,low)==1:
			if b_mat.item(i,high)==1:
				b_mat[i,high]=0
			else:
				b_mat[i,high]=1
	lowest_ones[high] = get_low(high)

#returns a reduced boundary matrix
def reduce_matrix():
	for i in range(0,b_size):
		low_index = has_lower(i)
		while(low_index!=-1):
			add_column(low_index,i)
			low_index = has_lower(i)

#returns betti 0 and betti 1
def compute_homology(vertices):
	z0,b0,z1,b1 = 0,0,0,0
	for i in range(0,vertices):
		if lowest_ones[i]==-1:
			z0+=1
		if i in lowest_ones:
			b0+=1
	for i in range(vertices,b_size):
		if lowest_ones[i]==-1:
			z1+=1
		if i in lowest_ones:
			b1+=1
	return (z0-b0,z1-b1)
	

if __name__=="__main__":
	main(sys.argv[1:])