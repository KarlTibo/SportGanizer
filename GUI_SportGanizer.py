# -*- coding: utf-8 -*-

from SportGanizer import *
from kivy.app import App


from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown


class SportGanizerApp(App):
	def build(self):

		#name_input = TextInput(text='Hello world', multiline=False, size_hint=None, height=10)
		#make_button = Button(text='make_tournament', size_hint=(0.1, 0.1))

		dropdown = DropDown()
		for index in range(10):
			btn = TextInput(text='Team %d' % index, size_hint_y=None, height=44,multiline=False)
			dropdown.add_widget(btn)

		mainbutton = Button(text='Hello', size_hint=(None, None))
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

		return mainbutton



if __name__ == '__main__':
    SportGanizerApp().run()
