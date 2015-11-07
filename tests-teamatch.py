from teamatch import *
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
		assert self.team._matchList == []

	def test_all_dummy_teams_are_not_the_same(self):
		otherTeam = Team()
		assert self.team != otherTeam
	def test_team_is_equal_to_self_only(self):
		assert self.team == self.team

	def test_has_no_wins(self):
		assert self.team._countWins() == 0
	def test_has_no_loss(self):
		assert self.team._countLosses() == 0
	def test_has_no_scoreFor(self):
		assert self.team._countScoresFor() == 0
	def test_has_no_scoreAgainst(self):
		assert self.team._countScoresAgainst() == 0
	def test_is_not_lower_than_self(self):
		assert not self.team < self.team
	def test_can_be_renamed(self):
		self.team.name = 'otherTeamName'
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
		assert self.team._matchList == []

	def test_same_name_teams_are_not_the_same(self):
		otherTeam = Team('teamName')
		assert self.team != otherTeam
	def test_team_is_equal_to_self_only(self):
		assert self.team == self.team

	def test_has_no_wins(self):
		assert self.team._countWins() == 0
	def test_has_no_loss(self):
		assert self.team._countLosses() == 0
	def test_has_no_scoreFor(self):
		assert self.team._countScoresFor() == 0
	def test_has_no_scoreAgainst(self):
		assert self.team._countScoresAgainst() == 0
	def test_is_not_lower_than_self(self):
		assert not self.team < self.team
	def test_can_be_renamed(self):
		self.team.name = 'otherTeamName'
		assert self.team.name == 'otherTeamName'


#
# TESTS for CLASS MATCH INITIALIZATION (implicitely testing Match.addMatch)

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
		assert not self.match.isTied
	def test_score_is_zero_zero(self):
		assert self.match._scoreA == 0
		assert self.match._scoreB == 0

	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match._teamA._matchList
	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match._teamB._matchList
	def test_one_can_access_recursively_acess_teams_and_match(self):
		assert self.match._teamA._matchList[0] == self.match
		assert self.match._teamA._matchList[0]._teamB == self.match._teamB
		assert self.match._teamA._matchList[0]._teamB._matchList[0] == self.match


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
		assert not self.match.isTied
	def test_score_is_zero_zero(self):
		assert self.match._scoreA == 0
		assert self.match._scoreB == 0

	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match._teamA._matchList
	def test_match_is_in_teamA_matchList(self):
		assert self.match in self.match._teamB._matchList
	def test_one_can_access_recursively_acess_teams_and_match(self):
		assert self.match._teamA._matchList[0] == self.match
		assert self.match._teamA._matchList[0]._teamB == self.match._teamB
		assert self.match._teamA._matchList[0]._teamB._matchList[0] == self.match		

	def test_team_name_acess(self):
		assert self.match._teamA.name == 'Alice'
		assert self.match._teamB.name == 'Bob'

class Test_match_with_recognizable_Teams:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB

	def teams_are_recognized(self):
		assert self.matchAB._teamA == self._teamAlice
		assert self.matchAB._teamB == self._teamBob

class Test_match_replace:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.teamCharlie = Team('Charlie')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB1')
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.teamCharlie
		del self.matchAB

	def test_replace_case1(self):
		self.matchAB._replace(self._teamBob,self.teamCharlie)
		assert self.matchAB._teamB == self.teamCharlie
	def test_replace_case2(self):
		self.matchAB._replace(self._teamAlice,self.teamCharlie)
		assert self.matchAB._teamA == self.teamCharlie
	def test_replace_case3(self):
		self.matchAB._replace(self.teamCharlie,self._teamBob)
		assert self.matchAB._teamB == self.teamCharlie
	def test_replace_case4(self):
		self.matchAB._replace(self.teamCharlie,self._teamAlice)
		assert self.matchAB._teamA == self.teamCharlie
	def test_replace_NameError(self):
		with pytest.raises(ValueError):
		 	self.matchAB._replace(Team(),Team())

class Test_match_getScore_getScoreAgainst:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB._scoreA = 13
		self.matchAB._scoreB = 17
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB

	def test_match_getScore(self):
		assert self.matchAB._getScore(self._teamAlice) == 13
		assert self.matchAB._getScore(self._teamBob) == 17
	def test_match_getScore_NameError(self):
		with pytest.raises(ValueError):
		 	self.matchAB._getScore(Team()) 
	def test_match_getScoreAgainst(self):
		assert self.matchAB._getScoreAgainst(self._teamAlice) == 17
		assert self.matchAB._getScoreAgainst(self._teamBob) == 13
	def test_match_getScore_NameError(self):
		with pytest.raises(ValueError):
		 	self.matchAB._getScoreAgainst(Team()) 
		
