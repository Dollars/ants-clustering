class Datapoint:
	maxDistance = 1.0
	def __init__(self):
		pass
	def distanceNorm(self,other):
		return self.distance(other)/self.maxDistance
	def distance(self,other):
		return 1
	def __str(self):
		return ("You forgot to redefine the __str__ !")
