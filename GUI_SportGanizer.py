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

'''
class GUI_Team():
	counter = 0
	__init__(self):
		counter += 1
		self.team = Team('team '+str(counter))

		name_input = TextInput(text='Hello world', multiline=False, size_hint=None, height=10)
'''


class GUI_TeamList():
	def __init__(self):
		self.teamList = [Team('team '+str(i+1)) for i in range(19)]


	def layout(self,**kwargs):

		button = Button(text='add team',pos_hint={'center_x':0.5},size_hint_x=None, size_hint_y=None, height=30, width=100)
		scrollSpace = ScrollView(size_hint=(1.0, 1.0))
		
		input_list = GridLayout(cols=2, spacing=5, size_hint_y=None)
		input_list.bind(minimum_height=input_list.setter('height'))

		for team in self.teamList:
			team_name = TextInput(text=team.name,size_hint_x=1.0, size_hint_y=None, height=30, multiline=False)
			delete_button = Button(text='-', size_hint_x=None, size_hint_y=None, height=20, width=20,)
			input_list.add_widget(team_name)
			input_list.add_widget(delete_button)
		scrollSpace.add_widget(input_list)

		mainLayout = BoxLayout(orientation='vertical', spacing=5,**kwargs)
		mainLayout.add_widget(button)
		mainLayout.add_widget(scrollSpace)

		return mainLayout


class SportGanizerApp(App):
	def build(self):
		mainLayout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=1)
		teamList = GUI_TeamList()
		treeLayout = BoxLayout(orientation='vertical', size_hint_x=1.0,spacing=15)
		# treeLayout.add_widget(Button(text='dumb'))

		mainLayout.add_widget(teamList.layout(size_hint_x=None, width=150))
		mainLayout.add_widget(treeLayout)

		return mainLayout



if __name__ == '__main__':
    SportGanizerApp().run()
