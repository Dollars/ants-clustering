from random import choice

class Ant:
	def __init__(self,position,boardDimension):
		self.position = position
		self.boardDimension = boardDimension
		self.isCarrying = False

	#executes nbSteps movement steps and return the new position
	def move(self,nbSteps = 1):
		for steps in range (nbSteps):
			moveDirection = choice(range(len(self.position)))
			self.position[moveDirection]+= choice([-1,1])
			
			#Check validity of move. If moved the ant out of the board, place it back on the board at the nearest position
			if(self.position[moveDirection]<0):
				self.position[moveDirection] = 0
			elif(self.position[moveDirection]>=self.boardDimension):
				self.position[moveDirection]=self.boardDimension-1
		return self.position

	def carrying(self):
		return self.isCarrying
	
	#return the value of the carried datapoint, or void if no datapoint was carried
	def drop(self):
		if self.isCarrying:
			self.isCarrying = False
			return self.datapoint

	#return true if the new datapoint was picked-up correctly
	def pickup(self,datapoint):
		if not self.isCarrying:
			self.isCarrying = True
			self.datapoint = datapoint
			return True
		return False
	
	#peek at the value of the datapoint held. Returns void if no datapoint carried
	def peek(self):
		if self.isCarrying:
			return self.datapoint

	def getPos(self):
		return self.position
