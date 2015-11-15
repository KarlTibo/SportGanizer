from SportGanizer import *
import pytest




#
# TEST on class POOL

class TestPool_initialization:
	def setup_method(self,method):
		self.poolParty = Pool()
	def teardown_method(self,method):
		del self.poolParty

	def test_pool_name_is_None(self):
		assert self.poolParty.name == None
	def test_pool_nbOfTeam(self):
		assert self.poolParty.nOfTeams == 0
	def test_pool_nbOfMatchs(self):
		assert self.poolParty.nOfMatches == 0
	def test_pool_teamList(self):
		assert self.poolParty._teamList == []
	def test_pool_matchList(self):
		assert self.poolParty._matchList == []
	def test_pool_renaming(self):
		self.poolParty.rename('Party')
		assert self.poolParty.name == 'Party'


class TestPool_initialization_with_team:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.poolParty = Pool("Party",[self.teamAlice])
	def teardown_method(self,method):
		del self.poolParty

	def test_init_name(self):
		assert self.poolParty.name == 'Party'
	def test_nOfTeams_increased(self):
		assert self.poolParty.nOfTeams == 1
	def test_pool_initialization(self):
		assert self.poolParty._teamList == [self.teamAlice]

class TestPool_addTeam:	
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.poolParty = Pool("Party")
		self.poolParty.addTeam(self.teamAlice)
	def teardown_method(self,method):
		del self.teamAlice
		del self.poolParty

	def test_nOfTeams_increased(self):
		assert self.poolParty.nOfTeams == 1
	def test_team_in_pool(self):
		assert self.teamAlice in self.poolParty._teamList

class TestPool_addTeam_list:
	def setup_method(self,method):
		self.poolParty = Pool("Party")
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob")
		lst = [self.teamAlice,self.teamBob]
		self.poolParty.addTeam(lst)
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.poolParty

	def test_both_team_in_pool(self):
		assert self.poolParty.nOfTeams == 2
		assert self.teamAlice in self.poolParty._teamList
		assert self.teamBob in self.poolParty._teamList
	def test_addTeam_with_list_order(self):
		assert self.poolParty._teamList[0] == self.teamAlice
		assert self.poolParty._teamList[1] == self.teamBob


class TestPool_createMatch:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob")
		self.poolParty = Pool("Party")
		self.poolParty.addTeam(self.teamAlice)
		self.poolParty.addTeam(self.teamBob)
		self.poolParty.createMatch(0, 1, "matchTest")
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.poolParty

	def test_both_team_in_pool(self):
		assert self.poolParty.nOfTeams == 2
		assert self.teamAlice in self.poolParty._teamList
		assert self.teamBob in self.poolParty._teamList
	def test_number_of_match_increased(self):
		assert self.poolParty.nOfMatches == 1
	def test_match_name(self):
		assert self.poolParty._matchList[0].name == "matchTest"
	def test_match_teams(self):
		assert self.poolParty._matchList[0]._teamA == self.teamAlice
		assert self.poolParty._matchList[0]._teamB == self.teamBob


class TestPool_winnerList_loserList_unmatchedList:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob") 	
		self.teamCharlie = Team("Charlie")
		self.teamDave = Team("Dave")
		self.teamElise = Team("Elise")
		self.poolParty = Pool("Party",[self.teamAlice,self.teamBob,self.teamCharlie,self.teamDave,self.teamElise])
		self.poolParty.createMatch(0, 1, "matchAB")
		self.poolParty.createMatch(0, 2, "matchAC")
		self.poolParty.createMatch(1, 2, "matchBC")
		self.externalMatch = Match(self.teamElise,self.teamBob,'outsider')
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.teamCharlie
		del self.teamDave
		del self.teamElise
		del self.poolParty

	def test_winnerList(self):
		assert self.poolParty.winnerList() == [self.poolParty._matchList[i].winner for i in range(3)]
	def test_loserList(self):
		assert self.poolParty.loserList() == [self.poolParty._matchList[i].loser for i in range(3)]
	def test_unmatchedList(self):
		assert self.poolParty.unmatchedList() == [self.teamDave,self.teamElise]
	
class TestPool_winnerList_loserList_unmatchedList_once_matchs_are_played:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob") 	
		self.teamCharlie = Team("Charlie")
		self.teamDave = Team("Dave")
		self.teamElise = Team("Elise")
		self.poolParty = Pool("Party",[self.teamAlice,self.teamBob,self.teamCharlie,self.teamDave,self.teamElise])
		self.poolParty.createMatch(0, 1, "matchAB")
		self.poolParty.createMatch(0, 2, "matchAC")
		self.poolParty.createMatch(1, 2, "matchBC")
		self.externalMatchEB = Match(self.teamElise,self.teamBob,'matchEB')
		# SET Pool A-2-0-12-6 ; B-1-1-9-11 ; C-0-2-8-12 ; D-0-0-0-0 ; E-0-0-0-0
		# BUT out  A-2-0-12-6 ; B-1-2-17-23; C-0-2-8-12 ; D-0-0-0-0 ; E-1-0-12-8
		self.poolParty._matchList[0].endMatch(self.teamAlice,6,self.teamBob,3)
		self.poolParty._matchList[1].endMatch(self.teamAlice,6,self.teamCharlie,3)
		self.poolParty._matchList[2].endMatch(self.teamBob,6,self.teamCharlie,5)
		self.externalMatchEB.endMatch(self.teamElise, 12, self.teamBob, 8)	
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.teamCharlie
		del self.teamDave
		del self.teamElise
		del self.poolParty

	def test_winnerList(self):
		assert self.poolParty.winnerList() == [self.teamAlice,self.teamAlice,self.teamBob]
	def test_loserList(self):
		assert self.poolParty.loserList() == [self.teamBob,self.teamCharlie,self.teamCharlie]
	def test_unmatchedList(self):
		assert self.poolParty.unmatchedList() == [self.teamDave,self.teamElise]
	

	

