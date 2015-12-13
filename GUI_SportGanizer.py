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
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle



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

		self.makeButton = Button(text='make',pos_hint={'center_x':0.5},size_hint_x=None, size_hint_y=None, height=30, width=100)
		self.add_widget(self.makeButton)
		

		for i in range(n_init_teams):
			self.addTeam(None)
	
	def addTeam(self,addButton):
		team = GUI_Team('team '+str(len(self.teamList)+1))
		self.teamList.append(team)
		self.listLayout.add_widget(team)
		team.delete_button.bind(on_press=self.removeTeam)

	def update(self):
		self.listLayout.clear_widgets()
		for team in self.teamList:
			self.listLayout.add_widget(team)

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
		
		self.treeLayout = GridLayout(orientation='horizontal',rows=1, spacing=5, size_hint_y=None, size_hint_x=None)
		self.treeLayout.bind(minimum_height=self.treeLayout.setter('height'))
		self.treeLayout.bind(minimum_width=self.treeLayout.setter('width'))
		self.scrollSpace = ScrollView(size_hint=(1.0, 1.0))
		self.scrollSpace.add_widget(self.treeLayout)

		self.add_widget(self.scrollSpace)

	def make(self,teamList):
		self.tournament = SingleElimination(teamList)
		self.tournament.makeMatchTree()
		self.update()

	
	def update(self):
		self.treeLayout.clear_widgets()
		for pool in self.tournament.poolList[:-1]:
			poolBox = GridLayout(orientation='vertical', cols=1, spacing=5, size_hint_y=None, size_hint_x=None, width=260)
			for match in pool.matchList:
				gui_match = GUI_Match(match)
				poolBox.add_widget(gui_match)
				poolBox.bind(minimum_height=poolBox.setter('height'))
		
			self.treeLayout.add_widget(poolBox)



class GUI_Match(BoxLayout):
	def __init__(self,match, **kwargs):
		super(GUI_Match, self).__init__(orientation='horizontal', size_hint_x=None, spacing=5, width=250, size_hint_y=None, height=70, padding=5, **kwargs)
		self.match = match
		self.name = self.match.name

		self.labelName = Label(text=self.name, pos_hint={'center_y':0.5},size_hint_x=None, size_hint_y=None, height=45, width=55)
		self.labelA = Label(text=self.match._teamA.name)
		self.labelB = Label(text=self.match._teamB.name)			
		self.teamALayout = BoxLayout(orientation='horizontal')
		self.teamBLayout = BoxLayout(orientation='horizontal')
		self.teamsLayout = BoxLayout(orientation='vertical')
		
		if not self.match.ended: self.setActive()
		if self.match.ended: self.setInactive()
		self.update()


		with self.canvas.before:
			Color(0.2, 0.2, 0.2, 1)
			self.rect = Rectangle(size=self.size, pos=self.pos)
		self.bind(pos=self.update_rect, size=self.update_rect)

	def update_rect(instance, value, what): # I don't know what is what...
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size

	def setActive(self):
		self.scoreA = TextInput(text=str(self.match._scoreA),size_hint_x=None, width=40, multiline=False)	
		self.scoreA.bind(text=self.setScore)
		self.scoreB = TextInput(text=str(self.match._scoreB),size_hint_x=None, width=40, multiline=False)	
		self.scoreB.bind(text=self.setScore)
		self.endButton = Button(text='End', pos_hint={'center_y':0.5},size_hint_x=None, size_hint_y=None, height=45, width=45)		
		self.endButton.bind(on_press=self.endMatch)
	
	def update(self):
		self.teamALayout.clear_widgets()
		self.teamBLayout.clear_widgets()
		self.teamsLayout.clear_widgets()
		self.clear_widgets()

		self.teamALayout.add_widget(self.labelA)
		self.teamBLayout.add_widget(self.labelB)
		self.teamALayout.add_widget(self.scoreA)
		self.teamBLayout.add_widget(self.scoreB)
		self.teamsLayout.add_widget(self.teamALayout)
		self.teamsLayout.add_widget(self.teamBLayout)
		self.add_widget(self.labelName)
		self.add_widget(self.teamsLayout)
		self.add_widget(self.endButton)

	def setInactive(self):
		self.scoreA = Label(text=str(self.match._scoreA),size_hint_x=None, width=40)	
		self.scoreB = Label(text=str(self.match._scoreB),size_hint_x=None, width=40)	
		self.endButton = Button(text='Reset', pos_hint={'center_y':0.5},size_hint_x=None, size_hint_y=None, height=45, width=45)		
		self.endButton.bind(on_press=self.reactivate)

	def reactivate(self,button):
		print 'cannot "un-end" match !!!'
		self.parent.parent.parent.parent.update()

	def setScore(self,tInput,text):
		if tInput == self.scoreA:
			self.match.setScore(self.match._teamA,text)
		elif tInput == self.scoreB:
			self.match.setScore(self.match._teamB,text)

	def endMatch(self,button):
		self.match.endMatch()
		self.parent.parent.parent.parent.update()




class SportGanizerApp(App):
	def build(self):
		teamList = GUI_TeamList(size_hint_x=None, width=150)
		treeLayout = GUI_MatchTree()
		mainLayout = BoxLayout()

		teamList.makeButton.bind(on_press=lambda x: treeLayout.make(teamList.activeList()))

		mainLayout.add_widget(teamList)
		mainLayout.add_widget(treeLayout)

		return mainLayout

if __name__ == '__main__':
    SportGanizerApp().run()
