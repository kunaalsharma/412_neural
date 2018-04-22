function make_distances_from_wAdj(inputname, numInputMats)

%%% Makes distance matrix from weighted adjactency matrix
%%% INPUT: Output name from makeAllGraphs, number of adjacency matrices matrices

for i = 1:numInputMats
    
    Matrix = importdata(sprintf('%s%d.txt',inputname,i-1));
    
    Matrix = abs(Matrix);
    
    matfilename = sprintf('%s%d',inputname,i-1);
    
    save(matfilename,'Matrix'); % Saves adjacency matrix as .mat file
    
    adj_matrix_to_edge_list(matfilename,matfilename);
    
    edgefilename = sprintf('%s_edge_list.txt',matfilename);
    
    edgelist_to_point_cloud_dist_mat(edgefilename,'inv'); % Creates distance matrix
    
    delete(sprintf('%s.mat',matfilename));
    delete(edgefilename)
end

