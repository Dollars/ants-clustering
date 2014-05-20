from random import choice
from AntsCemetery import *
from Datapoint import *

class GreyScalePixel(Datapoint) :
	maxDistance = 255.0
	def __init__(self,value):
		self.value = value
	def getValue(self):
		return self.value
	def distance(self,other):
		return abs(self.value - other.getValue())
	def __str__(self):
		return str(self.value)

if __name__ == "__main__":
	dataset = []
	range1 = range(16)
	range2 = range(105,121)
	range3 = range(240,256)
	for i in range (30):
		dataset.append(GreyScalePixel(choice(range1)))
		dataset.append(GreyScalePixel(choice(range2)))
		dataset.append(GreyScalePixel(choice(range3)))
	
	ac = AntsCemetery(dataset,0.15,0.15)
	print (ac)
	print ("\nInitial solution quality : "+str(ac.getSolutionQuality()))
	print ("\n --------------------------------------------------- \n")
	ac.iterate(100000)
	ac.finalize()
	
	print (ac)
	print ("\nFinal solution quality : "+str(ac.getSolutionQuality()))

	print ("\n --------------------------------------------------- \n")
	print (ac.metaRepr())
