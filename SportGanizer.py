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
		selfHasLessWins = self.stats['numberOfWins'] < teamToCompare.stats['numberOfWins']
		equalWins = self.stats['numberOfWins'] == teamToCompare.stats['numberOfWins']
		selfHasMoreLosses = self.stats['numberOfLosses'] > teamToCompare.stats['numberOfLosses']
		equalLosses = self.stats['numberOfLosses'] == teamToCompare.stats['numberOfLosses']
		selfHasLessScoresFor = self.stats['scoresFor'] < teamToCompare.stats['scoresFor']
		equalScoresFor = self.stats['scoresFor'] == teamToCompare.stats['scoresFor']
		selfHasMoreScoresAgainst = self.stats['scoresAgainst'] > teamToCompare.stats['scoresAgainst']
		
		if selfHasLessWins:
			return True
		elif equalWins and selfHasMoreLosses:
			return True
		elif equalWins and equalLosses:
			if selfHasLessScoresFor:
				return True
			elif equalScoresFor and selfHasMoreScoresAgainst:
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
		self.winner = Team(self.name+"Winner")
		self.loser = Team(self.name+"Loser")
		
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



class Pool:
	def __init__(self, initName = "defaultPool", initTeamList = []):
		self.name = initName
		self.numberOfTeams = 0
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


class Tournament:
	def __init__(self):
		self.name = "no-name Tournament"
		self.poolList = []
			
	def rename(self, name):
		self.name = name

	def addPool(self, pool):
		self.poolList.append(pool)
	
		
class SingleElimination(Tournament):
	def __init__(self):
		Tournament.__init__(self)
		self.rename('no-name single elimination')
			
	
	'''
	def buildNextPool(prevPool):
		rankedTeamList = pool.Ranking()
		nextPool = Pool()
		for team in len(rankedTeamList)
			nextPool.addTeam(rankedTeamList[0])
			nextPool.addTeam(rankedTeamList[0])
		self.addPool(nextPool)
	'''	
