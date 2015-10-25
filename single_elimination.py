# -*- coding: utf-8 -*-

#installer 
#http://graph-tool.skewed.de/
#http://networkx.github.io/
#http://igraph.org/python/
from numpy import *


###########################################################################################
#Définition des objets nécessaires

class equipe:
#Doit contenir les infos nécessaires à propos de chaque équipe
	def __init__(self, name="equipe", n_players=1, player_names=["a"]):
		self.name = name
		self.n_players = n_players
		self.player_names = player_names


class terrain:
#Doit contenir les infos nécessaires à propos de chaque terrain
	def __init__(self, name="terrain", location="indoors", availability="always"):
		self.name = name
		self.location = location
		self.availability = availability
		

#class time_constraints:
#Est-ce que l'utilisateur veut qu'on fasse un horaire avec le temps explicite?
#	def __init__(self, name="time"):
#		self.name = name
		

class match:
#Contient les infos pour chaque match
	def __init__(self, name, equipe1=equipe(), equipe2=equipe(), terrain=terrain(), time=None):
		self.name = name
		self.versus = [equipe1,equipe2]
		self.location = terrain
		self.time = time
		self.winner = equipe('winner'+name)
		
	def set_winner(number=0):
		if number==1:
			self.winner = equipe1
		elif number==2:
			self.winner = equipe2
		else:
			pass
		
			


#class type_tournoi:
#Quel type de tournoi l'utilisateur veut il creer?
#	def __init__(self, name="single_elimination"):
#		self.name = single_elimination
		


###########################################################################################
#Définition des variables input par l'utilisateur

n_equipe=28

terrain1=terrain()

use_time="True"

starting_time=10.00

match_time=1.00

pause_between="True"

type_tournoi="single_elimination"

#equipe 1 = input dans l'interface graphique (Les Moldus)

###########################################################################################
#Définition des fonctions nécessaires
def n_round(n_equipe, type_tournoi):
	if type_tournoi=="single_elimination":
		return int(ceil(log2(n_equipe)))
	elif type_tournoi=="double_elimination":
		return "Its complicated"
	else:
		return "Its complicated"


def n_match(n_equipe, type_tournoi):
	if type_tournoi=="single_elimination":
		if float.is_integer(log2(n_equipe))==True:
			n_match_per_round=[]
			for i in arange(0,n_round(n_equipe, type_tournoi)):
				n_match_per_round.append(n_equipe/2/(2**i))
			return n_match_per_round
		else:
			n_bye=2**n_round(n_equipe, type_tournoi)-n_equipe
			n_match_per_round=[(n_equipe-n_bye)/2]
			for i in arange(1,n_round(n_equipe, type_tournoi)):
				n_match_per_round.append((n_equipe-(n_equipe-n_bye)/2)/(2**i))
			return n_match_per_round
	elif type_tournoi=="double_elimination":
		return n_equipe                     #CHANGE THAT LATER
	elif type_tournoi=="round_robin":
	#Calcule le nombre de matchs par pool
		return n_equipe                     #CHANGE THAT LATER



#def n_match(n_equipe, type_tournoi):
#	if type_tournoi in ("single_elimination", "double_elimination"):
#	#Calcule le nombre de matchs par round ou pour la première round
#		if n_equipe%2==0:
#			return n_equipe/2
#		else:
#			return n_equipe/2+1 #PAS BON LOL
#	elif type_tournoi=="round_robin":
#	#Calcule le nombre de matchs par pool
#		return n_equipe                     #CHANGE THAT LATER




#Liste des équipes
equipes=[]
for i in arange(0,n_equipe):
	equipes.append(equipe("equipe%i"%(i+1)))
				
				
