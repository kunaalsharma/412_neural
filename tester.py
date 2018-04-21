import numpy,os,sys,stage3

#creates test matrices for stage3 pipeline

filename = "unweightedAdjacencyMatrices/cutOffTenth"

for i in range(9,-1,-1):
	currfile = filename + str(i) + ".txt"
	print(stage3.main(["",currfile]))