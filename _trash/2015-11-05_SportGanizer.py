# -*- coding: utf-8 -*-
from numpy import *
import copy

class Team:
	def __init__(self, name = None):
		self.name = name 
		self.matchList = []
	
	###[ NOTE : this one should definitely be private, because it doesn't handle the match itself
	def addMatch(self, match):
		self.matchList.append(match)
	###]

	def isUnnamedAndHasNoMatch(self):
		return ((self.name == None) and (self.matchList == []))
	def rename(self, name):
		self.name = name
	
	def takingPlaceOf(self, team):
		for match in team.matchList:
			match.replace(self,team)
			self.addMatch(match)
		team.matchList = []
		return self
	
	def countScoresFor(self):
		nOfScoreFor = 0
		for match in self.matchList:
			nOfScoreFor += match.getScore(self)
		return nOfScoreFor
	def countScoresAgainst(self):
		nOfScoreAgainst = 0
		for match in self.matchList:
			nOfScoreAgainst += match.getScoreAgainst(self)
		return nOfScoreAgainst
	def countWins(self):
		nOfWins = 0
		for match in self.matchList:
			if match.getWinner() == self: 
				nOfWins += 1
		return nOfWins
	def countLosses(self):
		nOfLosses = 0
		for match in self.matchList:
			if match.getLoser() == self: 
				nOfLosses += 1
		return nOfLosses
	def __lt__(self, team): # NOTE : __lt__ is not the opposite of __gt__ in the case of an exact tie. 
		if self.countWins() == team.countWins():
			if self.countLosses() == team.countLosses():
				if self.countScoresFor() == team.countScoresFor():
					return self.countScoresAgainst() > team.countScoresAgainst()
				else: return self.countScoresFor() < team.countScoresFor()
			else : return self.countLosses() > team.countLosses()
		else: return self.countWins() < team.countWins()

	#To implement : team delete with incidence on matchs, __lt__ conditionned on selected pool, __cmp__ or __gt__


class Match:
	def __init__(self, teamA, teamB, name = None):
		self.name = name

		self.teamA = teamA
		self.teamA.addMatch(self)
		self.teamB = teamB
		self.teamB.addMatch(self)

		self.ended = False
		self.tie = False
		self.scoreA = 0
		self.scoreB = 0
		self.winner = Team(str(self.name)+'-winner')
		self.loser = Team()

	###[ NOTE : this one (used in takingPlaceOf, should be private, because it doesn't handle matchList... then we could code a public version using takingPlaceOf...)
	def replace(self, firstTeam, secondTeam):
		if self.teamA == firstTeam: 
			self.teamA = secondTeam
		elif self.teamB == firstTeam: 
			self.teamB = secondTeam
		elif self.teamA == secondTeam: 
			self.teamA = firstTeam
		elif self.teamB == secondTeam: 
			self.teamB = firstTeam
		else:
			raise ValueError("neither "+str(firstTeam.name)+" nor "+str(firstTeam.name)+" found")
	# private?... we don't want to use this outside Match.endMatch() 
	def setWinner(self, team):
		self.winner = team.takingPlaceOf(self.winner)
	def setLoser(self, team):
		self.loser = team.takingPlaceOf(self.loser)
	###]

	def getScore(self, team):
		if team == self.teamA:
			return self.scoreA
		elif team == self.teamB:
			return self.scoreB
		else:
			raise ValueError("team "+str(team.name)+" not found")
	def getScoreAgainst(self, team):
		if team == self.teamA:
			return self.scoreB
		elif team == self.teamB:
			return self.scoreA
		else:
			raise ValueError("team "+str(team.name)+" not found")	
	def getWinner(self):
		return self.winner
	def getLoser(self):
		return self.loser

	def setScore(self, team, score, secondTeam = None, secondScore = None):
		assert not self.ended
		if secondTeam == None and secondScore == None:
			if team == self.teamA:
				self.scoreA = score
			elif team == self.teamB:
				self.scoreB = score
			else:
				raise ValueError("team "+str(team.name)+" not found") 
		else:
			self.setScore(team,score)
			self.setScore(secondTeam,secondScore)
	
	def endMatch(self, team = None, score = None, secondTeam = None, secondScore = None):
		assert not self.ended
		if not (team==None and score==None and secondTeam==None and secondScore==None):
			self.setScore(team, score, secondTeam, secondScore)
		if self.scoreA > self.scoreB:
			self.setWinner(self.teamA)
			self.setLoser(self.teamB)
		elif self.scoreA < self.scoreB:
			self.setWinner(self.teamB)
			self.setLoser(self.teamA)
		else:
			self.tie = True
			raise ValueError("No tie allowed")
		self.ended = True
	
	# To implement : match location, match time, match versus?, match delete(+ team.removeMatch test)
	# if match already exists, copy itself to the existing match?






