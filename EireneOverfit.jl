include("/Users/joetharayil/Documents/Topology/PH-roadmap-master/matlab/Eirene0_3_7/Eirene0_3_7.jl");

for i = 2:100
    dist2 = readdlm("412_neural/overfitWeightedAdjacencyMatrices/Overfitmats$(i)_edge_list_SP_distmat.txt");
    dist2 = Symmetric(dist2);
    C2Over = eirene(dist2,bettimax=1);
    writedlm("412_neural/VR_Betti/Over_$(i)_Betti_2.txt",betticurve(C2Over,dim=2),",");
end
