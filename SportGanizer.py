# -*- coding: utf-8 -*-
from numpy import *

class Team:
	def __init__(self, name = None):
		self.name = name 
		self.matchList = []
		self.nextMatchIndex = 0
		self.stats = {'numberOfWins': 0, 'numberOfLosses': 0, 'numberOfTies': 0, 'scoresFor': 0, 'scoresAgainst': 0} #Stats inside each pool the team participates in, resetted after each pool ends.
		self.statsTotal = {'numberOfWins': 0, 'numberOfLosses': 0, 'numberOfTies': 0, 'scoresFor': 0, 'scoresAgainst': 0} #Total stats over every pool, updated after each pool ends.

	def __lt__(self, teamToCompare):
		selfWins = self.stats['numberOfWins']
		compWins = teamToCompare.stats['numberOfWins']
		selfLosses = self.stats['numberOfLosses']
		compLosses = teamToCompare.stats['numberOfLosses']
		selfScoreFor = self.stats['scoresFor']
		compScoreFor = teamToCompare.stats['scoresFor']
		selfScoreAgst = self.stats['scoresAgainst']
		compScoreAgst = teamToCompare.stats['scoresAgainst']
		
		SelfHasLessWins = selfWins < compWins
		EqualWins = selfWins == compWins
		SelfHasMoreLosses = selfLosses > compLosses
		EqualLosses = selfLosses == compLosses
		SelfHasLessScoresFor = selfScoreFor < compScoreFor
		EqualScoresFor = selfScoreFor == compScoreFor
		SelfHasMoreScoresAgainst = selfScoreAgst > compScoreAgst
		
		if SelfHasLessWins:
			return True
		elif EqualWins and SelfHasMoreLosses:
			return True
		elif EqualWins and EqualLosses:
			if SelfHasLessScoresFor:
				return True
			elif EqualScoresFor and SelfHasMoreScoresAgainst:
				return True
		else:
			return False
	
	def _addMatch(self, match):
		self.matchList.append(match)
	
	def _removeMatch(self, match):
		self.matchList.remove(match)
	
	def _increaseNextMatchIndex(self):
		self.nextMatchIndex = self.nextMatchIndex + 1
	
	def _becomes(self, team):
		#Could it ultimately be the "=" operator ?
		#Important for crossovers when a matchList already exist for an undetermined team
		self.matchList.extend(team.matchList)
		self._increaseNextMatchIndex()
	
	def _swap(self, team):
		tempMatchList=self.matchList
		tempName=self.name
		tempNextMatchIndex=self.nextMatchIndex
		self.matchList=team.matchList
		
	def rename(self, name):
		self.name=name
		
	#To implement : team stats, team delete?, __lt__ conditionned on if self has beaten other team in the pool,
	#Functions :  swap(using deepcopy)
	#_becomes : needs to erase future matches (crossovers)


class Match:
	def __init__(self, teamA, teamB, name = None, weight = 0):
		self.name = name
		self.teamA = teamA
		self.teamA._addMatch(self)
		self.teamB = teamB
		self.teamB._addMatch(self)
		self.weight = weight
		self.winner = Team(str(self.name)+"Winner")
		self.loser = Team(str(self.name)+"Loser")
		
	def replaceDummyTeam(self, dummyTeam, newTeam):
		if self.teamA == dummyTeam:
			self.teamA._removeMatch(self)
			self.teamA = newTeam
			self.teamA._addMatch(self)
			self.teamA._increaseNextMatchIndex()
			del dummyTeam
		elif self.teamB == dummyTeam:
			self.teamB._removeMatch(self)
			self.teamB = newTeam
			self.teamB._addMatch(self)
			self.teamB._increaseNextMatchIndex()
			del dummyTeam
		else:
			pass # SHOULD WARN

	def setWinner(self, team):
		if self.winner.matchList == []: #Limit case that might need fixing (end of the tournament?)
			#team.wasLastMatch()        Needs implementation
			self.winner = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ? NOOOOOOOOO! We will need to replaceDummyTeam in the other match that the winner will play by the self.winner.
			self.winner.stats['numberOfWins'] += 1
			#Means the tournament is over!?!? Needs something more.
		else:
			#winnerMatch=self.winner.matchList[0] #Shouldn't it be self.winner.matchList[self.nextMatchIndex-1] ?
			self.winner = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ? NOOOOOOOOO! We will need to replaceDummyTeam in the other match that the winner will play by the self.winner.
			self.winner.stats['numberOfWins'] += 1

	def setResult(self, teamA, teamAscore, teamB, teamBscore):
		if (teamA != self.teamA and teamA != self.teamB):
			teamIsNotInMatch_EXCEPTION(self, teamA)
		elif (teamB != self.teamA and teamB != self.teamB):
			teamIsNotInMatch_EXCEPTION(self, teamB)
		else:
			if teamAscore > teamBscore:
				self.setWinner(teamA)
			elif teamBscore > teamAscore:
				self.setWinner(teamB)
			else:
				pass #If tie, maybe something happens if possible
		
	def teamIsNotInMatch_EXCEPTION(match, team):
		print team.name+" "+"is not in"+" "+match.name
		
		
	#To implement : match result, match location, match time, match versus?, match delete(+ team.removeMatch test)
	# match winner, match loser
	#if match already exists, copy itself to the existing match
	#coding = and == operators of matches
	#Functions : match.setResult(tests) and losers!!
	# match.setVersus?



