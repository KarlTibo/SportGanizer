# -*- coding: utf-8 -*-
from numpy import *

class Team:
	def __init__(self, name = None):
		self.name = name 
		self.matchList = []
		#self.nextMatchIndex = 0
		#self.stats = {'numberOfWins': 0, 'numberOfLosses': 0, 'numberOfTies': 0, 'scoresFor': 0, 'scoresAgainst': 0} #Stats inside each pool the team participates in, resetted after each pool ends.
		#self.statsTotal = {'numberOfWins': 0, 'numberOfLosses': 0, 'numberOfTies': 0, 'scoresFor': 0, 'scoresAgainst': 0} #Total stats over every pool, updated after each pool ends.

	def rename(self, name):
		self.name=name

	def _addMatch(self, match):
		self.matchList.append(match)
	
	def _removeMatch(self, match):
		self.matchList.remove(match)
	
	# NOTE : This guy could be a function that takes advantage of Match.ended
	def _increaseNextMatchIndex(self):
		self.nextMatchIndex = self.nextMatchIndex + 1
	
	# NOTE : untested anyway, probably useless... (think about crossover)
	'''
	def _swap(self, team):
		tempMatchList=self.matchList
		tempName=self.name
		tempNextMatchIndex=self.nextMatchIndex
		self.matchList=team.matchList
	'''

	# WARNING : it is a bit intense to just lose track of team after this acts; OK when team is a dummy object, but otherwise???
	# WARNING : becomes cannot work - a function of team can't reassing one of its arguments (self or team)... damn it!
	def becomes(self, team):
		self = team
	

	# TODO : test this: need EndMatch to work - need becomes to work... major issue
	def countWins(self):
		nOfWins = 0
		for match in self.matchList:
			if match.winner == self :
				nOfWins += 1
			else : pass
		return nOfWins

	# TODO : test this:
	def countLosses(self):
		nOfLosses = 0
		for match in self.matchList:
			if match.loser == self :
				nOfLosses += 1
			else : pass
		return nOfLosses

	# TODO : test this:
	def countScoreFor(self):
		nOfScoreFor = 0
		for match in self.matchList:
			if match.teamA == self:
				nOfScoreFor += match.scoreA
			else :
				nOfScoreFor += match.scoreB

	# TODO : test this:
	def countScoreAgainst(self):
		nOfScoreAgainst = 0
		for match in self.matchList:
			if match.teamA == self:
				nOfScoreFor += match.scoreB
			else :
				nOfScoreFor += match.scoreA



	def __lt__(self, teamToCompare):

		SelfHasLessWins = self.countWins() < teamToCompare.countWins()
		EqualWins = self.countWins() == teamToCompare.countWins()
		SelfHasMoreLosses = self.countLosses() > teamToCompare.countLosses()
		EqualLosses = self.countLosses() == teamToCompare.countLosses()
		
		# TODO : before to create functions countScoresFor() and countScoresAgainst() we need to manage score in class Match
		SelfHasLessScoresFor = False
		EqualScoresFor = False
		SelfHasMoreScoresAgainst = True
		
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


		
	#To implement : team stats, team delete?, __lt__ conditionned on if self has beaten other team in the pool,
	#Functions :  swap(using deepcopy)
	#_becomes : needs to erase future matches (crossovers)


class Match:
	def __init__(self, teamA, teamB, name = None, weight = 0):
		self.name = name
		self.weight = weight

		self.teamA = teamA
		self.teamA._addMatch(self)
		self.teamB = teamB
		self.teamB._addMatch(self)

		self.ended = False
		self.tie = False
		self.scoreA = 0
		self.scoreB = 0
		self.winner = Team()
		self.loser = Team()


	def setScore(self, team, score, secondTeam = None, secondScore = None):
		assert not self.ended
		if team == self.teamA:
			self.scoreA = score
		elif team == self.teamB:
			self.scoreB = score
		else:
			print "\tWARNING : setScore input team "+str(team.name)+" was not one of match actual teams "+str(self.teamA.name)+" and "+str(self.teamB.name)
			# TODO : decide what happens then...
		if secondTeam == None and secondScore == None:
			pass
		elif secondTeam != None and secondScore != None and secondTeam != team:
			self.setScore(secondTeam,secondScore)
		else:
			print "\tWARNING : something is wrong with second team input"
			# TODO : handle exceptions


	# NOTE : we could choose to also set score when ending match, just add arguments and call setScore() 
	def endMatch(self):
		assert not self.ended
		if self.scoreA == self.scoreB:
			self.tie = True
			print "WARNING : no behaviour decided for a tie"
			pass # TODO : who wins? who loses?
		# WARNING : becomes cannot work - a function of team can't reassing one of its arguments (self or team)... damn it!
		elif self.scoreA > self.scoreB:
			self.winner = self.teamA #### WRONG!!!
			self.loser = self.teamB #### WRONG !!!
		else :
			self.winner = self.teamB #### WRONG !!!
			self.loser = self.teamA #### WRONG !!!
		self.ended = True

	'''	
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


	def _setWinner(self, team):
		if self.winner.matchList == []: #Limit case that might need fixing (end of the tournament?)
			#team.wasLastMatch()        Needs implementation
			self.winner = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ? NOOOOOOOOO! We will need to replaceDummyTeam in the other match that the winner will play by the self.winner.
			#Means the tournament is over!?!? Needs something more.
		else:
			#winnerMatch=self.winner.matchList[0] #Shouldn't it be self.winner.matchList[self.nextMatchIndex-1] ?
			self.winner = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ? NOOOOOOOOO! We will need to replaceDummyTeam in the other match that the winner will play by the self.winner.

	def _setLoser(self, team):
		if self.winner.matchList == []: #Limit case that might need fixing (end of the tournament?)
			#team.wasLastMatch()        Needs implementation
			self.loser = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ? NOOOOOOOOO! We will need to replaceDummyTeam in the other match that the winner will play by the self.winner.
			#Means the tournament is over!?!? Needs something more.
		else:
			#winnerMatch=self.winner.matchList[0] #Shouldn't it be self.winner.matchList[self.nextMatchIndex-1] ?
			self.loser = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ? NOOOOOOOOO! We will need to replaceDummyTeam in the other match that the winner will play by the self.winner.


	def setResult(self, teamA, teamAscore, teamB, teamBscore):
		if (teamA != self.teamA and teamA != self.teamB):
			teamIsNotInMatch_EXCEPTION(self, teamA)
		elif (teamB != self.teamA and teamB != self.teamB):
			teamIsNotInMatch_EXCEPTION(self, teamB)
		else:
			if teamAscore > teamBscore:
				self._setWinner(teamA)
			elif teamBscore > teamAscore:
				self._setWinner(teamB)
			else:
				pass #If tie, maybe something happens if possible
		
	def teamIsNotInMatch_EXCEPTION(match, team):
		print team.name+" "+"is not in"+" "+match.name
	'''
		
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
	