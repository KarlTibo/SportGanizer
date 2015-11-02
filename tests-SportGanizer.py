from SportGanizer import *
import pytest

#
# TESTS on CLASS TEAM INITIALIZATION (without matchs)

class TestUnnamedTeamInitialization:
	def setup_method(self,method):
		self.team = Team()
	def teardown_method(self,method):
		del self.team

	def test_has_no_name(self):
		assert self.team.name == None
	def test_has_no_matchs(self):
		assert self.team.matchList == []
	def test_is_dummy(self):
		assert self.team.isUnnamedAndHasNoMatch()

	def test_all_dummy_teams_are_not_the_same(self):
		otherTeam = Team()
		assert self.team != otherTeam
	def test_team_is_equal_to_self_only(self):
		assert self.team == self.team

	def test_has_no_wins(self):
		assert self.team.countWins() == 0
	def test_has_no_loss(self):
		assert self.team.countLosses() == 0
	def test_has_no_scoreFor(self):
		assert self.team.countScoresFor() == 0
	def test_has_no_scoreAgainst(self):
		assert self.team.countScoresAgainst() == 0
	def test_is_not_lower_than_self(self):
		assert not self.team < self.team
	def test_can_be_renamed(self):
		self.team.rename('otherTeamName')
		assert self.team.name == 'otherTeamName'


class TestNamedTeamInitialization:
	def setup_method(self,method):
		self.team = Team('teamName')
	def teardown_method(self,method):
		del self.team

	def test_has_name(self):
		assert self.team.name != None
		assert self.team.name == 'teamName'
	def test_has_no_matchs(self):
		assert self.team.matchList == []
	def test_is_not_dummy(self):
		assert not self.team.isUnnamedAndHasNoMatch()

	def test_same_name_teams_are_not_the_same(self):
		otherTeam = Team('teamName')
		assert self.team != otherTeam
	def test_team_is_equal_to_self_only(self):
		assert self.team == self.team

	def test_has_no_wins(self):
		assert self.team.countWins() == 0
	def test_has_no_loss(self):
		assert self.team.countLosses() == 0
	def test_has_no_scoreFor(self):
		assert self.team.countScoresFor() == 0
	def test_has_no_scoreAgainst(self):
		assert self.team.countScoresAgainst() == 0
	def test_is_not_lower_than_self(self):
		assert not self.team < self.team
	def test_can_be_renamed(self):
		self.team.rename('otherTeamName')
		assert self.team.name == 'otherTeamName'


#
# TESTS for CLASS MATCH INITIALIZATION (with basic empty teams)

class TestUnnamedMatchWithBasicTeamsInitialization:
	def setup_method(self,method):
		self.match = Match(Team(),Team())
	def teardown_method(self,method):
		del self.match

	def test_has_no_name(self):
		assert self.match.name == None
	def test_is_not_ended(self):
		assert not self.match.ended
	def test_is_not_tie(self):
		assert not self.match.tie
	def test_score_is_zero_zero(self):
		assert self.match.scoreA == 0
		assert self.match.scoreB == 0
	def test_winner_is_dummy(self):
		assert self.match.winner.isUnnamedAndHasNoMatch()
	def test_loser_is_dummy(self):
		assert self.match.winner.isUnnamedAndHasNoMatch()

	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match.teamA.matchList
	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match.teamB.matchList
	def test_one_can_access_recursively_acess_teams_and_match(self):
		assert self.match.teamA.matchList[0] == self.match
		assert self.match.teamA.matchList[0].teamB == self.match.teamB
		assert self.match.teamA.matchList[0].teamB.matchList[0] == self.match


class TestNamedMatchWithDifferentiableTeamsInitialization:
	def setup_method(self,method):
		self.match = Match(Team('Alice'),Team('Bob'),'matchName')
	def teardown_method(self,method):
		del self.match

	def test_has_no_name(self):
		assert self.match != None
		assert self.match.name == 'matchName'
	def test_is_not_ended(self):
		assert not self.match.ended
	def test_is_not_tie(self):
		assert not self.match.tie
	def test_score_is_zero_zero(self):
		assert self.match.scoreA == 0
		assert self.match.scoreB == 0
	def test_winner_is_dummy(self):
		assert self.match.winner.isUnnamedAndHasNoMatch()
	def test_loser_is_dummy(self):
		assert self.match.winner.isUnnamedAndHasNoMatch()

	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match.teamA.matchList
	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match.teamB.matchList
	def test_one_can_access_recursively_acess_teams_and_match(self):
		assert self.match.teamA.matchList[0] == self.match
		assert self.match.teamA.matchList[0].teamB == self.match.teamB
		assert self.match.teamA.matchList[0].teamB.matchList[0] == self.match		

	def test_team_name_acess(self):
		assert self.match.teamA.name == 'Alice'
		assert self.match.teamB.name == 'Bob'