## Should correct the name for Pool also

class Pool:
	def __init__(self, initName = "defaultPool", initTeamList = []):
		self.name = initName
		self.numberOfTeams = len(initTeamList)
		self.numberOfMatches = 0
		self.teamList = initTeamList
		self.matchList = []
		
	def addTeam(self, newTeam):
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
	
		
class SingleElimination(Tournament):
	''' Must input a pool with method setInputPool before using other functions. '''
	
	# TODO: Finish cleaning buildAllPools in smaller functions buildFirstPool, buildOtherPools
	
	def __init__(self):
		Tournament.__init__(self, 'single elimination')
		
	def setInputPool(self, initPool):
		self.inputPool = initPool
		self.nOfTeams = self.inputPool.numberOfTeams
		self.additionnalTeams = self.nOfTeams%(2**(int(log2(self.nOfTeams))))
		self.nTeamsIsPowerOf2 = (self.additionnalTeams == 0)
		
	def buildAllPools(self):
		nOfLayers = self.calcNumberOfLayers(self.nOfTeams)
		
		if self.nTeamsIsPowerOf2:
			self.buildFirstPool()
			for layer in range(int(nOfLayers)):
				nOfTeams = int(2**(nOfLayers-layer))
				tempTeamList = [Team('dummyTeam'+str(i)) for i in range(nOfTeams)]
				
				tempPool = Pool('pool'+str(layer),tempTeamList)
				for i in range (nOfTeams/2):
					tempPool.createMatch(i,i+nOfTeams/2, 'match_'+str(layer)+'-'+str(i))
				self.addPool(tempPool)
		else:
			self.buildInputPool()
			print 'not implemented for unfitted number of teams, try with 2, 4, 8, 16,...'
		
	def buildFirstPool(self):
		if self.nTeamsIsPowerOf2:
			for i in range (self.nOfTeams/2):
				self.inputPool.createMatch(i,i+self.nOfTeams/2, 'match_0-'+str(i))
				self.addPool(self.inputPool)
		else:
			'not implemented for unfitted number of teams, try with 2, 4, 8, 16,...'
			
	def buildOtherPool(self,nOfTeams):
		pass
		
	def calcNumberOfLayers(self, nOfTeams):
		if self.nTeamsIsPowerOf2:
			nOfLayers = log2(nOfTeams)
			return nOfLayers
		else:
			nOfLayers = int(log2(nOfTeams))+1
			return nOfLayers

	def show(self):
		for pool in self.poolList:
			print '\n'+str(pool.name)+'\n'
			for match in pool.matchList:
				print str(match.name)+' : '+str(match.teamA.name)+' vs '+str(match.teamB.name)+'\n'
	
	# TO BE CONTINUED 
	'''
	def show():
		for pool in poolList:
			
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
		
	# can have a globalRanking and a temporaryRanking
				
if __name__ == "__main__":
	
	thePool = Pool('inputPool', [Team('team1'),Team('team2'),Team('team3'),Team('team4'),Team('team5'),Team('team6'),Team('team7'),Team('team8')])
	theTournament = SingleElimination()
	theTournament.setInputPool(thePool)
	#don't work yet
	theTournament.buildAllPools()
	theTournament.show()
	