from soccersimulator import GolfState,Golf,Parcours1,Parcours2,Parcours3,Parcours4
from soccersimulator import SoccerTeam,show_simu
from soccersimulator import Strategy,SoccerAction,Vector2D,settings
from tools import MYState


GOLF = 0.001
SLALOM = 10.


class DemoStrategy(Strategy):
    def __init__(self):
        super(DemoStrategy,self).__init__("Demo")
    def compute_strategy(self,state,id_team,id_player):
        """ zones : liste des zones restantes a valider """
        zones = state.get_zones(id_team)
        if len(z)==0:
            """ shooter au but """
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                    Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
        """ zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
            centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
            zone.dedans(point) : teste si le point est dans la zone
        """
        zone = z[0]
        """ si la ball est dans une zone a valider """
        if zone.dedans(state.ball.position):
            return SoccerAction()
        """ sinon """
        distance = state.player_state(id_team,id_player).position.distance(zone.position+Vector2D(zone.l,zone.l))
        return SoccerAction()

class FonceStrategy_g(Strategy):
	def __init__(self):
		super(FonceStrategy_g,self).__init__("Fonceur_g")
	def compute_strategy(self,state,id_team,id_player):
		#mstate = MyState(state,idteam,idplayer)
		""" zones : liste des zones restantes a valider """
		zones = state.get_zones(id_team)
		if len(zones)==0:
			""" shooter au but """
			return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
				Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
		""" zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
      	      centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
      	      zone.dedans(point) : teste si le point est dans la zone
      	"""
		zone = zones[0]
     		""" si la ball est dans une zone a valider """
		if zone.dedans(state.ball.position):
			if state.ball.vitesse <= GOLF:
				
				if len(zones) == 1:
					if id_team ==1:
						zone = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
					else:
						zone = Vector2D(0,settings.GAME_HEIGHT/2.)
				else :
					zones = zones[1:len(zones)-1]
					zone = zones[0]
				return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
					Vector2D(0,((zone.position+Vector2D(zone.l/2.,zone.l/2.))-state.ball.position).normalize()*10))
			else :
				return
        	""" sinon """
		distance = state.player_state(id_team,id_player).position.distance(zone.position+Vector2D(zone.l,zone.l))
		return SoccerAction((state.ball.position-state.player_state(id_team,id_player).position).normalize()*distance,\
			(((zone.position+Vector2D(zone.l/2.,zone.l/2.))-state.ball.position).normalize()*distance/15))


class FonceStrategy(Strategy):
	def __init__(self):
		super(FonceStrategy,self).__init__("Fonceur")
	def compute_strategy(self,state,id_team,id_player):
		""" zones : liste des zones restantes a valider """
		zones = state.get_zones(id_team)
		if len(zones)==0:
			""" shooter au but """
			return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
				Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
		""" zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
      	      centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
      	      zone.dedans(point) : teste si le point est dans la zone
      	"""
		zone = zones[0]
     		""" si la ball est dans une zone a valider """
		if zone.dedans(state.ball.position):
			if state.ball.vitesse <= SLALOM:
				
				if len(zones) == 1:
					if id_team ==1:
						zone = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
					else:
						zone = Vector2D(0,settings.GAME_HEIGHT/2.)
				else :
					zones = zones[1:len(zones)-1]
					zone = zones[0]
				return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
					((zone.position+Vector2D(zone.l/2.,zone.l/2.))-state.ball.position).normalize()*10)
			else:
				return
        	""" sinon """
		distance = state.player_state(id_team,id_player).position.distance(zone.position+Vector2D(zone.l,zone.l))
		return SoccerAction((state.ball.position-state.player_state(id_team,id_player).position).normalize()*distance,\
			(((zone.position+Vector2D(zone.l/2.,zone.l/2.))-state.ball.position).normalize()*distance/15))


class FonceStrategy_2vs2(Strategy):
	def __init__(self):
		super(FonceStrategy_2vs2,self).__init__("Fonceur1et2")
	def compute_strategy(self,state,id_team,id_player):
		mstate = MyState(state,idteam,idplayer)
		""" zones : liste des zones restantes a valider """
		zones = state.get_zones(id_team)
		if len(zones)==0:
			""" shooter au but """
			return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
				Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)
		""" zone : carre de zone avec z.position angle bas,gauche et z.l longueur du cote
      	      centre du carre : zone.position+Vector2D(z.l/2.,z.l/2.)
      	      zone.dedans(point) : teste si le point est dans la zone
      	"""
		zone = zones[0]
     		""" si la ball est dans une zone a valider """
		if zone.dedans(state.ball.position):
			if state.ball.vitesse <= SLALOM:
				
				if len(zones) == 1:
					if id_team ==1:
						zone = Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
					else:
						zone = Vector2D(0,settings.GAME_HEIGHT/2.)
				else :
					zones = zones[1:len(zones)-1]
					zone = zones[0]
				return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
					((zone.position+Vector2D(zone.l/2.,zone.l/2.))-state.ball.position).normalize()*10)
			else:
				return
        	""" sinon """
		distance = state.player_state(id_team,id_player).position.distance(zone.position+Vector2D(zone.l,zone.l))
		return SoccerAction((state.ball.position-state.player_state(id_team,id_player).position).normalize()*distance,\
			(((zone.position+Vector2D(zone.l/2.,zone.l/2.))-state.ball.position).normalize()*distance/15))



team1 = SoccerTeam()
team2 = SoccerTeam()
team1.add("John",FonceStrategy_g())
team2.add("John",FonceStrategy_g())
#simu = Parcours1(team1=team1,vitesse=GOLF)
#show_simu(simu)
#simu = Parcours2(team1=team1,vitesse=GOLF)
#show_simu(simu)
#simu = Parcours3(team1=team1,vitesse=SLALOM)
#show_simu(simu)
#simu = Parcours4(team1=team1,team2=team2,vitesse=SLALOM)
#show_simu(simu)