#
# TESTS on CLASS TEAM (with basic matchs)

class Test_team_takingPlaceOf:
	def setup_method(self,method):
		self.teamAlice = Team('Alice')
		self.teamBob = Team('Bob')
		self.teamCharlie = Team('Charlie')
		self.matchAB = Match(self.teamAlice,self.teamBob,'matchAB')
		self.matchBC = Match(self.teamBob,self.teamCharlie,'matchBC')
		self.matchCB = Match(self.teamCharlie,self.teamBob,'matchCB')
		self.newTeamAlice = self.teamAlice.takingPlaceOf(self.teamCharlie)

	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.matchAB
		del self.matchBC
		del self.matchCB
		del self.newTeamAlice

	def test_newTeamAlice_is_teamAlice(self):
		assert self.newTeamAlice == self.teamAlice
	def test_teamCharlie_matchList_was_emptied(self):
		assert self.teamCharlie.matchList == []
	def test_teamAlice_still_has_its_first_match(self):
		assert self.matchAB in self.teamAlice.matchList
		assert self.matchAB.teamA == self.teamAlice
	def test_matchAB_is_first_in_teamAlice_matchList(self):
		assert self.teamAlice.matchList[0] == self.matchAB
	def test_teamAlice_matchList_contains_teamCharlie_old_matchs(self):
		assert self.matchBC in self.teamAlice.matchList
		assert self.matchCB in self.teamAlice.matchList
	def test_teamAlice_is_in_teamCharlie_old_matchs(self):
		assert self.matchBC.teamB == self.teamAlice
		assert self.matchCB.teamA == self.teamAlice


#
# TESTS on CLASS MATCH (with recognizable teams)

class Test_match_setScore_TWO_args:
	def setup_method(self,method):
		self.teamAlice = Team('Alice')
		self.teamBob = Team('Bob')
		self.matchAB = Match(self.teamAlice,self.teamBob,'matchAB')
		self.matchAB.setScore(self.teamAlice,5)
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.matchAB

	def teams_are_recognized(self):
		assert self.matchAB.teamA == self.teamAlice
		assert self.matchAB.teamB == self.teamBob

	def test_scoreA(self):
		assert self.matchAB.scoreA == 5
	def test_scoreB(self):
		assert self.matchAB.scoreA == 5
	def test_effect_on_teamA(self):
		assert self.teamAlice.countScoresFor() == 5
		assert self.teamAlice.countScoresAgainst() == 0
	def test_effect_on_teamB(self):
		assert self.teamBob.countScoresFor() == 0
		assert self.teamBob.countScoresAgainst() == 5


class Test_match_setScore_FOUR_args:
	def setup_method(self,method):
		self.teamAlice = Team('Alice')
		self.teamBob = Team('Bob')
		self.matchAB = Match(self.teamAlice,self.teamBob,'matchAB')
		self.matchAB.setScore(self.teamBob,3,self.teamAlice,5)
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.matchAB

	def teams_are_recognized(self):
		assert self.matchAB.teamA == self.teamAlice
		assert self.matchAB.teamB == self.teamBob

	def test_scoreA(self):
		assert self.matchAB.scoreA == 5
	def test_scoreB(self):
		assert self.matchAB.scoreB == 3
	def test_effect_on_teamA(self):
		assert self.teamAlice.countScoresFor() == 5
		assert self.teamAlice.countScoresAgainst() == 3
	def test_effect_on_teamB(self):
		assert self.teamBob.countScoresFor() == 3
		assert self.teamBob.countScoresAgainst() == 5


class Test_match_setScore_then_endMatch_with_A_gt_B:
	def setup_method(self,method):
		self.teamAlice = Team('Alice')
		self.teamBob = Team('Bob')
		self.matchAB1 = Match(self.teamAlice,self.teamBob,'matchAB')
		self.matchAB2 = Match(self.teamAlice,self.teamBob,'matchAB')
		self.matchAB1.setScore(self.teamBob,3,self.teamAlice,5)
		self.matchAB2.setScore(self.teamBob,3,self.teamAlice,5)
		self.matchAB1.endMatch()
		self.matchAB2.endMatch()
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.matchAB1
		del self.matchAB2

	def test_winner_was_defined_for_AgtB(self):
		self.matchAB1.winner == self.teamAlice
	def test_loser_was_defined_for_AgtB(self):
		self.matchAB1.loser == self.teamBob
	def test_winner_was_defined_for_AgtB(self):
		self.matchAB2.winner == self.teamBob
	def test_loser_was_defined_for_AgtB(self):
		self.matchAB2.loser == self.teamAlice


