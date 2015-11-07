# -*- coding: utf-8 -*-
from numpy import *
import copy

from teamatch import *


class Pool:
	def __init__(self, initName=None, initTeamList=None):
		self.name = initName
		if initTeamList:
			self.nOfTeams = len(initTeamList)
			self.teamList = initTeamList
		else:
			self.nOfTeams = 0
			self.teamList = []
		self.numberOfMatches = 0
		self.matchList = []
	def rename(self,name):
		self.name = name
		
	def addTeam(self, newTeam):
		if isinstance(newTeam, list):
			self.nOfTeams += len(newTeam)
			self.teamList.extend(newTeam)
		else:
			self.nOfTeams += 1
			self.teamList.append(newTeam)
	def createMatch(self, teamANumber, teamBNumber, matchName = None):
		self.numberOfMatches += 1
		self.newMatch = Match(self.teamList[teamANumber], self.teamList[teamBNumber], matchName)
		self.matchList.append(self.newMatch)
		
	def ranking(self):
		sortedTeamList = sorted(self.teamList)
		return sortedTeamList	

	# IMPORTANT: the Pool shall receive the Teams input from the GUI
	# TODO:
		#createTimeSlots(timeList) and assignTimeSlotsToMatches(timeSlots) OR a function that does both at same time, although that seems too large
		#createLocations(locationList) and assignLocationsToMatches(locations) OR a function that does both at same time, although that seems too large




class Tournament:
	def __init__(self, name = None):
		self.name = name
		self.poolList = []
		self.nOfPools = 0
	def rename(self, name):
		self.name = name
	def addPool(self, pool):
		self.poolList.append(pool)
		self.nOfPools += 1
	def removePool(self, pool):
		self.poolList.remove(pool)
	

class SingleElimination(Tournament):
	''' Must input a pool with method setInputPool before using other functions. '''
	def __init__(self, initPool = None):
		Tournament.__init__(self, 'single elimination')	
		if initPool:
			self.inputPool = initPool
			self.inputPool.rename("Pool_1")
			self.addPool(self.inputPool)

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
			self.createMatchsAndNextPool()
			self.createPoolList()

	def createMatchsAndNextPool(self):
		inPool = self.poolList[-1]
		nOfByes = (2**(int(log2(inPool.nOfTeams)+1)))%inPool.nOfTeams
		nOfElim = (inPool.nOfTeams-nOfByes)/2
		
		# make nextPool part 1
		outPool = Pool('Pool_'+str(self.nOfPools+1))
		for i in range(nOfByes):
			outPool.addTeam(inPool.teamList[i])
		# make eliminations
		for i in range(nOfElim):
			nextWorstTeam = inPool.nOfTeams-1-i
			nextBestTeam = nOfByes + i
			elimName = 'Match_'+str(inPool.name[-1])+'-'+str(i+1)
			inPool.createMatch(nextWorstTeam, nextBestTeam, elimName)
			# make nextPool part 2
			outPool.addTeam(inPool.matchList[-1].getWinner())
		# make nextPool part 3
		self.addPool(outPool)
		# TODO: 
			# need to be splitted : self.createMatchs() and pool.passingTeams()
				# however, passing teams needs to be more flexible : pool.passingTeams()
			# should access neither pool.teamList nor pool.nOfTeams... 
				# functions to do : pool.size() pool.match(i) pool.team(i)
				# there may be a way to unify pool.team(i) and pool.ranking()

	def show(self):
		for pool in self.poolList:
			print '\n'+str(pool.name)+'\n'
			for match in pool.matchList:
				print str(match.name)+' : '+str(match.teamA.name)+' vs '+str(match.teamB.name)+'\n'

	# TODO: 
		#updatePool using the GUI
		#add line in buildFirstPool and buildOtherPools assigning time slots and locations to matchs in each pool via pool.assignTimeSlotsToMatches and pool.assignLocationsToMatches


			
if __name__ == "__main__":
	
	nOfTeams = int(input("How many teams are in your tournament?"))
	thePool = Pool('inputPool', [Team('Team_'+str(i)) for i in range(1, nOfTeams+1)])
	theTournament = SingleElimination()
	theTournament.setInputPool(thePool)
	theTournament.createPoolList()
	theTournament.show()
	