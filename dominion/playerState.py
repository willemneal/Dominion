class GameState(object):
	def __init__(self,game):
		self.game = game
		self.state = {}
		self.state["supply"]= game.supply.toDict()
		self.state["log"]	= game.log

class PlayerState(GameState):
	def __init__(self,player,game):
		super(PlayerState,self).__init__(game)
		self.player = player

	def isCurrentPlayer(self):
		return self.player == self.game.currentPlayer

	def setState(self):
		self.state["hand"] = [card.getAttr() for card in self.player.hand]
		self.state["coinInHand"] = self.player.coinInHand()
		self.state['choice'] = self.game.currentTurn.playerChoice[self.player.name]
		self.state["supply"]= self.game.supply.toDict()
		self.state["choice"] =self.game.currentTurn.playerChoice[self.player.name]
		if self.isCurrentPlayer():
			self.state["turn"] = self.game.currentTurn.toDict()
			self.state["phase"] = self.game.currentTurn.phase
		else:
			self.state["phase"] = "waiting"


	def getState(self):
		return self.state
