import matplotlib.pyplot as plt
import numpy, time

for i in range(0,10):
	string = "bettiCurves/iter%d.txt" % i
	matrix = numpy.loadtxt(string)
	plt.plot(matrix[:,1])
	string2 = "bettiCurves/all_betti1_%d.png" %i
	plt.savefig(string2)
