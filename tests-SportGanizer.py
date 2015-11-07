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
		assert self.poolParty.teamList == []
	def test_pool_initialization(self):
		assert self.poolParty.matchList == []

class TestPool_initialization_with_team:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.poolParty = Pool("Party",[self.teamAlice])
	def teardown_method(self,method):
		del self.poolParty

	def test_nOfTeams_increased(self):
		assert self.poolParty.nOfTeams == 1
	def test_pool_initialization(self):
		assert self.poolParty.teamList == [self.teamAlice]

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
		assert self.teamAlice in self.poolParty.teamList

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
		assert self.teamAlice in self.poolParty.teamList
		assert self.teamBob in self.poolParty.teamList
	def test_number_of_match_increased(self):
		assert self.poolParty.numberOfMatches == 1
	def test_match_name(self):
		assert self.poolParty.matchList[0].name == "matchTest"
	def test_match_teams(self):
		assert self.poolParty.matchList[0].teamA == self.teamAlice
		assert self.poolParty.matchList[0].teamB == self.teamBob

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
		assert self.teamAlice in self.poolParty.teamList
		assert self.teamBob in self.poolParty.teamList
	def test_addTeam_with_list_order(self):
		assert self.poolParty.teamList[0] == self.teamAlice
		assert self.poolParty.teamList[1] == self.teamBob

class TestPool_ranking:
	def setup_method(self,method):
		self.teamAlice = Team("Alice")
		self.teamBob = Team("Bob") 	
		self.teamCharlie = Team("Charlie")
		self.poolParty = Pool("Party")
	def teardown_method(self,method):
		del self.teamAlice
		del self.teamBob
		del self.poolParty

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
		assert self.tournamentA.name == None
		assert self.tournamentA.poolList == []
		
 	def testInitializationRename(self):
		self.tournamentA.rename("Ultimate Tournament")
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
		
		

