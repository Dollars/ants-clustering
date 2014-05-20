from random import choice
from AntsCemetery import *
from AntsCemeteryNormalized import *
from Datapoint import *

class ColorPixel(Datapoint) :
	maxDistance = sqrt((255.0**2)*3)
	def __init__(self,red,green,blue):
		self.red = red
		self.green = green
		self.blue = blue
	def getValue(self):
		return (self.red,self.green,self.blue)
	def distance(self,other):
		otherColors = other.getValue()
		otherRed = otherColors[0]
		otherGreen = otherColors[1]
		otherBlue = otherColors[2]
		return sqrt((self.red-otherRed)**2 + (self.green-otherGreen)**2 + (self.blue-otherBlue)**2)
	def __str__(self):
		return "#{0:0>2X}{1:0>2X}{2:0>2X}".format(self.red,self.green,self.blue)

class ColorPixel_otherDistance(ColorPixel) :
	maxDistance = sqrt((255.0)*3)
	def __init__(self,red,green,blue):
		super().__init__(red,green,blue)
	def distance(self,other):
		otherColors = other.getValue()
		otherRed = otherColors[0]
		otherGreen = otherColors[1]
		otherBlue = otherColors[2]
		return (abs(self.red-otherRed) + abs(self.green-otherGreen) + abs(self.blue-otherBlue))

if __name__ == "__main__":
	dataset = []
	range1 = range(16)
	range2 = range(105,121)
	range3 = range(240,256)
	for i in range (30):
		dataset.append(ColorPixel_otherDistance(choice(range3),choice(range1),choice(range1)))#Mostly red pixels
		dataset.append(ColorPixel_otherDistance(choice(range1),choice(range3),choice(range1)))#Mostly green pixels
		dataset.append(ColorPixel_otherDistance(choice(range1),choice(range1),choice(range3)))#Mostly blue pixels
			
		#dataset.append(ColorPixel(choice(range2),choice(range2),choice(range2)))#Mostly grey (?) pixels
	
	ac = AntsCemeteryNormalized(dataset,0.6,0.6,3,AntsCemetery.getNeighborhood_8neighbors)
	print (ac)
	print ("\nInitial solution quality : "+str(ac.getSolutionQuality()))
	print ("\n --------------------------------------------------- \n")
	ac.iterate(100000)
	ac.finalize()
	
	print (ac)
	print ("\nFinal solution quality : "+str(ac.getSolutionQuality()))

	print ("\n --------------------------------------------------- \n")
	print (ac.metaRepr())
