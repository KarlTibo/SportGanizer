# -*- coding: utf-8 -*-

from SportGanizer import *
from kivy.app import App


from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
#from kivy.uix.dropdown import DropDown
from kivy.uix.listview import ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class GUI_Team(BoxLayout):
	def __init__(self, name = 'team' ,**kwargs):
		super(GUI_Team, self).__init__(orientation='horizontal', spacing=5, size_hint_y=None, height=30, **kwargs)
		self.team = Team(name)

		self.name_input = TextInput(text=self.team.name,size_hint_x=1.0, multiline=False)	
		self.name_input.bind(text=self.rename)
		self.add_widget(self.name_input)

		self.delete_button = Button(text='-', pos_hint={'center_y':0.5}, size_hint_x=None, size_hint_y=None, height=25, width=25)
		self.add_widget(self.delete_button)
		
	def rename(self,instance,text):
		self.team.name = text


class GUI_TeamList(BoxLayout):							# NOTE : important that the layout is not a function otherwise binding fails.
	def __init__(self, n_init_teams=2, **kwargs):
		super(GUI_TeamList, self).__init__(orientation='vertical', spacing=5, padding=10, **kwargs)
		self.teamList = []
		
		self.listLayout = GridLayout(cols=1, spacing=5, size_hint_y=None)
		self.listLayout.bind(minimum_height=self.listLayout.setter('height'))
		self.scrollSpace = ScrollView(size_hint=(1.0, 1.0))
		self.scrollSpace.add_widget(self.listLayout)
		
		self.addTeamButton = Button(text='add team',pos_hint={'center_x':0.5},size_hint_x=None, size_hint_y=None, height=30, width=100)
		self.addTeamButton.bind(on_press=self.addTeam)

		self.add_widget(self.addTeamButton)
		self.add_widget(self.scrollSpace)

		for i in range(n_init_teams):
			self.addTeam(None)
	
	def addTeam(self,addButton):
		team = GUI_Team('team '+str(len(self.teamList)+1))
		self.teamList.append(team)
		self.addTeamToLayout(team)
		team.delete_button.bind(on_press=self.removeTeam)

	def addTeamToLayout(self,team):
		self.listLayout.add_widget(team)

	def update(self):
		self.listLayout.clear_widgets()
		for team in self.teamList:
			self.addTeamToLayout(team)

	def removeTeam(self,button):
		for team in self.teamList:
			if team.delete_button == button:
				teamToDelete = team
		self.teamList.remove(teamToDelete)
		self.update()

	def activeList(self):
		return [t.team for t in self.teamList]


class GUI_MatchTree(BoxLayout):
	def __init__(self, **kwargs):
		super(GUI_MatchTree, self).__init__(orientation='vertical', spacing=5, padding=10, **kwargs)
		self.teamList = []
		
		self.treeLayout = GridLayout(cols=1, spacing=5, size_hint_y=None)
		self.treeLayout.bind(minimum_height=self.treeLayout.setter('height'))
		self.treeLayout.bind(minimum_width=self.treeLayout.setter('width'))
		self.scrollSpace = ScrollView(size_hint=(1.0, 1.0))
		self.scrollSpace.add_widget(self.treeLayout)

		self.add_widget(self.scrollSpace)

	def make(self,teamList):
		tournament = SingleElimination(teamList)
		tournament.makeMatchTree()

		# def update ?
		for pool in tournament.poolList:
			pool.show()
			'''
			add a PoolBox
			for match in pool:
				add match to PoolBox
			'''
	

class SportGanizerApp(App):
	def build(self):
		teamList = GUI_TeamList(size_hint_x=None, width=150)
		treeLayout = GUI_MatchTree()
		mainLayout = BoxLayout()

		makeButton = Button(text='make',pos_hint={'left_x':0},size_hint_x=None, size_hint_y=None, height=30, width=100)
		makeButton.bind(on_press=lambda x: treeLayout.make(teamList.activeList()))

		mainLayout.add_widget(teamList)
		mainLayout.add_widget(makeButton)
		mainLayout.add_widget(treeLayout)

		return mainLayout

if __name__ == '__main__':
    SportGanizerApp().run()
