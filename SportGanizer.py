# -*- coding: utf-8 -*-
from numpy import *

class Team:
	def __init__(self, name = None):
		self.name = name 
		self.matchList = []
	
	def isDummy(self):
		return ((self.name == None) and (self.matchList == []))
	def rename(self, name):
		self.name = name
	def addMatch(self, match):
		self.matchList.append(match)
	def removeMatch(self, match):
		self.matchList.remove(match)
	
	def replacedInMatchsOf(self, team):
		self.matchList.extend(team.matchList)
		for match in team.matchList:
			if match.teamA == team:
				match.teamA = self
			elif match.teamB == team:
				match.teamB = self
		return self
	
	def countWins(self):
		nOfWins = 0
		for match in self.matchList:
			if match.winner == self: 
				nOfWins += 1
		return nOfWins
	def countLosses(self):
		nOfLosses = 0
		for match in self.matchList:
			if match.loser == self: 
				nOfLosses += 1
		return nOfLosses
	def countScoresFor(self):
		nOfScoreFor = 0
		for match in self.matchList:
			if match.teamA == self:
				nOfScoreFor += match.scoreA
			else :
				nOfScoreFor += match.scoreB
		return nOfScoreFor
	def countScoresAgainst(self):
		nOfScoreAgainst = 0
		for match in self.matchList:
			if match.teamA == self:
				nOfScoreAgainst += match.scoreB
			else :
				nOfScoreAgainst += match.scoreA
		return nOfScoreAgainst

	def __lt__(self, team):
		if self.countWins() == team.countWins():
			if self.countLosses() == team.countLosses():
				if self.countScoresFor() == team.countScoresFor():
					return self.countScoresAgainst() > self.countScoresAgainst() 
				else: return self.countScoresFor() < team.countScoresFor()
			else : return self.countLosses() > team.countLosses()
		else: return self.countWins() < team.countWins()

	#To implement : team delete?, __lt__ conditionned on selected pool,

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
		self.winner = Team()
		self.loser = Team()

	### WHY GOD WHY???
	'''
	def select(self,team):
		if self.teamA == team:
			return self.teamA
		elif self.teamB == team:
			return self.teamB
		else: print "\tWARNING : setScore input team "+str(team.name)+" was not one of match actual teams "+str(self.teamA.name)+" and "+str(self.teamB.name)

	def scoreOf(self,team):
		if self.teamA == team:
			return self.scoreA
		elif self.teamB == team:
			return self.scoreB
		else: print "\tWARNING : setScore input team "+str(team.name)+" was not one of match actual teams "+str(self.teamA.name)+" and "+str(self.teamB.name)

	def setScore(self, team, score, secondTeam = None, secondScore = None):
		assert not self.ended
		if secondTeam == None and secondScore == None:
			self.scoreOf(team) = score
		else:
			self.setScore(team,score)
			self.setScore(secondTeam,secondScore)
	'''
	### It would be so beautiful !!

	def setScore(self, team, score, secondTeam = None, secondScore = None):
		assert not self.ended
		if secondTeam == None and secondScore == None:
			if team == self.teamA:
				self.scoreA = score
			elif team == self.teamB:
				self.scoreB = score
			else: # TODO : decide what happens then...
				print "\tWARNING : setScore input team "+str(team.name)+" was not one of match actual teams "+str(self.teamA.name)+" and "+str(self.teamB.name)
		else:
			self.setScore(team,score)
			self.setScore(secondTeam,secondScore)

	# NOTE : we could choose to also set score when ending match, just add arguments and call setScore() 
	def endMatch(self):
		assert not self.ended
		if self.scoreA == self.scoreB:
			self.tie = True
			print "WARNING : no behaviour decided for a tie" # TODO : who wins? who loses?
		elif self.scoreA > self.scoreB:
			self.winner = self.teamA.replacedInMatchsOf(self.winner)
			self.loser = self.teamB.replacedInMatchsOf(self.loser)
		elif self.scoreA < self.scoreB:
			self.winner = self.teamB.replacedInMatchsOf(self.winner)
			self.loser = self.teamA.replacedInMatchsOf(self.loser)
		self.ended = True
	

	# To implement : match location, match time, match versus?, match delete(+ team.removeMatch test)
	# if match already exists, copy itself to the existing match?






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
	