class Test_match_getWinner_getLoser:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB._winner = self._teamAlice
		self.matchAB._loser = self._teamBob
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB

	def test_match_getWinner(self):
		assert self.matchAB.winner == self._teamAlice
	def test_match_getLoser(self):
		assert self.matchAB.loser == self._teamBob

class Test_match_setScore_TWO_args:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB.setScore(self._teamAlice,5)
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB

	def test_scoreA(self):
		assert self.matchAB._getScore(self._teamAlice) == 5
	def test_scoreB(self):
		assert self.matchAB._getScore(self._teamBob) == 0

class Test_match_setScore_Error:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB

	def test_scoreA(self):
		with pytest.raises(ValueError):
			self.matchAB.setScore(Team(),5)

class Test_match_setScore_FOUR_args:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB1 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB2 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB1.setScore(self._teamBob,3,self._teamAlice,5)
		self.matchAB2.setScore(self._teamAlice,7,self._teamBob,11)
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB1
		del self.matchAB2

	def test_scoreA(self):
		assert self.matchAB1._scoreA == 5
		assert self.matchAB2._scoreA == 7
	def test_scoreB(self):
		assert self.matchAB1._scoreB == 3
		assert self.matchAB2._scoreB == 11


#
# TESTS on CLASS TEAM - functions necessitating matchs

class Test_team_takingPlaceOf:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.teamCharlie = Team('Charlie')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchBC = Match(self._teamBob,self.teamCharlie,'matchBC')
		self.matchCB = Match(self.teamCharlie,self._teamBob,'matchCB')
		self.newTeamAlice = self._teamAlice._takingPlaceOf(self.teamCharlie)
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB
		del self.matchBC
		del self.matchCB
		del self.newTeamAlice

	def test_newTeamAlice_is_teamAlice(self):
		assert self.newTeamAlice == self._teamAlice
	def test_teamCharlie_matchList_was_emptied(self):
		assert self.teamCharlie._matchList == []
	def test_teamAlice_still_has_its_first_match(self):
		assert self.matchAB in self._teamAlice._matchList
		assert self.matchAB._teamA == self._teamAlice
	def test_matchAB_is_first_in_teamAlice_matchList(self):
		assert self._teamAlice._matchList[0] == self.matchAB
	def test_teamAlice_matchList_contains_teamCharlie_old_matchs(self):
		assert self.matchBC in self._teamAlice._matchList
		assert self.matchCB in self._teamAlice._matchList
	def test_teamAlice_is_in_teamCharlie_old_matchs(self):
		assert self.matchBC._teamB == self._teamAlice
		assert self.matchCB._teamA == self._teamAlice

class Test_team_countScore_countScoreAgainst:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.teamCharlie = Team('Charlie')
		self.matchAB1 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB2 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAC = Match(self._teamAlice,self.teamCharlie,'matchBC')
		self.matchBC = Match(self._teamBob,self.teamCharlie,'matchBC')
		self.matchAB1.setScore(self._teamAlice,3,self._teamBob,5)
		self.matchAB2.setScore(self._teamAlice,7,self._teamBob,11)
		self.matchAC.setScore(self._teamAlice,13,self.teamCharlie,17)
		self.matchBC.setScore(self._teamBob,11,self.teamCharlie,13)
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.teamCharlie
		del self.matchAB1
		del self.matchAB2
		del self.matchAC
		del self.matchBC

	def test_effect_on_teamA(self):
		assert self._teamAlice._countScoresFor() == 23
		assert self._teamAlice._countScoresAgainst() == 33
	def test_effect_on_teamB(self):
		assert self._teamBob._countScoresFor() == 27
		assert self._teamBob._countScoresAgainst() == 23
	def test_effect_on_teamC(self):
		assert self.teamCharlie._countScoresFor() == 30
		assert self.teamCharlie._countScoresAgainst() == 24


#
# TESTS on CLASS MATCH (methods necessitating takingPlaceOf)

