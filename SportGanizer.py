# -*- coding: utf-8 -*-
from numpy import *
import copy

from teamatch import *


class Pool:
	def __init__(self, initName=None, initTeamList=None):
		self.name = initName
		if initTeamList:
			self.nOfTeams = len(initTeamList)
			self._teamList = initTeamList
		else:
			self.nOfTeams = 0
			self._teamList = []
		self.nOfMatches = 0
		self._matchList = []

	def show(self):
		print '\n'+str(self.name)+'\n'
		for match in self._matchList:
			match.show()
	def rename(self, newName):
		self.name = newName

	def addTeam(self, newTeam):
		if isinstance(newTeam, list):
			self.nOfTeams += len(newTeam)
			self._teamList.extend(newTeam)
		else:
			self.nOfTeams += 1
			self._teamList.append(newTeam)
	
	def createMatch(self, teamANumber, teamBNumber, matchName = None):
		self.nOfMatches += 1
		newMatch = Match(self._teamList[teamANumber], self._teamList[teamBNumber], matchName)
		self._matchList.append(newMatch)
	
	def winnerList(self):
		winnerList = []
		for match in self._matchList:
			winnerList.append(match.winner)
		return winnerList

	def loserList(self):
		loserList = []
		for match in self._matchList:
			loserList.append(match.loser)
		return loserList

	def unmatchedList(self):
		unmatchedList = self._teamList
		for match in self._matchList:
			for team in match:
				if team in unmatchedList:
					unmatchedList.remove(team)
		return unmatchedList
	
	def ranking(self):
		sortedTeamList = sorted(self._teamList, reverse = True)
		return sortedTeamList

	### TODO : the ranking function should only consider stats of the pool
	



class Tournament:
	def __init__(self, name = None):
		self.name = name
		self.poolList = []
		self.nOfPools = 0
	@property
	def lastPool(self):
		if self.poolList:
			return self.poolList[-1]
		else:
			return None

	def rename(self,newName):
		self.name = newName
	def show(self):
		for pool in self.poolList:
			pool.show()

	def addPool(self, newPool):
		if isinstance(newPool, list):
			self.nOfPools += len(newPool)
			self.poolList.extend(newPool)
		else:
			self.nOfPools += 1	
			self.poolList.append(newPool)
			

class SingleElimination(Tournament):

	def __init__(self, initPool = None):
		Tournament.__init__(self, 'single elimination')	
		if initPool:
			self.setInputPool(initPool)
		
	### WARNING : side effect of renaming. See _makeEliminationMatch before changing
	### NOTE : we might want to input a Pool with matchs already in it. This would
	  # break our use of Pool.unmatchList() in makeMatchTree. The class should
	  # may be take a team list as input rather than an actual Pool... or a pool input
	  # being copied instead of taken as is and renamed. This is presently unclear
	  # because of our poor specifications definition.
	def setInputPool(self, initPool):
		initPool.rename("Pool_1")
		self.addPool(initPool)
	
	def makeMatchTree(self):				# recursive
		if self.lastPool.nOfTeams == 1:
			self.lastPool.rename('Champion')# stops recursion
		else:
			self._makeEliminationMatches()
			self._makeNextPool()
			self.makeMatchTree()			# recall 
	def _makeEliminationMatches(self):
		# nOfByes could be self.nOfByes with a function self.calcByesAndElims()
		nOfByes = (2**(int(log2(self.lastPool.nOfTeams)+1)))%self.lastPool.nOfTeams
		nOfElim = (self.lastPool.nOfTeams-nOfByes)/2
		for i in range(nOfElim):
			nextBestTeamIndex = nOfByes + i
			nextWorstTeamIndex = self.lastPool.nOfTeams-1-i
			### WARNING : necessitate a pool name ending with a number
			elimName = 'Match '+str(self.lastPool.name.strip('Pool_'))+'-'+str(i+1)
			self.lastPool.createMatch(nextBestTeamIndex, nextWorstTeamIndex ,elimName)
	def _makeNextPool(self):
		nextPool = Pool('Pool_'+str(self.nOfPools+1))
		nextPool.addTeam(self.lastPool.unmatchedList())
		nextPool.addTeam(self.lastPool.winnerList())
		self.addPool(nextPool)



			
if __name__ == "__main__":

	nOfTeams = int(input("How many teams are in your tournament?"))
	#import sys
	#try: nOfTeams = int(sys.argv[0])
	#except: nOfTeams = 47
	
	thePool = Pool('inputPool', [Team('Team_'+str(i)) for i in range(1, nOfTeams+1)])
	theTournament = SingleElimination(thePool)
	theTournament.makeMatchTree()
	theTournament.show()
	