#
# TESTS - TEAMS with BASIC MATCH TREE





#
#
#
#
#
#
# OLD TESTS
	
class TestMatch:
	
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob")
		self.teamCharlie = Team("Charlie")
		self.teamDave = Team("Dave")
		self.matchAB = Match(self.teamAlice, self.teamBob,"MatchAB")	
		self.matchCD = Match(self.teamCharlie, self.teamDave,"MatchCD")
		
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.teamCharlie
		del self.teamDave
		del self.matchAB
		del self.matchCD

	def test_endMatch(self):
		self.matchAB.setScore(self.teamAlice,7,self.teamBob,4)
		self.matchAB.endMatch()
		assert self.matchAB.ended
		assert self.matchAB.winner == self.teamAlice
		assert self.matchAB.loser == self.teamBob


class TestTeamAndMatch:

	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob")
		self.teamCharlie = Team("Charlie")
		self.teamDave = Team("Dave")
		self.matchAB = Match(self.teamAlice,self.teamBob)
		self.matchAC = Match(self.teamAlice,self.teamCharlie)
		self.matchAD = Match(self.teamAlice,self.teamDave)
		self.matchCD = Match(self.teamCharlie,self.teamDave)
		self.matchWABvWCD = Match(self.matchAB.winner,self.matchCD.winner)
		self.matchWABvLCD = Match(self.matchAB.winner,self.matchCD.loser)
		self.matchFinal = Match(self.matchWABvWCD.winner,self.matchWABvLCD.winner)

	def teardown_method(self,method):
		del self.teamAlice 
		del self.teamBob
		del self.teamCharlie
		del self.teamDave
		del self.matchAB
		del self.matchAC
		del self.matchAD
		del self.matchCD
		del self.matchWABvWCD
		del self.matchWABvLCD
		del self.matchFinal

	def test_setup(self):
		assert len(self.teamAlice.matchList) == 3
		assert len(self.teamBob.matchList) == 1
		assert len(self.teamCharlie.matchList) == 2
		assert len(self.teamDave.matchList) == 2
		assert self.matchWABvWCD in self.matchAB.winner.matchList
		assert self.matchWABvLCD in self.matchAB.winner.matchList 

	def test_Team_takingPlaceOf(self):
		self.matchAB.winner = self.teamAlice.takingPlaceOf(self.matchAB.winner)
		assert self.matchWABvLCD.teamA == self.matchAB.winner
		assert self.matchAB.winner == self.teamAlice
		assert self.matchAB in self.teamAlice.matchList
		assert self.matchWABvWCD in self.teamAlice.matchList
		assert self.matchWABvLCD in self.teamAlice.matchList
		assert self.matchWABvLCD.teamA == self.teamAlice

	def test_Match_endMatch(self):
		self.matchCD.setScore(self.teamDave,1)
		self.matchCD.endMatch()
		assert self.matchCD.winner == self.teamDave
		assert self.matchWABvWCD in self.teamDave.matchList
		assert self.matchWABvLCD in self.teamCharlie.matchList
		assert self.matchCD.ended
		assert self.matchWABvWCD.teamB == self.teamDave
		assert self.matchWABvLCD.teamB == self.teamCharlie

	def test_Team_countWins_non_zero(self):
		self.matchAB.setScore(self.teamAlice,1)
		self.matchAC.setScore(self.teamAlice,1)
		self.matchAD.setScore(self.teamDave,1)
		self.matchAB.endMatch()
		self.matchAC.endMatch()
		self.matchAD.endMatch()
		assert self.teamAlice.countWins() == 2
		assert self.teamBob.countWins() == 0
		assert self.teamCharlie.countWins() == 0 
		assert self.teamDave.countWins() == 1
	

	def test_Team_countLosses_non_zero(self):
		self.matchAB.setScore(self.teamAlice,1)
		self.matchAC.setScore(self.teamAlice,1)
		self.matchAD.setScore(self.teamDave,1)
		self.matchCD.setScore(self.teamDave,1)
		self.matchAB.endMatch()
		self.matchAC.endMatch()
		self.matchAD.endMatch()
		self.matchCD.endMatch()
		assert self.teamAlice.countLosses() == 1
		assert self.teamBob.countLosses() == 1
		assert self.teamCharlie.countLosses() == 2 
		assert self.teamDave.countLosses() == 0

	def test_Team_countScores(self):
		self.matchAB.setScore(self.teamAlice,2,self.teamBob,1)
		self.matchAC.setScore(self.teamAlice,3)
		self.matchAD.setScore(self.teamDave,6)
		self.matchCD.setScore(self.teamDave,7)
		self.matchAB.endMatch()
		self.matchAC.endMatch()
		self.matchAD.endMatch()
		self.matchCD.endMatch()
		assert self.teamAlice.countScoresFor() == 5
		assert self.teamAlice.countScoresAgainst() == 7
		assert self.teamBob.countScoresAgainst() == 2
		assert self.teamCharlie.countScoresAgainst() == 10 
		assert self.teamDave.countScoresFor() == 13

	def test_sorting_teams(self):
		self.matchAB.setScore(self.teamAlice,2,self.teamBob,1)
		self.matchAB.endMatch()
		self.matchAC.setScore(self.teamAlice,6,self.teamCharlie,4)
		self.matchAC.endMatch()
		self.matchAD.setScore(self.teamAlice,4,self.teamDave,9)
		self.matchAD.endMatch()
		self.matchCD.setScore(self.teamCharlie,5,self.teamDave,2)
		self.matchCD.endMatch()
		# A : 2-1-12-14 , C : 1-2-9-8 , D : 1-1-11-9
		assert self.teamAlice > self.teamCharlie
		assert self.teamCharlie < self.teamAlice
		assert self.teamCharlie < self.teamDave
		assert sorted([self.teamAlice,self.teamBob,self.teamCharlie,self.teamDave], reverse = True) == [self.teamAlice,self.teamDave,self.teamCharlie,self.teamBob]


