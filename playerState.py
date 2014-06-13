

class GameState(object):
	def __init__(self,game):
		self.game = game
		self.state = {}
		self.state["supply"]= game.supply.toDict()
		self.state["log"]	= game.log



class PlayerState(GameState):
	def __init__(self,player,game):
		GameState.__init__(self,game)
		self.player = player

		

	def isCurrentPlayer(self):
		return self.player == self.game.currentPlayer

	def getState(self):
		self.state["hand"] = [card.name for card in self.player.hand]
		if self.isCurrentPlayer():
			self.state["turn"] = self.game.currentTurn.toDict()
			if self.player in self.game.currentTurn.playerChoice:
				self.state["choice"] = self.game.currentTurn.playerChoice
			self.state["phase"] = self.game.currentTurn.phase
		else:
			self.state["phase"] = "waiting"
			if self.player in self.game.currentTurn.playerChoice:
				self.state["choice"] =self.game.currentTurn.playerChoice[self.player]
		return self.state
