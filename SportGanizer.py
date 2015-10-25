# -*- coding: utf-8 -*-
from numpy import *


###########################################################################################
#Definition of the necessary objects

class Team:
	
	numberOfTeams = 0
	
	def __init__(self, initName = "defaultTeam"):
		self.name = initName 
		self.matchList = []
		self.nextMatchIndex = 0
		Team.numberOfTeams += 1
	
	def __del__(self):
		Team.numberOfTeams -= 1
	
	def _addMatch(self, match):
		self.matchList.append(match)
	
	def _removeMatch(self, match):
		self.matchList.remove(match)
	
	def _increaseNextMatchIndex(self):
		self.nextMatchIndex = self.nextMatchIndex + 1
	
	def _becomes(self, team):
		#Possibly for crossovers
		self.matchList.extend(team.matchList)
		self._increaseNextMatchIndex()
	
	def _swap(self, team):
		tempMatchList=self.matchList
		tempName=self.name
		tempNextMatchIndex=self.nextMatchIndex
		self.matchList=team.matchList
	#To implement : team stats, team delete?
	#Functions :  swap(using deepcopy)
	#_becomes : needs to erase future matches (crossovers)
	

#retest don't understand


class Match:
	def __init__(self, initName = "defaultMatch", initTeamA = Team(), initTeamB = Team(), initWeight = 0):
		self.name = initName
		self.teamA = initTeamA
		self.teamA._addMatch(self)
		self.teamB = initTeamB
		self.teamB._addMatch(self)
		self.weight = initWeight
		self.winner = Team(self.name+"_"+"Winner")
		self.loser = Team(self.name+"_"+"Loser")
		
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
			pass
	
	def setWinner(self, team):
		if self.winner.matchList == []: #Limit case that might need fixing
			#team.wasLastMatch()        Needs implementation
			self.winner = team
			#Means the tournament is over!?!? Needs something more.
		else:
			winnerMatch=self.winner.matchList[0] #Shouldn't it be self.winner.matchList[self.nextMatchIndex-1] ?
			winnerMatch.replaceDummyTeam(self.winner, team) 
			self.winner = team #Why is that line there? Doesn't it destroy the whole point of using replaceDummyTeam ?
	
	def setResult(self, teamA, teamAscore, teamB, teamBscore):
		if (teamA != self.teamA and teamA != self.teamB):
			teamIsNotInMatch_EXCEPTION(self, teamA)
		elif (teamB != self.teamA and teamB != self.teamB):
			teamIsNotInMatch_EXCEPTION(self, teamB)
		else:
			if teamAscore > teamBscore:
				setWinner(teamA)
			elif teamBscore > teamAscore:
				setWinner(teamB)
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
	def __init__(self, initName = "defaultPool"):
		self.name = initName
		
	#To implement : 
	#Functions : cleanPool, singleElimination, doubleElimination, roundRobin, 
	#The last Winner cannot have a next match.

	def singleElimination():
		numberOfMatches = Team.numberOfTeams/2











