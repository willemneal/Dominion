from game import Game

def GameState(Object):
	def __init__(self,game):
		self.game = game
		self.state = {}
		self.state["supply"]= game.supply.toDict()
		self.state["log"]	= game.log

class PlayerState(GameState):
	def __init__(self,player,game):
		GameState.__init__(self,game)
		self.player = player
		self.state["hand"] = player.hand

		

	def isCurrentPlayer(self):
		return self.player == game.currertPlayer

	def getState(self):
		if isCurrentPlayer:
			self.state["turn"] = game.currentTurn.toDict()
			if self.player in G.currentTurn.playerChoice:
				self.state["choice"] = G.currentTurn.playerChoice
			self.state["phase"] = G.currentTurn.phase
		else:
			self.state["phase"] = "waiting"
			if self.player in G.currentTurn.playerChoice:
				self.state["choice"] =G.currentTurn.playerChoice[self.player]
		return self.state
