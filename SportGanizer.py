# -*- coding: utf-8 -*-
from numpy import *
import copy

from teamatch import *


class Pool(object):
	def __init__(self, initName=None, initTeamList=None):
		self.name = initName
		if initTeamList:
			self.nOfTeams = len(initTeamList)
			self.teamList = initTeamList
		else:
			self.nOfTeams = 0
			self.teamList = []
		self.nOfMatches = 0
		self.matchList = []

	def show(self):
		print '\n'+str(self.name)+'\n'
		for match in self.matchList:
			match.show()
		if self.matchList == []:
			print str(self.teamList[0].name)
			print '\n\n'
	def rename(self, newName):
		self.name = newName

	def addTeam(self, newTeam):
		if isinstance(newTeam, list):
			self.nOfTeams += len(newTeam)
			self.teamList.extend(newTeam)
		else:
			self.nOfTeams += 1
			self.teamList.append(newTeam)
	
	def createMatch(self, teamANumber, teamBNumber, matchName = None):
		self.nOfMatches += 1
		newMatch = Match(self.teamList[teamANumber], self.teamList[teamBNumber], matchName)
		self.matchList.append(newMatch)
	
	def winnerList(self):
		winnerList = []
		for match in self.matchList:
			winnerList.append(match.winner)
		return winnerList

	def loserList(self):
		loserList = []
		for match in self.matchList:
			loserList.append(match.loser)
		return loserList

	def unmatchedList(self):
		unmatchedList = self.teamList
		for match in self.matchList:
			for team in match:
				if team in unmatchedList:
					unmatchedList.remove(team)
		return unmatchedList
	
	def ranking(self):
		sortedTeamListCopy = []
		for team in self.teamList:
			sortedTeamListCopy.append(team.createDummyTeamForPool(self))
		sortedTeamListCopy = sorted(sortedTeamListCopy, reverse = True)
		sortedTeamList = []
		for teamCopy in sortedTeamListCopy:
			for team in self.teamList:
				if teamCopy.name == team.name:
					sortedTeamList.append(team)
		return sortedTeamList
	### TODO : the ranking function should only consider stats of the pool
	



class Tournament(object):
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
		print '\n'+str(self.name)+'\n'
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
	'''
	Takes a pre-ranked team list as input. If no team list is inputted at creation, make sure to use function "makeInputPool" before using "makeMatchTree".
	'''
	
	def __init__(self, initTeamList = None):
		Tournament.__init__(self, 'Single elimination')	
		if initTeamList:
			self.makeInputPool(initTeamList)
		
	def makeInputPool(self, initTeamList):
		self.addPool(Pool('Pool_1',initTeamList))
		
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
			elimName = str(self.name[0])+' match '+str(self.lastPool.name.strip('Pool_'))+'-'+str(i+1)
			self.lastPool.createMatch(nextBestTeamIndex, nextWorstTeamIndex ,elimName)

	def _makeNextPool(self):
		nextPool = Pool('Pool_'+str(self.nOfPools+1))
		nextPool.addTeam(self.lastPool.unmatchedList())
		nextPool.addTeam(self.lastPool.winnerList())
		self.addPool(nextPool)

class LoserBracket(SingleElimination):
	## TODO : Be sure it is not possible to change the "if" in __init__
	## TODO : The matches are not exactly as they should be. There is too many possibilities of replaying the same team (look at the difference on "Challonge".
	## TODO : Reimplement the "if" in _makeNextPool.
	def __init__(self, winnerBracket):
		self.winnerBracket = winnerBracket
		self.nOfTeamsInTournament = winnerBracket.poolList[0].nOfTeams
		if self.nOfTeamsInTournament > 2:
			Tournament.__init__(self, 'Loser Bracket')	
			self._makeInputPool()
		else:
			raise ValueError("Double Elimination not needed.")
		self.loserAddIndex = 2

	def _makeInputPool(self):
		firstTeamList = self.winnerBracket.poolList[1].loserList() + self.winnerBracket.poolList[0].loserList()[::-1]
		self.addPool(Pool('Pool_1',firstTeamList))

	def _makeNextPool(self):
		nextPool = Pool('Pool_'+str(self.nOfPools+1))
		if (self.nOfPools > 1 and len(self.lastPool.unmatchedList()) == 0) or (self.nOfTeamsInTournament > 4 and self.nOfPools == 1 and 2**len(self.lastPool.unmatchedList()) < self.nOfTeamsInTournament):
			nextPool.addTeam(self.winnerBracket.poolList[self.loserAddIndex].loserList())
			self.loserAddIndex += 1
		nextPool.addTeam(self.lastPool.unmatchedList())
		nextPool.addTeam(self.lastPool.winnerList())
		self.addPool(nextPool)

class DoubleElimination():
	'''
	Takes a pre-ranked team list as input. If no team list is inputted at creation, make sure to use function "makeInputPool" before using "makeMatchTree".
	'''
	## TODO : Implement the 2nd match of the final bracket if the winner loses.
	## TODO : Make sure this is the best implementation possible.
	def __init__(self, initTeamList = None):
		if initTeamList:
			self.winnerBracket = SingleElimination(initTeamList)
		else:
			self.winnerBracket = SingleElimination()
		
		self.winnerBracket.rename("Winner Bracket")
		self.finalBracket = SingleElimination()
		self.finalBracket.rename("Finals Bracket")
		
	def makeInputPool(self, initTeamList):
		self.winnerBracket.makeInputPool(initTeamList)
	
	def makeMatchTree(self):
		#iterate winner bracket
		self.winnerBracket.makeMatchTree()
		#iterate loser bracket
		self.loserBracket = LoserBracket(self.winnerBracket)
		self.loserBracket.rename("Loser Bracket")
		self.loserBracket.makeMatchTree()
		#create finals bracket
		self.finalTeamList = [self.winnerBracket.lastPool.teamList[0],self.loserBracket.lastPool.teamList[0]]
		self.finalBracket.makeInputPool(self.finalTeamList)
		self.finalBracket.makeMatchTree()
		
	def show(self):
		print
		self.winnerBracket.show()
		self.loserBracket.show()
		self.finalBracket.show()
		



if __name__ == "__main__":

	nOfTeams = int(input("How many teams are in your tournament?"))
		
	theTeamList = [Team('Team_'+str(i)) for i in range(1, nOfTeams+1)]
	typeOfTournament = str(input("What type of tournament do you want? \n Input 'SE' for Single Elimination or 'DE' for Double Elimination."))
	if typeOfTournament == "SE":
		theTournament = SingleElimination(theTeamList)
	elif typeOfTournament == "DE":
		theTournament = DoubleElimination(theTeamList)
	else:
		raise ValueError("You have not entered a correct input. Please retry.")
		
	theTournament.makeMatchTree()
	theTournament.show()
	