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
    
    shortest_paths(edgefilename); % Creates distance matrix
    
    delete(sprintf('%s.mat',matfilename));
    delete(edgefilename);
    
    distancefilename = sprintf('%s_edge_list_SP_distmat.txt',matfilename);
    distances = importdata(distancefilename);
    numpoints = size(distances,1);
    mindist = min(min(distances(distances > 0)));
    maxdist = max(max(distances));
    
    fid = fopen(sprintf('%s_distances.txt',matfilename),'w');
    fprintf(fid,'%d\n',numpoints);
    fclose(fid);
    
    fid = fopen(sprintf('%s_distances.txt',matfilename),'a');
    fprintf(fid,sprintf('0 %f %d 3\n',[mindist,ceil(maxdist/mindist)]));
    fclose(fid);
    
    fid = fopen(sprintf('%s_distances.txt',matfilename),'a');
    fprintf(fid,'%s\n',mat2str(distances));
    fclose(fid);
    
    delete(distancefilename);
end



