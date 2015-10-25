from SportGanizer import *
#import unittest
import pytest

class TestTeam:
	#Tests on class Team in to_be_named.py
	
	def setup_class(cls):
		cls.teamAlice = Team("Alice")
	
	def teardown_class(cls):
		del cls.teamAlice
	
	def test_team_initialization(cls):
		assert (cls.teamAlice.name != "defaultTeam")
		assert (cls.teamAlice.name == "Alice")
		assert (cls.teamAlice.matchList == [])
	
	def test_increaseNextMatchIndex(cls):
		cls.teamAlice._increaseNextMatchIndex()
		assert (cls.teamAlice.nextMatchIndex == 1)

class TestMatch:
	#Tests on class Match
	
	def setup_class(cls):
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob")
		cls.matchAB = Match("MatchAB", cls.teamAlice, cls.teamBob)	
		cls.teamC = Team("C")
		cls.teamD = Team("D")
		cls.matchCD = Match("MatchCD", cls.teamC, cls.teamD)
		
	def teardown_class(cls):
		del cls.teamAlice
		del cls.teamBob
		del cls.matchAB
	
	def test_match_initialization(cls):
		assert (cls.matchAB.name != "defaultMatch")
		assert (cls.matchAB.name == "MatchAB")
		assert (cls.matchAB.teamA.name == "Alice")
		assert (cls.matchAB.teamB.name == "Bob")
		assert (cls.matchAB.weight == 0)
		assert (cls.teamAlice.matchList.count(cls.matchAB) == 1)
		assert (cls.teamBob.matchList.count(cls.matchAB) == 1)
		assert (cls.matchAB.teamA.matchList.count(cls.matchAB) == 1)
		assert (cls.matchAB.teamB.matchList.count(cls.matchAB) == 1)
		assert  cls.teamAlice.matchList[0] == cls.matchAB
		assert  cls.teamBob.matchList[0] == cls.matchAB
	
	def test_replaceDummyTeam(cls):
		cls.matchW1W2 = Match("Match W1-W2", cls.matchAB.winner, cls.matchCD.winner)	
		cls.matchW1W2.replaceDummyTeam(cls.matchAB.winner, cls.teamAlice)
		assert cls.matchW1W2.teamA == cls.teamAlice
		assert cls.teamAlice.matchList[1] == cls.matchW1W2
		cls.matchW1W2.replaceDummyTeam(cls.matchCD.winner, cls.teamC)
		assert cls.matchW1W2.teamB == cls.teamC
		assert cls.matchW1W2.teamB.nextMatchIndex == 1
	
	def test_setWinner(cls):
		cls.matchW1W2 = Match("Match W1-W2", cls.matchAB.winner, cls.matchCD.winner)
		cls.matchCD.setWinner(cls.teamC)
		assert cls.matchCD.winner == cls.teamC
		assert cls.matchW1W2.teamB == cls.teamC
		cls.matchAB.setWinner(cls.teamAlice)
		cls.matchW1W2.setWinner(cls.teamC)
		assert cls.matchAB.winner == cls.teamAlice
		assert cls.matchW1W2.winner == cls.teamC
	
	
	
	"""
	##Test setResult
	matchW1W2 = Match("Match W1-W2", matchAB.winner, matchCD.winner)
	#matchCD.setResult(teamC)
	
	#Tests on class Team and Match
	teamAlice = Team("Alice")
	teamBob = Team("Bob")
	matchAB = Match("MatchAB", teamAlice, teamBob)
	teamAlice._becomes(teamBob)
	assert len(teamAlice.matchList) == 2
	assert teamAlice.matchList[1] == matchAB
	assert teamAlice.nextMatchIndex == 1
	"""
	
class TestPool:
	#Tests on class Pool
	
	def setup_class(cls):
		cls.cls.poolParty = Pool("Party")
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob") 
		cls.matchAB = Match("MatchAB", cls.teamAlice, cls.teamBob)	
	def teardown_class(cls):
	
	def test_pool_initialization(cls):
		assert cls.poolParty.name != "defaultPool"
		assert cls.poolParty.name == "Party"
		assert cls.poolParty.numberOfTeams == 0
		assert cls.poolParty.numberOfMatches == 0
		assert cls.poolParty.teamList == []
		assert cls.poolParty.matchList == []

	def test_addTeam(cls):
		cls.poolParty.addTeam(cls.teamAlice)
		assert cls.poolParty.numberOfTeams == 1
		assert cls.poolParty.teamList.count(cls.teamAlice) == 1
		
	def test_addMatch(cls):
		cls.poolParty.addMatch(cls.matchAB)
		assert cls.poolParty.numberOfMatches == 1
		assert cls.poolParty.matchList.count(cls.matchAB) == 1
		
class TestTournament:
	#Tests on class Tournament
 	
	def setup_class(cls):
		cls.tournamentA = Tournament()
		
	def teardown_class(cls):
		del cls.tournamentA
 	
	def test_match_initialization(cls):
		assert (cls.tournamentA.name == "no-name Tournament")
 	def test_match_rename(cls):
		cls.tournamentA.rename("Ultimate Tournament")
		assert (cls.tournamentA.name == "Ultimate Tournament")
		 
