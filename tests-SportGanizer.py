from SportGanizer import *
import pytest

class TestTeam:
	
	def setup_method(cls,method):
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob")
	
	def teardown_method(cls,method):
		del cls.teamAlice
		del cls.teamBob
	
	def test_team_initialization(cls):
		assert cls.teamAlice.name != "defaultTeam"
		assert cls.teamAlice.name == "Alice"
		assert cls.teamAlice.matchList == []

	def test_countWins_zero(cls):
		assert cls.teamAlice.countWins() == 0

	def test_countLosses_zero(cls):
		assert cls.teamAlice.countLosses() == 0

	
class TestMatch:
	
	def setup_method(cls,method):
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob")
		cls.teamCharlie = Team("Charlie")
		cls.teamDave = Team("Dave")
		cls.matchAB = Match(cls.teamAlice, cls.teamBob,"MatchAB")	
		cls.matchCD = Match(cls.teamCharlie, cls.teamDave,"MatchCD")
		
	def teardown_method(cls,method):
		del cls.teamAlice
		del cls.teamBob
		del cls.teamCharlie
		del cls.teamDave
		del cls.matchAB
		del cls.matchCD
	
	def test_match_initialization(cls):
		assert cls.matchAB.name != "defaultMatch"
		assert cls.matchAB.name == "MatchAB"
		assert cls.matchAB.teamA.name == "Alice"
		assert cls.matchAB.teamB.name == "Bob"
		assert cls.matchAB.weight == 0
		assert cls.teamAlice.matchList.count(cls.matchAB) == 1
		assert cls.teamBob.matchList.count(cls.matchAB) == 1
		assert cls.matchAB.teamA.matchList.count(cls.matchAB) == 1
		assert cls.matchAB.teamB.matchList.count(cls.matchAB) == 1
		assert cls.teamAlice.matchList[0] == cls.matchAB
		assert cls.teamBob.matchList[0] == cls.matchAB
	
	def test_setScore(cls):
		cls.matchAB.setScore(cls.teamAlice,5)
		cls.matchAB.setScore(cls.teamBob,2)
		assert cls.matchAB.scoreA == 5
		assert cls.matchAB.scoreB == 2
		cls.matchAB.setScore(cls.teamBob,3,cls.teamAlice,5)
		assert cls.matchAB.scoreA == 5
		assert cls.matchAB.scoreB == 3
		cls.matchAB.setScore(cls.teamCharlie,7)
		cls.matchAB.setScore(cls.teamBob,7,cls.teamDave)
		assert cls.matchAB.scoreB == 7

	def test_endMatch(cls):
		cls.matchAB.setScore(cls.teamAlice,7,cls.teamBob,4)
		cls.matchAB.endMatch()
		assert cls.matchAB.ended
		assert cls.matchAB.winner == cls.teamAlice
		assert cls.matchAB.loser == cls.teamBob


