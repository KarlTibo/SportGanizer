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
	
	def test_increaseNextMatchIndex(cls):
		cls.teamAlice._increaseNextMatchIndex()
		assert cls.teamAlice.nextMatchIndex == 1
	
	def test_countWins_zero(cls):
		# NOTE : see class TestTeamAndMatch for non-zero case 
		assert cls.teamAlice.countWins() == 0

	def test_countLosses_zero(cls):
		assert cls.teamAlice.countLosses() == 0

	def test_sorted(cls):
		assert sorted([cls.teamAlice,cls.teamBob], reverse = True)[0] == cls.teamAlice
		cls.teamBob.stats['numberOfLosses'] += 1
		assert cls.teamAlice > cls.teamBob
		assert sorted([cls.teamAlice,cls.teamBob], reverse = True)[0] == cls.teamAlice
		cls.teamBob.stats['numberOfLosses'] = 0
		cls.teamAlice.stats['scoresFor'] += 1
		assert cls.teamBob < cls.teamAlice
		assert sorted([cls.teamAlice,cls.teamBob], reverse = True)[0] == cls.teamAlice
		cls.teamAlice.stats['scoresFor'] = 0
		cls.teamAlice.stats['scoresAgainst'] += 1
		assert cls.teamAlice < cls.teamBob
		assert sorted([cls.teamAlice,cls.teamBob], reverse = True)[0] == cls.teamBob
		
		
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
	
	'''
	def test_replaceDummyTeam(cls):
		cls.matchW1W2 = Match(cls.matchAB.winner, cls.matchCD.winner, "Match W1-W2")	
		cls.matchW1W2.replaceDummyTeam(cls.matchAB.winner, cls.teamAlice)
		assert cls.matchW1W2.teamA == cls.teamAlice
		assert cls.teamAlice.matchList[1] == cls.matchW1W2
		cls.matchW1W2.replaceDummyTeam(cls.matchCD.winner, cls.teamCharlie)
		assert cls.matchW1W2.teamB == cls.teamCharlie
		assert cls.matchW1W2.teamB.nextMatchIndex == 1
	
	def test_setWinner(cls):
		cls.matchCD._setWinner(cls.teamCharlie)
		cls.matchW1W2 = Match(cls.matchAB.winner, cls.matchCD.winner, "Match W1-W2",)
		assert cls.matchCD.winner == cls.teamCharlie
		assert cls.matchW1W2.teamB == cls.teamCharlie
		cls.matchAB._setWinner(cls.teamAlice)
		cls.matchW1W2._setWinner(cls.teamCharlie)
		assert cls.matchAB.winner == cls.teamAlice
		assert cls.matchW1W2.winner == cls.teamCharlie

	def test_setLoser(cls):
		cls.matchCD._setLoser(cls.teamCharlie)
		cls.matchL1L2 = Match(cls.matchAB.loser, cls.matchCD.loser, "Match W1-W2",)
		assert cls.matchCD.loser == cls.teamCharlie
		assert cls.matchL1L2.teamB == cls.teamCharlie
		cls.matchAB._setLoser(cls.teamAlice)
		cls.matchL1L2._setLoser(cls.teamCharlie)
		assert cls.matchAB.loser == cls.teamAlice
		assert cls.matchL1L2.loser == cls.teamCharlie
	'''

	"""
	##Test setResult
	matchW1W2 = Match("Match W1-W2", matchAB.winner, matchCD.winner)
	#matchCD.setResult(teamCharlie)
	
	#Tests on class Team and Match
	teamAlice = Team("Alice")
	teamBob = Team("Bob")
	matchAB = Match("MatchAB", teamAlice, teamBob)
	teamAlice._becomes(teamBob)
	assert len(teamAlice.matchList) == 2
	assert teamAlice.matchList[1] == matchAB
	assert teamAlice.nextMatchIndex == 1
	"""


class TestTeamAndMatch:

	def setup_method(cls,method):
		cls.teamAlice = Team("Alice")
		cls.teamBob = Team("Bob")
		cls.teamCharlie = Team("Charlie")
		cls.teamDave = Team("Dave")
		cls.matchAB = Match(cls.teamAlice,cls.teamBob)
		cls.matchAC = Match(cls.teamAlice,cls.teamCharlie)
		cls.matchAD = Match(cls.teamAlice,cls.teamDave)

	def teardown_method(cls,method):
		del cls.teamAlice 
		del cls.teamBob
		del cls.teamCharlie
		del cls.teamDave
		del cls.matchAB
		del cls.matchAC
		del cls.matchAD

	def test_Team_countWins_non_zero(cls):
		cls.matchAB.winner = cls.teamAlice
		cls.matchAC.winner = cls.teamAlice
		cls.matchAD.winner = cls.teamDave
		assert cls.teamAlice.countWins() == 2
		assert cls.teamBob.countWins() == 0
		assert cls.teamDave.countWins() == 1

	def test_Team_countLosses_non_zero(cls):
		cls.matchAB.loser = cls.teamBob
		cls.matchAC.loser = cls.teamAlice
		cls.matchAD.loser = cls.teamAlice
		assert cls.teamBob.countLosses() == 1
		assert cls.teamAlice.countLosses() == 2

	
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
		
		

