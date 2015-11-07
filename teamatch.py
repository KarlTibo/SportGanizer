# -*- coding: utf-8 -*-




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