from AntsCemetery import *

class AntsCemeteryNormalized (AntsCemetery):
	def __init__(self,dataset,dropFactor,pickupFactor,antMovementQuantifier = 1,neighborhoodGetter = AntsCemetery.getNeighborhood_8neighbors,sizeProportion = 4,antsProportion = 1/10.0):
		super().__init__(dataset,dropFactor,pickupFactor,antMovementQuantifier,neighborhoodGetter,sizeProportion,antsProportion)
		self.minDist=0
		self.maxDist=0
		if (self.nbDataPoints>1):
			dist=self.dataset[0].distance(self.dataset[1])
			self.minDist=dist
			self.maxDist=dist
		for i in range(self.nbDataPoints):
			for j in range(i,self.nbDataPoints):
				dist=self.dataset[i].distance(self.dataset[j])
				self.maxDist=max(dist,self.maxDist)
				self.minDist=min(dist,self.minDist)
		self.max_minus_minDist = self.maxDist-self.minDist
	
	def distanceNorm(self,dataPointA,dataPointB):
		dist = dataPointA.distance(dataPointB)
		return (dist - self.minDist)/self.max_minus_minDist