#
# TESTS on class TOURNAMENT

class TestTournament_empty_initialization:
	def setup_method(self,method):
		self.tournamentA = Tournament()
	def teardown_method(self,method):
		del self.tournamentA
 	
	def test_TournamentInitialization(self):
		assert self.tournamentA.name == None
		assert self.tournamentA.poolList == []
		assert self.tournamentA.nOfPools == 0
	def test_renaming(self):
		self.tournamentA.rename('tournament')
		assert self.tournamentA.name == 'tournament'
	def test_lastPool_property(self):
		self.tournamentA.lastPool == None

class TestTournament_adding_pool:
	def setup_method(self,method):
		self.tournamentA = Tournament()
		self.poolA = Pool('poolA')
		self.tournamentA.addPool(self.poolA)
	def teardown_method(self,method):
		del self.tournamentA
		del self.poolA
 	
	def test_adding_pool_is_there(self):
		assert self.tournamentA.poolList == [self.poolA]
	def test_nOfPools_was_increased(self):
		assert self.tournamentA.nOfPools == 1
	def test_lastPool_property(self):
		self.tournamentA.lastPool == self.poolA

class TestTournament_adding_pool_list:
	def setup_method(self,method):
		self.tournamentA = Tournament()
		self.poolA = Pool('poolA')
		self.poolB = Pool('poolB')
		self.poolC = Pool('poolB')
		self.lst = [self.poolA,self.poolB,self.poolC]
		self.tournamentA.addPool(self.lst)
	def teardown_method(self,method):
		del self.tournamentA
		del self.poolA
		del self.poolB
		del self.poolC

	def test_adding_pool_list(self):
		assert self.tournamentA.poolList == self.lst
	def test_nOfPools_was_increased(self):
		assert self.tournamentA.nOfPools == 3
	def test_lastPool_property(self):
		self.tournamentA.lastPool == self.poolC


#
# TESTS on class SINGLE ELIMINATION

class TestSingleElimination_empty_initialization:
	def setup_method(self,method):
		self.singleElimA = SingleElimination()
	def teardown_method(self,method):
		del self.singleElimA

	def test_name(self):
		assert self.singleElimA.name == "single elimination"

class TestSingleElimination_initialization_with_pool:
	def setup_method(self,method):
		self.poolA = Pool('poolA')
		self.singleElimA = SingleElimination(self.poolA)
	def teardown_method(self,method):
		del self.poolA
		del self.singleElimA

	def test_lastPool_is_poolA(self):
		assert self.singleElimA.lastPool == self.poolA
	def test_lastPool_was_renamed(self):	
		assert self.singleElimA.lastPool.name == 'Pool_1'
	def test_poolA_was_also_renamed(self):
		### PROBLEM? side effect on name
		assert self.poolA.name == 'Pool_1'

class TestSingleElimination_setInputPool:
	def setup_method(self,method):
		self.poolA = Pool('poolA')
		self.singleElimA = SingleElimination()		
		self.singleElimA.setInputPool(self.poolA)
	def teardown_method(self,method):
		del self.poolA
		del self.singleElimA

	def test_lastPool_is_poolA(self):
		assert self.singleElimA.lastPool == self.poolA
	def test_lastPool_was_renamed(self):	
		assert self.singleElimA.lastPool.name == 'Pool_1'
	def test_poolA_was_also_renamed(self):
		### PROBLEM? side effect on name
		assert self.poolA.name == 'Pool_1'

class TestSingleElimination_makeEliminationMatchs(self):
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob") 	
		self.teamCharlie = Team("Charlie")
		self.teamDave = Team("Dave")
		self.teamElise = Team("Elise")
		self.poolParty = Pool("Party",[self.teamAlice,self.teamBob,self.teamCharlie,self.teamDave,self.teamElise])
		self.singleElimA = SingleElimination(self.poolParty)
		self.singleElimA.makeEliminationMatches()
	def setup_method(self,method):
		del self.teamAlice
		del self.teamBob 	
		del self.teamCharlie
		del self.teamDave
		del self.teamElise
		del self.poolParty
		del self.singleElimA
		
	def test_2_matches_created(self):
		assert self.singleElimA.lastPool.nOfMatches == 2
	###
	###	PROBLEM: No way to publicly adress the matches or teams of Pool...
	### function like teamBob.playAgainst(teamAlice) would be nice.
	### similar to pool specific stats. must think of some way to do that.
	def test_matchBE_Bob(self):
		pass
	def test_matchBE_Elise(self):
		pass
	def test_matchCD_Charlie(self):
		pass
	def test_matchCD_Dave(self):
		pass
	def test_Alice_noMatch(self):
		pass
		
























