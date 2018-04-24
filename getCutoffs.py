import numpy,os,sys,stage3,makeAllGraphs
import matplotlib.pyplot as plt
import networkx as nx

'''
Generates adjacency matrices for different cutoff values and also computes betti numbers
for these matrices.

main([string outputfilename,float cutoff_step]) 
'''

directory = "unweightedAdjacencyMatrices/"
bdirectory = "bettiCurves/"

def main(argv):
	if len(argv)<2:
		print("Argument format should be: main([string output_filename,int cutoff_step, -t])\n")
		return
	global filename 
	filename = argv[0].replace(".txt","")
	cutoff_step = float(argv[1])
	generateCutoffs(cutoff_step)
	computeBetti(filename,cutoff_step)
	return


#runs makeAllGraphs for each step between 0 and 1 according to the cutoff
def generateCutoffs(cutoff_step):
	for i in [x/1000.0 for x in range(50,1000,int(cutoff_step*1000))]:
		makeAllGraphs.main(["",i,"-uw","-b",filename+str(i).replace(".","")])
	return

#computes the betti numbers for each file generated in the previous step
def computeBetti(filename,cutoff_step):
	for j in range(0,10):
		bfile = bdirectory + "iter"+str(j)+".txt"
		nums = []
		for i in [x/1000.0 for x in range(50,1000,int(cutoff_step*1000))]:
			(betti0,betti1)= stage3.main([directory+filename+str(i).replace(".","")+str(j)+".txt"])
			print("Iteration: %d, cutoff: %f. Betti 0: %d, Betti 1: %d")%(j,i,betti0,betti1)
			nums.append([betti0,betti1])
		npnums = numpy.array(nums)
		numpy.savetxt(bfile,npnums)
	return

if __name__=="__main__":
	main(sys.argv[1:])