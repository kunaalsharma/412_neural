import numpy,sys,os

#reads in an adjaency matrix, and returns all betti numbers
def main():
	if len(sys.argv)<2:
		print("Please run with arguments\n")
		return (-1,-1)
	file = fopen(sys.argv[1])
	matrix = get_adjacency_matrix(file)
	(vertices,edges,edge_list) = count_edges(matrix)
	boundary_matrix = make_boundary(vertices,edges,edge_list)
	boundary_size = boundary_matrix.shape[0]
	reduced_matrix = reduce_matrix(boundary_matrix)
	return compute_homology(reduced_matrix,vertices)

#return the adjacency matrix from file
def get_adjacency_matrix(filename):
	matrix = np.loadtxt(filename,dtpye=numpy.int)
	return matrix

#returns the number of faces along with a list of all edges
def count_edges(matrix):
	vertices = matrix.shape[0]
	edges = 0
	edge_list = []
	for i in range(0,vertices):
		for j in range(i,vertices):
			if matrix.item(i,j)==1:
				edges++
				edge_list.append((i,j))
	return (vertices,edges,edge_list)

#makes the boundary matrix and returns it
def make_boundary(vertices,edges,edge_list):
	boundary_matrix = numpy.zeroes((vertices+edges,vertices+edges),dtype=numpy.int)
	for num, (i,j) in enumerate(edge_list):
		index = num + vertices
		boundary_matrix[i,index] = 1
		boundary_matrix[j,index] = 1
	return boundary_matrix

#returns the index of the lowest 1 in a column
def get_low(boundary_matrix,j):
	lowest = -1
	matrix_size = boundary_matrix.shape[0]
	for i in range(0,matrix_size):
		if boundary_matrix.item(i,j)==1:
			lowest = i
	return lowest

#checks to see if there is a lower 1 and returns the index
def has_lower(boundary_matrix,j):
	if j==0:
		return -1
	for i in range(0,j):
		if get_low(boundary_matrix,i)==get_low(boundary_matrix,j):
			return i
	return -1

#adds two columns modulo 2 and returns the result
def add_column(boundary_matrix,low,high):
	matrix_size = boundary_matrix.shape[0]
	for i in range(0,matrix_size):
		if boundary_matrix.item(i,low)==1:
			if boundary_matrix.item(i,high)==1:
				boundary_matrix[i,high]=0
			else:
				boundary_matrix[i,high]=1
	return boundary_matrix

#returns a reduced boundary matrix
def reduce_matrix(boundary_matrix):
	matrix_size = boundary_matrix.shape[0]
	for i in range(0,matrix_size):
		low_index = has_lower(boundary_matrix,i)
		while(low_index!=-1):
			boundary_matrix = add_column(boundary_matrix,low_index,i)
			low_index = has_lower(boundary_matrix,i)
	return boundary_matrix

#returns betti 0 and betti 1
def compute_homology(reduced_matrix,vertices):
	lowest_ones = []
	matrix_size = reduced_matrix.shape[0]
	for i in range(0,matrix_size):
		lowest_ones.append(get_low(reduced_matrix,i))

	z0,b0,z1,b1 = 0,0,0,0

	for i in range(0,vertices):
		if lowest_ones[i]==-1:
			z0++
		for j in lowest_ones:
			if j==i:
				b0++
	for i in range(vertices,matrix_size):
		if lowest_ones[i]==-1:
			z1++
		for j in lowest_ones:
			if j==i:
				b1++
	return (z0-b0,z1-b1)
	

if __name__=="__main__":
	main()