class Pool:

	# TODO:
		#createTimeSlots(timeList) and assignTimeSlotsToMatches(timeSlots) OR a function that does both at same time, although that seems too large
		#createLocations(locationList) and assignLocationsToMatches(locations) OR a function that does both at same time, although that seems too large

	def __init__(self, initName = None, initTeamList = []):
		self.name = initName
		self.numberOfTeams = len(initTeamList)
		self.numberOfMatches = 0
		self.teamList = initTeamList
		self.matchList = []

	def rename(self,name):
		self.name = name
		
	def addTeam(self, newTeam):
		if isinstance(newTeam, list):
			self.numberOfTeams += len(newTeam)
			self.teamList.extend(newTeam)
		else:
			self.numberOfTeams += 1
			self.teamList.append(newTeam)
		
	def createMatch(self, teamANumber, teamBNumber, matchName = None):
		self.numberOfMatches += 1
		self.newMatch = Match(self.teamList[teamANumber], self.teamList[teamBNumber], matchName)
		self.matchList.append(self.newMatch)
		
	def ranking(self):
		sortedTeamList = sorted(self.teamList)
		return sortedTeamList
	
	# IMPORTANT: the Pool shall receive the Teams input from the GUI
	
	
class Tournament:
	def __init__(self, name = None):
		self.name = name
		self.poolList = []
			
	def rename(self, name):
		self.name = name

	def addPool(self, pool):
		self.poolList.append(pool)
		
	def removePool(self, pool):
		self.poolList.remove(pool)
	
		
