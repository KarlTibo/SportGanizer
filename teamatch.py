# -*- coding: utf-8 -*-




class Team:
	def __init__(self, name = None):
		self.name = name 
		self.matchList = []
	
	###[ NOTE : this one should definitely be private, because it doesn't handle the match itself
	def _addMatch(self, match):
		self.matchList.append(match)
	###]

	#def isUnnamedAndHasNoMatch(self):
	#	return ((self.name == None) and (self.matchList == []))
	def rename(self, name):
		self.name = name
	
	def _takingPlaceOf(self, team):
		for match in team.matchList:
			match._replace(self,team)
			self._addMatch(match)
		team.matchList = []
		return self
	
	def _countScoresFor(self):
		nOfScoreFor = 0
		for match in self.matchList:
			nOfScoreFor += match._getScore(self)
		return nOfScoreFor
	def _countScoresAgainst(self):
		nOfScoreAgainst = 0
		for match in self.matchList:
			nOfScoreAgainst += match._getScoreAgainst(self)
		return nOfScoreAgainst
	def _countWins(self):
		nOfWins = 0
		for match in self.matchList:
			if match.winner == self: 
				nOfWins += 1
		return nOfWins
	def _countLosses(self):
		nOfLosses = 0
		for match in self.matchList:
			if match.loser == self: 
				nOfLosses += 1
		return nOfLosses
	def __lt__(self, team): # NOTE : __lt__ is not the opposite of __gt__ in the case of an exact tie. 
		if self._countWins() == team._countWins():
			if self._countLosses() == team._countLosses():
				if self._countScoresFor() == team._countScoresFor():
					return self._countScoresAgainst() > team._countScoresAgainst()
				else: return self._countScoresFor() < team._countScoresFor()
			else : return self._countLosses() > team._countLosses()
		else: return self._countWins() < team._countWins()

	#To implement : team delete with incidence on matchs, __lt__ conditionned on selected pool, __cmp__ or __gt__




class Match:
	def __init__(self, teamA, teamB, name = None):
		self.name = name

		self.teamA = teamA
		self.teamA._addMatch(self)
		self.teamB = teamB
		self.teamB._addMatch(self)

		self.ended = False
		self.tie = False
		self.scoreA = 0
		self.scoreB = 0
		self.winner = Team(str(self.name)+'-winner')
		self.loser = Team()

	def _replace(self, firstTeam, secondTeam):
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
	def _setWinner(self, team):
		self.winner = team._takingPlaceOf(self.winner)
	def _setLoser(self, team):
		self.loser = team._takingPlaceOf(self.loser)
	def _getScore(self, team):
		if team == self.teamA:
			return self.scoreA
		elif team == self.teamB:
			return self.scoreB
		else:
			raise ValueError("team "+str(team.name)+" not found")
	def _getScoreAgainst(self, team):
		if team == self.teamA:
			return self.scoreB
		elif team == self.teamB:
			return self.scoreA
		else:
			raise ValueError("team "+str(team.name)+" not found")	
	#def getWinner(self):
	#	return self.winner
	#def getLoser(self):
	#	return self.loser

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
			self._setWinner(self.teamA)
			self._setLoser(self.teamB)
		elif self.scoreA < self.scoreB:
			self._setWinner(self.teamB)
			self._setLoser(self.teamA)
		else:
			self.tie = True
			raise ValueError("No tie allowed")
		self.ended = True
	
	# To implement : match location, match time, match versus?, match delete(+ team.removeMatch test)
	# if match already exists, copy itself to the existing match?	