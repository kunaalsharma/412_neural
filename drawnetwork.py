import stage3 as s3
import os

for file in os.listdir("unweightedAdjacencyMatrices/"):
	if file !=".DS_Store":
		print(file)
		(vertices,edges,edge_list) = s3.count_edges(s3.get_adjacency_matrix("unweightedAdjacencyMatrices/"+file))
		s3.draw_network(vertices,edge_list,"network_images1/"+file.replace(".txt",".png"))
