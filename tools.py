from soccersimulator import GolfState,Golf,Parcours1,Parcours2,Parcours3,Parcours4
from soccersimulator import SoccerTeam,show_simu
from soccersimulator import Strategy,SoccerAction,Vector2D,settings
import logging
import math





class MYState(object):
	def __init__(self,state,idteam,idplayer) :
		self.state = state
		self.key = (idteam, idplayer)
		
		self.my_position = self.state.player_state(self.key[0], self.key[1]).position
		self.ball_position = self.state.ball.position
		self.but_adv = Vector2D(150, 45) if self.key[0] == 1 else Vector2D(0, 45)	
		self.but = Vector2D(0, 45) if self.key[0] == 1 else Vector2D(150, 45)
		#recup joueur 
		self.all_players = self.state.players
		self.co_players = [p  for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
		
		#can the player shoot in the ball
		self.can_shoot = True if self.my_position.distance(self.ball_position) <= (settings.PLAYER_RADIUS + settings.BALL_RADIUS) else False
		#nouvelles motif pour simplifier
		self.sens = 1 if self.key[0] == 1 else -1
		
		
		
		
		
		#side of adv
		self.adv_on_right = 1 if self.state.player_state(self.adv_players[0][0], self.adv_players[0][1]).position.y > self.my_position.y else -1
		
		#vitesse balle
		self.v_ball = self.state.ball.vitesse
		
		#distance de la balle
		self.dist_ball = self.my_position.distance(self.ball_position)
		
		
		
		#mon vecteur vitesse
		self.my_v = self.state.player_state(self.key[0], self.key[1]).vitesse
		
		#est proche de la balle
		self.near_ball = True if self.my_position.distance(self.ball_position) < 20 else False
		
		#liste des coeq proche
		self.coeq_proche = [p for p in self.co_players if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < 75]
		
	@property
	def coeq_libre(self) :
		if len(self.coeq_proche) == 0 :
			return [0, 0]
		elif len(self.coeq_proche) == 1 :
			return self.coeq_proche[0]
		else :
			x = mstate.player_state(p[0], p[1]).position.distance(mstate.player_state(p[0], p[1]).adv_nearby())
			pp = coeq_proche[0]
			for p in coeq_proche[1:] :
				d = mstate.player_state(p[0], p[1]).position.distance(mstate.player_state(p[0], p[1]).adv_nearby())
				if x < d :
					x = d
					pp = p
			return pp
	@property
	def aller_ball(self) :
		#les cas ou je suis proche de la balle et elle va vite?
		v_ball = self.v_ball
		dist = self.dist_ball
		k = (v_ball*3+(self.ball_position - self.my_position))
		joue = SoccerAction(k, Vector2D())
		if self.dist_ball > 11:
			return joue
		elif self.dist_ball > 4:
			return SoccerAction((self.ball_position - self.my_position)/2, Vector2D())
		else :
			return SoccerAction((self.ball_position - self.my_position).normalize(), Vector2D())
	
	@property
	def predict_ball(self):
		norm_base = self.v_ball.norm
		norm_tour = self.v_ball.norm - settings.ballBrakeSquare * self.v_ball.norm ** 2 - settings.ballBrakeConstant * self.v_ball.norm 
		norm_fin = norm_base *2 - norm_tour
		for i in range (0, 3):
			norm_base = norm_fin
			norm_tour = norm_tour - settings.ballBrakeSquare * norm_tour ** 2 - settings.ballBrakeConstant * norm_tour 
			norm_fin = norm_base *2 - norm_tour
		ball_pos_fin = self.ball_position + (self.v_ball.normalize() * norm_fin)
		
		#print ball_pos_fin
		return ball_pos_fin
	"""def aller(self, p) :
		dist = p.distance(self.my_position)
		v_ball = self.v_ball
		k = (p-self.my_position)/300
		if dist > 10:
			return SoccerAction((p-self.my_position) , Vector2D())
		elif dist > 5:
			return SoccerAction((p-self.my_position) , Vector2D())
		return SoccerAction((p-self.my_position) , Vector2D())"""
	
	def aller(self, p) :
		#self.all_players_p
		dist = p.distance(self.my_position)
		v_ball = self.v_ball
		vec_dest = p-self.my_position
		if dist < 10:
			k = ((dist/4)%20)
			return SoccerAction(k*vec_dest, Vector2D())
		k = (dist)
		return SoccerAction(k*vec_dest, Vector2D())
	
	def shoot(self, p) :
		k = p.distance(self.my_position)/300
		"""if self.can_shoot :
			if (self.sens == 1 and self.my_position.x > 140) or (self.sens == -1 and self.my_position.x < 10) : 	
				if self.my_position.y > 70 or self.my_position.y < 20 :
					return self.drible()
					#return self.rebond #voir la variable step, et rajouter une variable dans le state a 5 par exp et je decremente a chaque tour
				return self.tire(p-self.my_position)"""
			#	return SoccerAction(Vector2D(),(p-self.my_position)/2)
	#sinon dans tout les autres cas
		if self.can_shoot :
			
			#print self.ball_position
			#i = self.predict_ball
			#print i
			if self.my_position.distance(p) < 20 :
				return self.tire((p-self.my_position)*2)
			return self.tire(k*(p-self.my_position))  
		else :
			#attendre 5 tours
			return self.aller_ball
	
	
	def tire(self, v):
		return SoccerAction(Vector2D(), v)
	
	@property
	def tirer(self):
		return SoccerAction(Vector2D(), (self.but_adv - self.my_position))
			
	"""
	@property
	def attaque_droite(self):
		if self.state.player_state(self.coeq_nearby[0], self.coeq_nearby[1]).position.distance(self.my_position) > 20:
			self.aller(self.ball_position) + shoot(self.state.player_state(self.coeq_nearby[0], self.coeq_nearby[1]).position) + 
		"""
		
	#recup adv le plus proche
	#@property
	def adv_nearby(self):
		players = self.adv_players
		"""if len(players) == 1:
			return None"""
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			ps_pp = self.state.player_state(pp[0], pp[1])
			dist_pp = self.my_position.distance(ps_pp.position)
			ps_p = self.state.player_state(p[0], p[1])
			dist_p = self.my_position.distance(ps_p.position)
			if dist_p < dist_pp :
				pp = p
		return pp
	
	def adv_danger_but(self):
		players = self.adv_players
		pp = players[0]
		for p in players:
			x_pp = self.state.player_state(pp[0], pp[1]).position.x
			x_p = self.state.player_state(p[0], p[1]).position.x
			if (x_p < x_pp and self.sens == 1) or (x_p > x_pp and self.sens == -1) :
				pp = p
		return pp
		
	
	def co_danger_but(self):
		players = self.co_players
		pp = players[0]
		for p in players:
			x_pp = self.state.player_state(pp[0], pp[1]).position.x
			x_p = self.state.player_state(p[0], p[1]).position.x
			if (x_p < x_pp and self.sens == -1) or (x_p > x_pp and self.sens == 1) :
				pp = p
		return pp
		
	
	def co_pball(self):
		players = self.co_players
		pp = (self.key[0], self.key[1])
		for p in players:
			dist_pp_ball = self.state.player_state(pp[0], pp[1]).position.distance(self.ball_position)
			dist_p_ball = self.state.player_state(p[0], p[1]).position.distance(self.ball_position)
			if (dist_pp_ball > dist_p_ball) :
				pp = p
		return pp
	
	def adv_pball(self):
		players = self.adv_players
		pp = players[0]
		for p in players:
			dist_pp_ball = self.state.player_state(pp[0], pp[1]).position.distance(self.ball_position)
			dist_p_ball = self.state.player_state(p[0], p[1]).position.distance(self.ball_position)
			if (dist_pp_ball > dist_p_ball) :
				pp = p
		return pp 
	
	def pos_j(self, p):
		return self.state.player_state(p[0], p[1]).position
		
	def passe(self, p):
		player = self.state.player_state(p[0], p[1])
		j_pos = player.position
		dist = self.my_position.distance(j_pos) 
		#k = dist/ 
		player = self.state.player_state(p[0], p[1])
		v_p = player.vitesse
		vect =( j_pos + math.log(dist*3)*v_p ) - self.my_position
		if self.can_shoot :
			return SoccerAction(Vector2D(), vect)
		return self.aller(self.ball_position)
	#log(dist*3) : proche 9/11, moyen 6/11, 7/11
	
	def adv_nearbyj(self, idteam, idplayer) :
		if self.idteam == idteam :
			return adv_nearby()
		else :
			return coeq_nearby()
		
	
		#recup adv le plus proche
	def coeq_nearby(self):
		
		players = self.co_players
		"""if len(players) == 1:
			return """
		pp = players[0]
		
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return pp
	
	#true if player p near ball
	def p_near_ball(self, p):
		return True if self.ball_position.distance(self.state.player_state(p[0], p[1]).position) < 20 else False
		
	
	def joueur_pos(self, x, y) :
		for p in self.all_players :
			if ( self.state.player_state(p[0], p[1]).position == Vector2D(x, y) ) :
				return p
				
	def drible(self) :
		adv = self.adv_nearby()
		sens = self.sens
		
		me = self.my_position
		adv_pos = self.state.player_state(adv[0], adv[1]).position
		#print self.state.player_state(self.key[0], self.key[1])._rd_angle(Vector2D(1, 1), 90, 1)
		if sens == 1 :
			if me.x < adv_pos.x :
				if me.y < adv_pos.y :
					return self.shoot((self.ball_position + sens*Vector2D(10, -10)).normalize()*7) # + self.aller(self.ball_position + sens*Vector2D(10, -10))
				else :
					return self.shoot((self.ball_position + sens*Vector2D(10, 10)).normalize()*7) #+ self.aller(self.ball_position + sens*Vector2D(10, -10))
		elif me.x > adv_pos.x :
			if me.y	< adv_pos.y :
				return self.shoot((self.ball_position + sens*Vector2D(10, 10)).normalize()*7) #+ self.aller(self.ball_position + sens*Vector2D(10, -10))	
			else:
				return self.shoot((self.ball_position + sens*Vector2D(10, -10)).normalize()*7) #+ self.aller(self.ball_position + sens*Vector2D(10, -10))
		else :
			return self.shoot((self.but_adv+me)/2)