#
# TEST on CLASS POOL
	
class TestPool:
	#Tests on class Pool
	
	def setup_method(self,method):
		self.poolParty = Pool("Party")
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob") 	
	
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.poolParty

	def test_pool_initialization(self):
		assert self.poolParty.name != "defaultPool"
		assert self.poolParty.name == "Party"
		assert self.poolParty.numberOfTeams == 0
		assert self.poolParty.numberOfMatches == 0
		assert self.poolParty.teamList == []
		assert self.poolParty.matchList == []

	def test_addTeam_and_createMatch(self):
		self.poolParty.addTeam(self.teamAlice)
		assert self.poolParty.numberOfTeams == 1
		assert self.poolParty.teamList.count(self.teamAlice) == 1
		self.poolParty.addTeam(self.teamBob)
		assert self.poolParty.numberOfTeams == 2
		self.poolParty.createMatch(0, 1, "matchTest")
		assert self.poolParty.numberOfMatches == 1
		assert self.poolParty.matchList[0].name == "matchTest"
		assert self.poolParty.teamList[0] == self.teamAlice
		assert self.poolParty.teamList[1] == self.teamBob

	def test_ranking(self):
		assert self.poolParty.ranking() == self.poolParty.teamList



class TestTournament:
	def setup_method(self,method):
		self.tournamentA = Tournament()
		self.poolA = Pool()
		
	def teardown_method(self,method):
		del self.tournamentA
		del self.poolA
 	
	def testTournamentInitialization(self):
		assert (self.tournamentA.name == None)
		assert (self.tournamentA.poolList == [])
		
 	def testInitializationRename(self):
		self.tournamentA.rename("Ultimate Tournament")
		assert (self.tournamentA.name == "Ultimate Tournament")
		
	def testAddingPool(self):
		self.tournamentA.addPool(self.poolA)
		assert (self.tournamentA.poolList == [self.poolA])
		
class TestSingleElimination:
	def setup_class(self):
		self.thePool = Pool('inputPool', [Team('team1'),Team('team2'),Team('team3'),Team('team4'),Team('team5'),Team('team6'),Team('team7'),Team('team8')])
		self.theTournament = SingleElimination()
		self.theTournament.setInputPool(self.thePool)
		
	def teardown_class(self):
		del self.theTournament
		del self.thePool
		
	def testSettingInputPool(self):
		assert (self.theTournament.inputPool == self.thePool)
		
	def testbuildAllPools(self):
		pass
		#self.theTournament.buildAllPools()
		
		#NEED to write all assert	
		
		