class Test_match_setLoser_setWinner:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchBW = Match(self._teamBob,self.matchAB.winner,'matchBW')
		self.matchWL = Match(self.matchAB.winner,self.matchAB.loser,'matchWB')
		self.matchAB._setWinner(self._teamAlice)
		self.matchAB._setLoser(self._teamBob)
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB
		del self.matchBW
		del self.matchWL

	def test_match_setWinner_winner(self):
		assert self.matchAB.winner == self._teamAlice
	def test_match_setWinner_winner_matchList(self):
		assert self.matchAB in self._teamAlice._matchList
		assert self.matchBW in self._teamAlice._matchList
		assert self.matchWL in self._teamAlice._matchList
	def test_match_setLoser_matchs_get_winner(self):
		assert self.matchWL._teamA == self._teamAlice
		assert self.matchBW._teamB == self._teamAlice
	def test_match_setLoser_loser(self):
		assert self.matchAB.loser == self._teamBob
	def test_match_setLoser_loser_matchList(self):
		assert self.matchAB in self._teamBob._matchList
		assert self.matchBW in self._teamBob._matchList
		assert self.matchWL in self._teamBob._matchList
	def test_match_setLoser_matchs_get_loser(self):
		assert self.matchWL._teamB == self._teamBob

class Test_match_endMatch:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB1 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB2 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB1.setScore(self._teamBob,3,self._teamAlice,5)
		self.matchAB2.setScore(self._teamBob,17,self._teamAlice,11)
		self.matchAB1.endMatch()
		self.matchAB2.endMatch()
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB1
		del self.matchAB2

	def test_winner_was_defined_A_beats_B(self):
		self.matchAB1.winner == self._teamAlice
	def test_loser_was_defined_A_beats_B(self):
		self.matchAB1.loser == self._teamBob
	def test_winner_was_defined_B_beats_A(self):
		self.matchAB2.winner == self._teamBob
	def test_loser_was_defined_B_beats_A(self):
		self.matchAB2.loser == self._teamAlice

class Test_match_endMatch_Error:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB = Match(self._teamAlice,self._teamBob,'matchAB')
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB	
	def test_NameError_after_setScore(self):
		self.matchAB.setScore(self._teamBob,11,self._teamAlice,11)
		with pytest.raises(ValueError):
			self.matchAB.endMatch()
	def test_NameError_directly(self):
		with pytest.raises(ValueError):
			self.matchAB.endMatch(self._teamBob,11,self._teamAlice,11)

class Test_match_endMatch_directly:
	def setup_method(self,method):
		self._teamAlice = Team('Alice')
		self._teamBob = Team('Bob')
		self.matchAB1 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB2 = Match(self._teamAlice,self._teamBob,'matchAB')
		self.matchAB1.endMatch(self._teamBob,3,self._teamAlice,5)
		self.matchAB2.endMatch(self._teamAlice,5)
	def teardown_method(self,method):
		del self._teamAlice
		del self._teamBob
		del self.matchAB1
		del self.matchAB2

	def test_winner_was_defined_A_beats_B(self):
		self.matchAB1.winner == self._teamAlice
	def test_loser_was_defined_A_beats_B(self):
		self.matchAB1.loser == self._teamBob
	def test_winner_was_defined_B_beats_A(self):
		self.matchAB2.winner == self._teamBob
	def test_loser_was_defined_B_beats_A(self):
		self.matchAB2.loser == self._teamAlice