class SingleElimination(Tournament):
	''' Must input a pool with method setInputPool before using other functions. '''
	
	# TODO: 
		#updatePool using the GUI
		#add line in buildFirstPool and buildOtherPools assigning time slots and locations to matchs in each pool via pool.assignTimeSlotsToMatches and pool.assignLocationsToMatches

	def __init__(self):
		Tournament.__init__(self, 'single elimination')
		
	def setInputPool(self, initPool):
		self.inputPool = initPool
		self.inputPool.rename("Pool_1")
		self.addPool(self.inputPool)
	
	def createPoolList(self):
		self.nOfTeamsInLatestPool = len(self.poolList[-1].teamList)
		if self.nOfTeamsInLatestPool == 1:
			print(str(self.poolList[-1].teamList[0].name)+' is the winner of the Tournament!')
			pass
		else:
			self.createPoolMatchListAndPrepareNextPool()
			self.createPoolList()
			
	def createPoolMatchListAndPrepareNextPool(self):
		# Declaring variables for clearer code
		pool = self.poolList[-1]
		nOfTeams = len(pool.teamList)
		self.nOfByes = (2**(int(log2(nOfTeams)+1)))%nOfTeams
		
		# Creating the next pool
		nextPoolNumber = len(self.poolList)+1
		tempPool = Pool('Pool_'+str(nextPoolNumber), []) # BUG : If i dont put (, []) to initialize the teamList, it doesnt work, WTF TABARNAK
		
		# Creating matches in the current pool and adding teams to the next one.
		for i in range(self.nOfByes):
			tempPool.addTeam(pool.teamList[i])
		for i in range((nOfTeams-self.nOfByes)/2):
			nextWorstTeam = nOfTeams-1-i
			nextBestTeam = self.nOfByes + i
			pool.createMatch(nextWorstTeam, nextBestTeam, 'Match_'+str(pool.name[-1])+'-'+str(i+1))
			tempPool.addTeam(pool.matchList[-1].getWinner())
		self.addPool(tempPool)

	'''
	def createPoolList(self):
		#Determine if last pool had a power of two team number
		if len(self.poolList) != 0:
			self.nOfTeamsInLatestPool = len(self.poolList[-1].teamList)
		else:
			self.nOfTeamsInLatestPool = len(self.inputPool.teamList)

		#Create Pools
		if self.nOfTeamsInLatestPool < 2:
			raise ValueError("Cannot create a tournament with less than 2 teams!")
		elif self.nOfTeamsInLatestPool == 2:
			if len(self.poolList) == 0:
				self.createNextPool()
				self.createPoolList()
			elif len(self.poolList) == 1 and len(self.inputPool.teamList) > 2:
				self.createNextPool()
				self.createPoolList()				
			else:
				pass
		else:
			self.createNextPool()
			self.createPoolList()

	def createNextPool(self):
		nextPoolNumber = len(self.poolList)+1
		tempPool = Pool('Pool_'+str(nextPoolNumber), self.createNextPoolTeamList())
		self.createNextPoolMatchList(tempPool)
		self.addPool(tempPool)

	def createNextPoolTeamList(self):
		if len(self.poolList) == 0:
			if not self.nInitialTeamsIsPowerOf2:
				teamList = self.inputPool.teamList[self.nOfByes:]
			else:
				teamList = self.inputPool.teamList
		elif len(self.poolList) == 1:
			if not self.nInitialTeamsIsPowerOf2:
				teamList = self.inputPool.teamList[:self.nOfByes]
				teamList.extend([self.poolList[0].matchList[i].getWinner() for i in range(len(self.poolList[0].matchList))])
			else:
				teamList = [self.poolList[0].matchList[i].getWinner() for i in range(len(self.poolList[0].matchList))]
		else:
			teamList = [self.poolList[-1].matchList[i].getWinner() for i in range(len(self.poolList[-1].matchList))]
		return teamList
		
	def createNextPoolMatchList(self, pool):
		nOfTeams = len(pool.teamList)
		if nOfTeams < 2 : 
			raise ValueError("Cannot create a match with less than 2 teams!")
		for i in range(nOfTeams/2):
			nextWorstTeam = nOfTeams-1-i
			nextBestTeam = i
			pool.createMatch(nextWorstTeam, nextBestTeam, 'Match_'+str(pool.name[-1])+'-'+str(i+1))
	'''

	'''	
	def buildAllPools(self):
		self.buildFirstPool()
		self.buildOtherPools()
		
	def buildFirstPool(self):
		self.inputPool.rename("Pool_1")
		if self.nTeamsIsPowerOf2:
			self.createPoolMatchList(self.inputPool, self.nOfTeams)
			self.addPool(self.inputPool)
		else:
			for i in range(self.nOfAdditionnalFirstPoolMatches):
				nextWorstTeam = self.nOfTeams-1-i
				nextBestTeam = self.nOfFirstPoolByes + i
				self.inputPool.createMatch(nextWorstTeam, nextBestTeam, 'Match_'+str(self.inputPool.name[-1])+'-'+str(i+1))
			#self.createPoolMatchList(LOTS OF ARGUMENTS....) or would need to just create another function for this one time use... not sure if needed
			self.addPool(self.inputPool)

	def buildOtherPools(self):
		if self.nTeamsIsPowerOf2:
			for layerExponent in range(self.nOfLayers-1,0,-1):
				poolNumber = self.nOfLayers-layerExponent+1
				nOfTeams = 2**layerExponent
				tempTeamList = [Team('Winner-Match_'+str(poolNumber-1)+'-'+str(i+1)) for i in range(nOfTeams)]
				tempPool = Pool('Pool_'+str(poolNumber),tempTeamList)
				self.createPoolMatchList(tempPool, nOfTeams)
				self.addPool(tempPool)
		else:
			for layerExponent in range(self.nOfLayers-1,0,-1):
				poolNumber = self.nOfLayers-layerExponent+1
				nOfTeams = 2**layerExponent
				if poolNumber == 2: # First other pool must contain the teams that had a bye if there were any
					tempTeamList = [self.inputPool.teamList[i] for i in range(self.nOfFirstPoolByes)]
					tempTeamList = tempTeamList + [Team('Winner-Match_'+str(poolNumber-1)+'-'+str(i+1)) for i in range(self.nOfAdditionnalTeams)]
				else:
					tempTeamList = [Team('Winner-Match_'+str(poolNumber-1)+'-'+str(i+1)) for i in range(nOfTeams)]
				tempPool = Pool('Pool_'+str(poolNumber), tempTeamList)
				self.createPoolMatchList(tempPool,nOfTeams)
				self.addPool(tempPool)
				
	def createPoolMatchList(self,pool,nOfTeams):
		for i in range(nOfTeams/2):
			nextWorstTeam = nOfTeams-1-i
			nextBestTeam = i
			pool.createMatch(nextWorstTeam, nextBestTeam, 'Match_'+str(pool.name[-1])+'-'+str(i+1))
			
	def calcNumberOfLayers(self, nOfTeams):
		if self.nTeamsIsPowerOf2:
			nOfLayers = log2(nOfTeams)
			return nOfLayers
		else:
			nOfLayers = int(log2(nOfTeams))+1
			return nOfLayers
	'''
	def show(self):
		for pool in self.poolList:
			print '\n'+str(pool.name)+'\n'
			for match in pool.matchList:
				print str(match.name)+' : '+str(match.teamA.name)+' vs '+str(match.teamB.name)+'\n'
	
	# TO BE CONTINUED 
	'''
	def update(self):
		if Pool.isAllMatchPlayed():
			rankedTeamList = pool.Ranking()
			#...
		else:
			pass
			#could display match to play
		print 'NYI'
		# should consult stats and adjust teams
	'''
				
if __name__ == "__main__":
	nOfTeams = int(input("How many teams are in your tournament?"))
	thePool = Pool('inputPool', [Team('Team_'+str(i)) for i in range(1, nOfTeams+1)])
	theTournament = SingleElimination()
	theTournament.setInputPool(thePool)
	#theTournament.buildAllPools()
	theTournament.createPoolList()
	theTournament.show()
