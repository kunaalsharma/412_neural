import numpy,os,sys,stage3

#creates test matrices for stage3 pipeline

filename = "unweightedAdjacencyMatrices/cutOffTenth"

for i in range(0,1):
	currfile = filename + str(i) + ".txt"
	print(stage3.main([True,currfile]))