class TestTeamAndMatch:

	def setup_method(cls,method):
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob")
		cls.teamCharlie = Team("Charlie")
		cls.teamDave = Team("Dave")
		cls.matchAB = Match(cls.teamAlice,cls.teamBob)
		cls.matchAC = Match(cls.teamAlice,cls.teamCharlie)
		cls.matchAD = Match(cls.teamAlice,cls.teamDave)
		cls.matchCD = Match(cls.teamCharlie,cls.teamDave)
		cls.matchWABvWCD = Match(cls.matchAB.winner,cls.matchCD.winner)
		cls.matchWABvLCD = Match(cls.matchAB.winner,cls.matchCD.loser)
		cls.matchFinal = Match(cls.matchWABvWCD.winner,cls.matchWABvLCD.winner)

	def teardown_method(cls,method):
		del cls.teamAlice 
		del cls.teamBob
		del cls.teamCharlie
		del cls.teamDave
		del cls.matchAB
		del cls.matchAC
		del cls.matchAD
		del cls.matchCD
		del cls.matchWABvWCD
		del cls.matchWABvLCD
		del cls.matchFinal

	def test_setup(cls):
		assert len(cls.teamAlice.matchList) == 3
		assert len(cls.teamBob.matchList) == 1
		assert len(cls.teamCharlie.matchList) == 2
		assert len(cls.teamDave.matchList) == 2
		assert cls.matchWABvWCD in cls.matchAB.winner.matchList
		assert cls.matchWABvLCD in cls.matchAB.winner.matchList 

	def test_Team_replacedInMatchsOf(cls):
		cls.matchAB.winner = cls.teamAlice.replacedInMatchsOf(cls.matchAB.winner)
		assert cls.matchWABvLCD.teamA == cls.matchAB.winner
		assert cls.matchAB.winner == cls.teamAlice
		assert cls.matchAB in cls.teamAlice.matchList
		assert cls.matchWABvWCD in cls.teamAlice.matchList
		assert cls.matchWABvLCD in cls.teamAlice.matchList
		assert cls.matchWABvLCD.teamA == cls.teamAlice

	def test_Match_endMatch(cls):
		cls.matchCD.setScore(cls.teamDave,1)
		cls.matchCD.endMatch()
		assert cls.matchCD.winner == cls.teamDave
		assert cls.matchWABvWCD in cls.teamDave.matchList
		assert cls.matchWABvLCD in cls.teamCharlie.matchList
		assert cls.matchCD.ended
		assert cls.matchWABvWCD.teamB == cls.teamDave
		assert cls.matchWABvLCD.teamB == cls.teamCharlie

	def test_Team_countWins_non_zero(cls):
		cls.matchAB.setScore(cls.teamAlice,1)
		cls.matchAC.setScore(cls.teamAlice,1)
		cls.matchAD.setScore(cls.teamDave,1)
		cls.matchAB.endMatch()
		cls.matchAC.endMatch()
		cls.matchAD.endMatch()
		assert cls.teamAlice.countWins() == 2
		assert cls.teamBob.countWins() == 0
		assert cls.teamCharlie.countWins() == 0 
		assert cls.teamDave.countWins() == 1
	

	def test_Team_countLosses_non_zero(cls):
		cls.matchAB.setScore(cls.teamAlice,1)
		cls.matchAC.setScore(cls.teamAlice,1)
		cls.matchAD.setScore(cls.teamDave,1)
		cls.matchCD.setScore(cls.teamDave,1)
		cls.matchAB.endMatch()
		cls.matchAC.endMatch()
		cls.matchAD.endMatch()
		cls.matchCD.endMatch()
		assert cls.teamAlice.countLosses() == 1
		assert cls.teamBob.countLosses() == 1
		assert cls.teamCharlie.countLosses() == 2 
		assert cls.teamDave.countLosses() == 0

	def test_Team_countScores(cls):
		cls.matchAB.setScore(cls.teamAlice,2,cls.teamBob,1)
		cls.matchAC.setScore(cls.teamAlice,3)
		cls.matchAD.setScore(cls.teamDave,6)
		cls.matchCD.setScore(cls.teamDave,7)
		cls.matchAB.endMatch()
		cls.matchAC.endMatch()
		cls.matchAD.endMatch()
		cls.matchCD.endMatch()
		assert cls.teamAlice.countScoresFor() == 5
		assert cls.teamAlice.countScoresAgainst() == 7
		assert cls.teamBob.countScoresAgainst() == 2
		assert cls.teamCharlie.countScoresAgainst() == 10 
		assert cls.teamDave.countScoresFor() == 13

	def test_sorting_teams(cls):
		cls.matchAB.setScore(cls.teamAlice,2,cls.teamBob,1)
		cls.matchAB.endMatch()
		cls.matchAC.setScore(cls.teamAlice,6,cls.teamCharlie,4)
		cls.matchAC.endMatch()
		cls.matchAD.setScore(cls.teamAlice,4,cls.teamDave,9)
		cls.matchAD.endMatch()
		cls.matchCD.setScore(cls.teamCharlie,5,cls.teamDave,2)
		cls.matchCD.endMatch()
		# A : 2-1-12-14 , C : 1-2-9-8 , D : 1-1-11-9
		assert cls.teamAlice > cls.teamCharlie
		assert cls.teamCharlie < cls.teamAlice
		assert cls.teamCharlie < cls.teamDave
		assert sorted([cls.teamAlice,cls.teamBob,cls.teamCharlie,cls.teamDave], reverse = True) == [cls.teamAlice,cls.teamDave,cls.teamCharlie,cls.teamBob]
	
	
class TestPool:
	#Tests on class Pool
	
	def setup_method(cls,method):
		cls.poolParty = Pool("Party")
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob") 	
	
	def teardown_method(cls,method):
		del cls.teamAlice
		del cls.teamBob
		del cls.poolParty

	def test_pool_initialization(cls):
		assert cls.poolParty.name != "defaultPool"
		assert cls.poolParty.name == "Party"
		assert cls.poolParty.numberOfTeams == 0
		assert cls.poolParty.numberOfMatches == 0
		assert cls.poolParty.teamList == []
		assert cls.poolParty.matchList == []

	def test_addTeam_and_createMatch(cls):
		cls.poolParty.addTeam(cls.teamAlice)
		assert cls.poolParty.numberOfTeams == 1
		assert cls.poolParty.teamList.count(cls.teamAlice) == 1
		cls.poolParty.addTeam(cls.teamBob)
		assert cls.poolParty.numberOfTeams == 2
		cls.poolParty.createMatch(0, 1, "matchTest")
		assert cls.poolParty.numberOfMatches == 1
		assert cls.poolParty.matchList[0].name == "matchTest"
		assert cls.poolParty.teamList[0] == cls.teamAlice
		assert cls.poolParty.teamList[1] == cls.teamBob

	def test_ranking(cls):
		assert cls.poolParty.ranking() == cls.poolParty.teamList



class TestTournament:
	def setup_method(cls,method):
		cls.tournamentA = Tournament()
		cls.poolA = Pool()
		
	def teardown_method(cls,method):
		del cls.tournamentA
		del cls.poolA
 	
	def testTournamentInitialization(cls):
		assert (cls.tournamentA.name == None)
		assert (cls.tournamentA.poolList == [])
		
 	def testInitializationRename(cls):
		cls.tournamentA.rename("Ultimate Tournament")
		assert (cls.tournamentA.name == "Ultimate Tournament")
		
	def testAddingPool(cls):
		cls.tournamentA.addPool(cls.poolA)
		assert (cls.tournamentA.poolList == [cls.poolA])
		
class TestSingleElimination:
	def setup_class(cls):
		cls.thePool = Pool('inputPool', [Team('team1'),Team('team2'),Team('team3'),Team('team4'),Team('team5'),Team('team6'),Team('team7'),Team('team8')])
		cls.theTournament = SingleElimination()
		cls.theTournament.setInputPool(cls.thePool)
		
	def teardown_class(cls):
		del cls.theTournament
		del cls.thePool
		
	def testSettingInputPool(cls):
		assert (cls.theTournament.inputPool == cls.thePool)
		
	def testbuildAllPools(cls):
		pass
		#cls.theTournament.buildAllPools()
		
		#NEED to write all assert	
		
		

