from SportGanizer import *
import pytest




#
# TEST on POOL initialization

class TestPool_initialization:
	def setup_method(self,method):
		self.poolParty = Pool("Party")
	def teardown_method(self,method):
		del self.poolParty

	def test_pool_name_is_None(self):
		assert self.poolParty.name == "Party"
	def test_pool_nbOfTeam(self):
		assert self.poolParty.nOfTeams == 0
	def test_pool_initialization(self):
		assert self.poolParty.numberOfMatches == 0
	def test_pool_initialization(self):
		assert self.poolParty._teamList == []
	def test_pool_initialization(self):
		assert self.poolParty._matchList == []

class TestPool_initialization_with_team:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.poolParty = Pool("Party",[self.teamAlice])
	def teardown_method(self,method):
		del self.poolParty

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
		assert self.poolParty.numberOfMatches == 1
	def test_match_name(self):
		assert self.poolParty._matchList[0].name == "matchTest"
	def test_match_teams(self):
		assert self.poolParty._matchList[0]._teamA == self.teamAlice
		assert self.poolParty._matchList[0]._teamB == self.teamBob

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

class TestPool_winnerList_loserList_unmatchedList_ranking:
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
	
class TestPool_winnerList_loserList_unmatchedList_ranking_once_matchs_are_played:
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
	
	










class TestTournament_initialization:
	def setup_method(self,method):
		self.tournamentA = Tournament()
		self.poolA = Pool()
		
	def teardown_method(self,method):
		del self.tournamentA
		del self.poolA
 	
	def testTournamentInitialization(self):
		assert self.tournamentA.name == None
		assert self.tournamentA.poolList == []
		
 	def testInitializationRename(self):
		self.tournamentA.name = "Ultimate Tournament"
		assert self.tournamentA.name == "Ultimate Tournament"
		
	def testAddingPool(self):
		self.tournamentA.addPool(self.poolA)
		assert self.tournamentA.poolList == [self.poolA]




###
###	TESTS ON CLASS SingleElimination
###

#
# TESTS for SingleElimination

class TestSingleElimination:
	def setup_class(self):
		self.nOfTeams = 35
		self.thePool = Pool('inputPool', [Team('Team_'+str(i)) for i in range(1, self.nOfTeams+1)])
		self.theTournament = SingleElimination()
		self.theTournament.setInputPool(self.thePool)
		
	def teardown_class(self):
		del self.theTournament
		del self.thePool
		
	def testSettingInputPool(self):
		assert self.theTournament.inputPool == self.thePool
		# assert self.theTournament.nOfTeams == self.nOfTeams
		# assert self.theTournament.nOfAdditionnalTeams == 3
		# assert self.theTournament.nOfAdditionnalFirstPoolMatches == 3
		# assert self.theTournament.nOfFirstPoolByes == 29
		# assert self.theTournament.nTeamsIsPowerOf2 == False
		# assert self.theTournament.nOfLayers == 6
		
	# def testbuildAllPools(self):
		# self.theTournament.createPoolList()
		# assert self.theTournament.poolList[0] == self.thePool
		#NEED to write all assert	
		
		