round[1].n_match				
				



				
def make_schedule(type_tournoi, use_time=False):
#Crée l'horaire
	if use_time==False:
		if type_tournoi=="single_elimination":
			if float.is_integer(log2(n_equipe))==True:
				horaire=[]
				for i in arange(0,n_match(n_equipe, type_tournoi)[0]):
					horaire.append(match("Match %i-%i"%(1,i+1), equipes[i], equipes[n_equipe-i-1], terrain1))
				for i in arange(1,n_round(n_equipe, type_tournoi)):
					for j in arange(0,n_match(n_equipe, type_tournoi)[i]):
						horaire.append(match("Match %i-%i"%(i+1,j+1), equipe("Winner %i-%i"%(i,2*j+1)), equipe("Winner %i-%i"%(i,2*j+2))))
				#for i in arange(0,n_match(n_equipe, type_tournoi)):
					#for j in arange(0,n_round(n_equipe, type_tournoi)):
						#horaire.append(match("match %i-%i"%(i+1,j+1), equipes[i], equipes[j], terrain1, 2))
				return horaire
			else:
				horaire=[]
				#Déterminer les équipes qui s'affronte en ronde 0
				for i in arange(0,n_match(n_equipe, type_tournoi)[0]):
					horaire.append(match("Match %i-%i"%(0,i+1), equipes[n_equipe-n_match(n_equipe, type_tournoi)[0]*2+i], equipes[n_equipe-i-1], terrain1))
				#Déterminer les match de 1ere ronde qui ont 1 "Winner" de la ronde 0
				for i in arange(0,n_match(n_equipe, type_tournoi)[1]-max(0,-(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))-max(0,(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))):
					horaire.append(match("Match %i-%i"%(1,i+1), equipes[i], equipe("Winner %i-%i"%(0,n_match(n_equipe, type_tournoi)[0]-i)), terrain1))
				#Déterminer les match de 1ere ronde qui ont 2 "Winner" de la ronde 0
				for i in arange(0,max(0,-(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))):
					horaire.append(match("Match %i-%i"%(1,i+1+n_match(n_equipe, type_tournoi)[1]-max(0,-(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))-max(0,(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))), equipe("Winner %i-%i"%(0,n_match(n_equipe, type_tournoi)[0]-i)), equipe("Winner %i-%i"%(0,n_match(n_equipe, type_tournoi)[0]-i)), terrain1))
				#Déterminer les match de 1ere ronde entre les équipes qui avaient un bye
				for i in arange(0,max(0,n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0])):
					horaire.append(match("Match %i-%i"%(1,i+1+n_match(n_equipe, type_tournoi)[1]-2*max(0,-(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))-max(0,(n_match(n_equipe, type_tournoi)[1]-n_match(n_equipe, type_tournoi)[0]))), equipes[i+n_match(n_equipe, type_tournoi)[0]], equipes[n_equipe-i-1-n_match(n_equipe, type_tournoi)[0]*2], terrain1))
				#Déterminer les rondes 2 et +
				for i in arange(2,n_round(n_equipe, type_tournoi)):
					for j in arange(0,n_match(n_equipe, type_tournoi)[i]):
						horaire.append(match("Match %i-%i"%(i,j+1), equipe("Winner %i-%i"%(i-1,j+1)), equipe("Winner %i-%i"%(i-1,n_match(n_equipe, type_tournoi)[i-1]-j))))
				#for i in arange(0,n_match(n_equipe, type_tournoi)):
					#for j in arange(0,n_round(n_equipe, type_tournoi)):
						#horaire.append(match("match %i-%i"%(i+1,j+1), equipes[i], equipes[j], terrain1, 2))
				return horaire
		else:
			return "Its complicated"
	else:
		return "Its complicated"



def show_schedule(schedule):
	for i in arange(0,n_round(n_equipe, type_tournoi)):
		for j in arange(0,n_match(n_equipe, type_tournoi)[i]):
			print [schedule[j+int(sum(n_match(n_equipe, type_tournoi)[0:i]))].name,schedule[int(sum(n_match(n_equipe, type_tournoi)[0:i]))+j].versus[0].name,schedule[int(sum(n_match(n_equipe, type_tournoi)[0:i]))+j].versus[1].name]

show_schedule(make_schedule(type_tournoi))