class Test_teams_countWins_countLosses_lt_and_sort:
	def setup_method(self,method):
		self._teamAlice = Team("Alice") 		#toset: 2-1-15-11 
		self._teamBob = Team("Bob") 			#toset: 2-1-15-11 #tie
		self.teamCharlie = Team("Charlie") 	#toset: 2-1-15-13 #more sA
		self.teamDave = Team("Dave")		#toset: 2-1-13-11 #less sF
		self.teamElise = Team("Elise")		#toset: 2-2-15-11 #more loss
		self.teamFred = Team("Fred")		#toset: 1-1-15-11 #less wins
		self.teamGreg = Team("Greg")		#play to set only
		Match(self._teamAlice,self._teamBob).endMatch(self._teamAlice,5,self._teamBob,3)
		Match(self._teamAlice,self.teamGreg).endMatch(self._teamAlice,7,self.teamGreg,3)
		Match(self._teamAlice,self._teamBob).endMatch(self._teamAlice,3,self._teamBob,5)
		Match(self._teamBob,self.teamGreg).endMatch(self._teamBob,7,self.teamGreg,3)
		Match(self.teamCharlie,self.teamDave).endMatch(self.teamCharlie,5,self.teamDave,3)
		Match(self.teamCharlie,self.teamGreg).endMatch(self.teamCharlie,7,self.teamGreg,5)
		Match(self.teamCharlie,self.teamDave).endMatch(self.teamCharlie,3,self.teamDave,5)
		Match(self.teamDave,self.teamGreg).endMatch(self.teamDave,5,self.teamGreg,3)
		Match(self.teamElise,self.teamFred).endMatch(self.teamElise,11,self.teamFred,5)
		Match(self.teamElise,self.teamGreg).endMatch(self.teamElise,2,self.teamGreg,0)
		Match(self.teamElise,self.teamGreg).endMatch(self.teamElise,0,self.teamGreg,3)
		Match(self.teamElise,self.teamGreg).endMatch(self.teamElise,2,self.teamGreg,3)
		Match(self.teamFred,self.teamGreg).endMatch(self.teamFred,10,self.teamGreg,0)
		self.lst = [self._teamBob,self.teamDave,self._teamAlice,self.teamCharlie,self.teamFred,self.teamElise]
		self.decLst = [self._teamBob,self._teamAlice,self.teamCharlie,self.teamDave,self.teamElise,self.teamFred]
		self.incLst = [self.teamFred,self.teamElise,self.teamDave,self.teamCharlie,self._teamBob,self._teamAlice]
	def teardown_method(self,method):
		del self._teamAlice 
		del self._teamBob
		del self.teamCharlie
		del self.teamDave
		del self.teamElise
		del self.teamFred
		del self.teamGreg
		
	def test_setup_and_Team_countWins_non_zero(self):
		assert self._teamAlice._countWins() == 2
		assert self._teamBob._countWins() == 2
		assert self.teamCharlie._countWins() == 2
		assert self.teamDave._countWins() == 2
		assert self.teamElise._countWins() == 2
		assert self.teamFred._countWins() == 1
	def test_setup_and_Team_countLosses_non_zero(self):
		assert self._teamAlice._countLosses() == 1
		assert self._teamBob._countLosses() == 1
		assert self.teamCharlie._countLosses() == 1
		assert self.teamDave._countLosses() == 1
		assert self.teamElise._countLosses() == 2
		assert self.teamFred._countLosses() == 1
	def test_setup_ScoresFor(self):
		assert self._teamAlice._countScoresFor() == 15
		assert self._teamBob._countScoresFor() == 15
		assert self.teamCharlie._countScoresFor() == 15
		assert self.teamDave._countScoresFor() == 13
		assert self.teamElise._countScoresFor() == 15
		assert self.teamFred._countScoresFor() == 15
	def test_setup_ScoresAgainst(self):
		assert self._teamAlice._countScoresAgainst() == 11
		assert self._teamBob._countScoresAgainst() == 11
		assert self.teamCharlie._countScoresAgainst() == 13
		assert self.teamDave._countScoresAgainst() == 11
		assert self.teamElise._countScoresAgainst() == 11
		assert self.teamFred._countScoresAgainst() == 11

	def test_lt_exact_Tie(self):
		assert not self._teamBob < self._teamAlice
	def test_rev_lt_exact_Tie(self):
		assert not self._teamAlice < self._teamBob
	def test_lt_when_more_scoreAgainst(self):
		assert self.teamCharlie < self._teamAlice
	def test_not_lt_when_less_scoreAgainst(self):
		assert not self._teamAlice < self.teamCharlie
	def test_lt_when_less_scoreFor(self):
		assert self.teamDave < self._teamAlice
	def test_not_lt_when_more_scoreFor(self):
		assert not self._teamAlice < self.teamDave
	def test_lt_when_more_losses(self):
		assert self.teamElise < self._teamAlice
	def test_not_lt_when_less_losses(self):
		assert not self._teamAlice < self.teamElise
	def test_lt_when_less_wins(self):
		assert self.teamFred < self._teamAlice
	def test_not_lt_when_more_wins(self):
		assert not self._teamAlice < self.teamFred
	
	def test_sorted(self):
		assert sorted(self.lst) == self.incLst
	def test_sorted_rev(self):
		assert sorted(self.lst,reverse=True) == self.decLst
	def test_sort(self):
		self.lst.sort()
		assert self.lst == self.incLst	
	def test_sort_rev(self):
		self.lst.sort(reverse=True)
		assert self.lst == self.decLst

		