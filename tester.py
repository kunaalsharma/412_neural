import numpy,os,sys,stage3

#creates test matrices for stage3 pipeline

a = numpy.matrix([[0,1,1,1,1],
	[1,0,1,1,1],
	[1,1,0,1,0],
	[1,1,1,0,1],
	[1,1,0,1,0]])

numpy.savetxt("test.txt",a,fmt="%d")
print(stage3.main(["","test.txt"]))
