# -*- coding: utf-8 -*-




class Team(object):
	def __init__(self, name = None):
		self.name = name 
		self._matchList = []
	
	def _addMatch(self, match):
		self._matchList.append(match)
	def _takingPlaceOf(self, team):
		for match in team._matchList:
			match._replace(self,team)
			self._addMatch(match)
		team._matchList = []
		return self
	
	def _countScoresFor(self):
		nOfScoreFor = 0
		for match in self._matchList:
			nOfScoreFor += match._getScore(self)
		return nOfScoreFor
	def _countScoresAgainst(self):
		nOfScoreAgainst = 0
		for match in self._matchList:
			nOfScoreAgainst += match._getScoreAgainst(self)
		return nOfScoreAgainst
	def _countWins(self):
		nOfWins = 0
		for match in self._matchList:
			if match.winner == self: 
				nOfWins += 1
		return nOfWins
	def _countLosses(self):
		nOfLosses = 0
		for match in self._matchList:
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




class Match(object):
	@property
	def winner(self):
		return self._winner
	@winner.setter
	def winner(self, input):
		raise ValueError('cannot set winner directly. Instead, use _setWinner to replace actual Team instance _winner in all its matchs')

	@property
	def loser(self):
		return self._loser
	@loser.setter
	def loser(self, input):
		raise ValueError('cannot set loser directly. Instead, use _setLoser to replace actual Team instance _loser in all its matchs')

	def __init__(self, teamA, teamB, name = None):
		self.name = name

		self._teamA = teamA
		self._teamA._addMatch(self)
		self._teamB = teamB
		self._teamB._addMatch(self)
		self._scoreA = 0
		self._scoreB = 0
		self._winner = Team(str(self.name)+'-winner')
		self._loser = Team(str(self.name)+'-loser')

		self.ended = False
		self.isTied = False


	def __contains__(self,team):
		return team in [self._teamA,self._teamB]

	def __iter__(self):
		for team in [self._teamA,self._teamB]:
			yield team

	def _replace(self, firstTeam, secondTeam):
		if self._teamA == firstTeam: 
			self._teamA = secondTeam
		elif self._teamB == firstTeam: 
			self._teamB = secondTeam
		elif self._teamA == secondTeam: 
			self._teamA = firstTeam
		elif self._teamB == secondTeam: 
			self._teamB = firstTeam
		else:
			raise ValueError("neither "+str(firstTeam.name)+" nor "+str(firstTeam.name)+" found")
	def _setWinner(self, team):
		self._winner = team._takingPlaceOf(self.winner)
	def _setLoser(self, team):
		self._loser = team._takingPlaceOf(self.loser)
	def _getScore(self, team):
		if team == self._teamA:
			return self._scoreA
		elif team == self._teamB:
			return self._scoreB
		else:
			raise ValueError("team "+str(team.name)+" not found")
	def _getScoreAgainst(self, team):
		if team == self._teamA:
			return self._scoreB
		elif team == self._teamB:
			return self._scoreA
		else:
			raise ValueError("team "+str(team.name)+" not found")	

	def setScore(self, team, score, secondTeam = None, secondScore = None):
		assert not self.ended
		if secondTeam == None and secondScore == None:
			if team == self._teamA:
				self._scoreA = score
			elif team == self._teamB:
				self._scoreB = score
			else:
				raise ValueError("team "+str(team.name)+" not found") 
		else:
			self.setScore(team,score)
			self.setScore(secondTeam,secondScore)
	def endMatch(self, team = None, score = None, secondTeam = None, secondScore = None):
		assert not self.ended
		if not (team==None and score==None and secondTeam==None and secondScore==None):
			self.setScore(team, score, secondTeam, secondScore)
		if self._scoreA > self._scoreB:
			self._setWinner(self._teamA)
			self._setLoser(self._teamB)
		elif self._scoreA < self._scoreB:
			self._setWinner(self._teamB)
			self._setLoser(self._teamA)
		else:
			self.isTied = True
			raise ValueError("No tie allowed for now")
		self.ended = True
	def show(self):
		print str(self.name)+' : '+str(self._teamA.name)+' vs '+str(self._teamB.name)+'\n'

	# To implement : match location, match time, match versus?, match delete(+ team.removeMatch test)
	# if match already exists, copy itself to the existing match?	