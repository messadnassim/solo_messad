from soccersimulator import GolfState,Golf,Parcours1,Parcours2,Parcours3,Parcours4
from soccersimulator import SoccerTeam,show_simu
from soccersimulator import Strategy,SoccerAction,Vector2D,settings
import logging
import math
from tools import MYState
from golf_exec import FonceStrategy, DemoStrategy, FonceStrategy_g

jean = Player("Drexor", FonceStrategy())
sydney = Player("Keeper", FonceStrategy())

solo = Player("miche-miche", FonceStrategy())
solo = Player("miche", FonceStrategy_g())

maestro = Player("Maestro", FonceStrategy())
leonardo = Player("Leo", FonceStrategy())



team1 = SoccerTeam("salom", [solo_s])



team2 = SoccerTeam("Two", [jean, sydney])

team_g = SoccerTeam("golf1", [solo_s2])


def get_golf_team():
	return team_g


def get_salom_team1():
	return team1

def get_salom_team2():
	return team2

