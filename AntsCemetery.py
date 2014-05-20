from math import ceil,sqrt
from random import sample,random
from Ants import *

class AntsCemetery :
	#antsProportion should always be < sizeProportions (otherwise there would be more ants than board positions)

	@staticmethod
	def getNeighborhood_8neighbors(pos):
		neighbors = []
		for i in range(pos[0]-1,pos[0]+2):
				for j in range(pos[1]-1,pos[1]+2):
					neighbors.append((i,j))
		neighbors.remove(pos)
		return neighbors
	
	@staticmethod
	def getNeighborhood_4neighbors(pos):
		neighbors = []
		for i in range(len(pos)):
			copyPos=list(pos)
			copyPos[i]=pos[i]-1
			neighbors.append(tuple(copyPos))
			copyPos[i]=pos[i]+1
			neighbors.append(tuple(copyPos))
		return neighbors
	
	def __init__(self,dataset,dropFactor,pickupFactor,antMovementQuantifier = 1,neighborhoodGetter = getNeighborhood_8neighbors,sizeProportion = 4,antsProportion = 1/10.0):
		self.antMovementQuantifier = antMovementQuantifier

		self.getNeighborhood = neighborhoodGetter.__get__(None,AntsCemetery)

		self.sizeProportion = sizeProportion
		self.antsProportion = antsProportion		
		
		self.dataset = dataset
		self.dropFactor = dropFactor
		self.pickupFactor = pickupFactor
		
		self.nbDataPoints = len(dataset)
		self.boardDimension = int(ceil(sqrt(self.nbDataPoints*self.sizeProportion)))
		
		self.board = {} #a sparse matrix ; a.k.a a dictionnary whose keys are 
		boardPositions = []
		for i in range (self.boardDimension):
			for j in range (self.boardDimension):
				boardPositions.append([i,j])
		
		dataPointsPositions = sample(boardPositions,self.nbDataPoints)
		for i in range (self.nbDataPoints):
			self.board[tuple(dataPointsPositions[i])] = self.dataset[i]
		self.nbAnts = int(ceil(self.nbDataPoints * self.antsProportion))
		self.ants = []
		antsPositions = sample(boardPositions,self.nbAnts)
		for i in range (self.nbAnts):
			self.ants.append(Ant(dataPointsPositions[i],self.boardDimension))

	def iterate(self,nbIter = 1, show = None, **kwargs):
		if nbIter>1:
			for i in range (nbIter):
				self.iterate(1, show=show, **kwargs)
		else:
			for ant in self.ants:
				if ant.carrying():
					prob = self.probToDrop(ant)
					r = random()
					if r<prob:
						self.board[tuple(ant.getPos())] = ant.drop()
				else :
					prob = self.probToPickup(ant)
					r = random()
					if r<prob:
						ant.pickup(self.board.pop(tuple(ant.getPos())))
				ant.move(self.antMovementQuantifier)
		if(show != None):
			show(self, **kwargs)
	
	def finalize(self):
		nbCarrying = 0
		for ant in self.ants :
			if ant.carrying():
				nbCarrying+=1
		while (nbCarrying > 0):
			for ant in self.ants :
				if ant.carrying():
					prob = self.probToDrop(ant)
					r = random()
					if r<prob:
						self.board[tuple(ant.getPos())] = ant.drop()
						nbCarrying-=1
					ant.move(self.antMovementQuantifier)
	
	def probToDrop(self,ant):
		prob = 0
		pos = tuple(ant.getPos())
		if ant.carrying() and not(pos in self.board):
			datapoint = ant.peek()
			f = self.neighborsResemblance(datapoint,pos)
			prob = (f/(self.dropFactor + f))**2
		return prob

	def probToPickup(self,ant):
		prob = 0
		pos = tuple(ant.getPos())
		if not(ant.carrying()) and pos in self.board:
			datapoint = self.board[pos]
			f = self.neighborsResemblance(datapoint,pos)
			prob = (self.pickupFactor/(self.pickupFactor + f))**2
		return prob
		
	def neighborsResemblance(self,datapoint,pos):
		total = 0
		neighbors = self.getNeighborhood(pos)
		#sum(...
		for neighbor in neighbors:
			if neighbor in self.board:
				total+=(1 - self.distanceNorm(datapoint,self.board[neighbor])) # 1 - d(o1,o2)
		#...)/Neigh
		return total/len(neighbors)
	
	def getSolutionQuality(self):
		total = 0
		for pos in self.board:
			total += self.neighborsResemblance(self.board[pos],pos)
		return total/self.nbDataPoints
	
	def distanceNorm(self,dataPointA,dataPointB):
		return dataPointA.distanceNorm(dataPointB)

	#Returns the maximun,minimum value of neighbors distance in the board 
	def getDistanceBounds(self):
		minBound = 1.1
		maxBound = -0.1
		for pos in self.board:
			neighbors = self.getNeighborhood(pos)
			for neighbor in neighbors:
				if neighbor in self.board:
					distance = self.distanceNorm(self.board[pos],self.board[neighbor])
					minBound = min(minBound,distance)
					maxBound = max(maxBound,distance)
		return (maxBound,minBound)

	def shiftPos(self,pos):
		shiftedPos = []
		for i in pos:
			shiftedPos.append(i*2)
		return tuple(shiftedPos)

	def getInbetweenPos(self,firstPos,scndPos):
		res = []
		shiftedPos=self.shiftPos(firstPos)
		for i in range(len(firstPos)):
			vector = firstPos[i]-scndPos[i]
			res.append(shiftedPos[i]-vector)
		return tuple(res)

	#Get the meta data (the meta data represented being the distance between neighboring datapoint)representation of the board ; 
	# where each datapoint has been replaced by a (R,G,B) tuple corresponding to its neighborhood resemblance.
	"""
	____________		__________________
	| Data Data |		| Data Dist Data |
	| Data Data | 	==> 	| Dist Dist Dist |
	|___________|		| Data Dist Data |
				|________________|
	"""
	def getMetaDataColorBoard(self):
		dataPointColor = (255,255,255)
		emptyColor = (0,0,0)
		bounds = self.getDistanceBounds()
		maxBound = bounds[0]
		minBound = bounds[1]
		denom = maxBound - minBound
		metaBoard = {}
		blue = 0
		for pos in self.board:
			shiftedPos = self.shiftPos(pos)
			metaBoard[shiftedPos] = [dataPointColor]
			neighbors = self.getNeighborhood(pos)
			for neighbor in neighbors:
				if neighbor in self.board:
					distance = self.distanceNorm(self.board[pos],self.board[neighbor])
					normDistance = (distance - minBound) / denom
					red = 255*normDistance
					green = 255-red
					inbetweenPos = self.getInbetweenPos(pos,neighbor)
					if inbetweenPos in metaBoard:
						metaBoard[inbetweenPos].append((red,green,blue))
					else:
						metaBoard[inbetweenPos]=[(red,green,blue)]
		#metaMatrix = [[emptyColor for i in range((self.boardDimension * 2))] for j in range((self.boardDimension * 2))]
		
		#Build the matrix by averaging the values of each point where multiple distances coincide
		for pos in metaBoard:
			nbColorPoints=len(metaBoard[pos])
			color = [0,0,0]
			if (nbColorPoints > 1) :
				for c in metaBoard[pos]:
					for i in range(len(c)):
						color[i]+=c[i]
				for i in range(len(color)):
					color[i] = int(round(color[i]/nbColorPoints))
			else:
				color = metaBoard[pos][0]
			#metaMatrix[pos[0]][pos[1]] = tuple(color)
			metaBoard[pos]=color
			
		return metaBoard
	
	#TODO removeme
	def metaRepr(self):
		metaMatrix = self.getMetaDataColorBoard()
		res = ""
		for i in range (self.boardDimension * 2):
			for j in range (self.boardDimension * 2):
				res+="  "
				if (i,j) in metaMatrix:
					if metaMatrix[(i,j)][0] > metaMatrix[(i,j)][1]:
						res+="r"
					elif metaMatrix[(i,j)][0] < metaMatrix[(i,j)][1]:
						res+="g"
					else:
						res+="b"
				else:
					res+= " "
			res+="\n"

		return res
	def __str__(self):
		res = ""
		for i in range (self.boardDimension):
			for j in range (self.boardDimension):
				res+="\t"
				if (i,j) in self.board :
					res+=str(self.board[(i,j)])
				else:
					res+="-"
			res+="\n"

		return res
