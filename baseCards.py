from card import Card
from card import ActionCard
from card import TreasureCard


curse    = Card('Curse',    0, vp = -1)
estate   = Card('Estate',   2, vp = 1)
duchy    = Card('Duchy',    5, vp = 3)
province = Card('Province', 8, vp = 6)

copper   = TreasureCard('Copper',  0, coin = 1)
silver   = TreasureCard('Silver',  3, coin = 2)
gold     = TreasureCard('Gold',    6, coin = 3)

def adventurerAction(turn):
	tmp = []
	numOfTreasures = 0
	
	while numOfTreasures<2:
		card = turn.player.drawCards(1)[0] #draw one card
		if card.isTreasure():
			numOfTreasures+=1
			self.player.hand.append(card)
		else:
			tmp.append(card)
	self.player.discard.extend(tmp)

def bureaucratAction(turn):
	turn.player.deck.addCardOnTop(turn.player.supply.gainCard(silver))
	for player in turn.otherPlayers:
		for card in player.hand:
			if card.isVictory():
				print player," please select a victory card."	
				cardindex = turn.promptCardsIndex(player.hand)
				while not player.hand[cardindex].isVictory():
					cardindex = turn.promptCardsIndex(player.hand)
				player.deck.addCardOnTop(player.hand.pop(cardindex))
				break

def cellarAction(turn):
	turn.updateActions(1)
	cardIndex = 0
	while cardIndex is not None:
		cardIndex = turn.promptCardsIndex(turn.player.hand)
		turn.player.discard()



def chancellorAction(turn):
	#FIXME ADD ACTION

def chapelAction(turn):
	turn.chooseTrash(4, turn.player)

def councilRoomAction(turn):
	#FIXME ADD ACTION

def feastAction(turn):
	#FIXME ADD ACTION

def festivalAction(turn):
	#FIXME ADD ACTION

def laboratoryAction(turn):
	#FIXME ADD ACTION

def libraryAction(turn):
	#FIXME ADD ACTION

def militiaAction(turn):
	#FIXME ADD ACTION

def mineAction(turn):
	#FIXME ADD ACTION

def moatAction(turn):

def moneylenderAction(turn):
	#FIXME ADD ACTION

def remodelAction(turn):
	#FIXME ADD ACTION

def smithyAction(turn):
	turn.player.drawToHand(3)

def spyAction(turn):
	#FIXME ADD ACTION

def theifAction(turn):
	#FIXME ADD ACTION

def throneRoomAction(turn):
	#FIXME ADD ACTION

def villageAction(turn):
	turn.player.drawToHand(1)
	turn.updateActions(2)

def witchAction(turn):
	#FIXME ADD ACTION

def woodcutterAction(turn):
	#FIXME ADD ACTION

def workshopAction(turn):
	#FIXME ADD ACTION

#card = Card Type ("Name",Cost,"Description","action = action function")
adventurer = ActionCard("Adventurer",6,"Reveal cards from your deck until you reveal 2 Treasure cards. Put those Tresure cards into your hand and discard the other revealed cards.", action = adventurerAction)
bureaucrat = ActionCard("Bureaucrat",4,"Gain a Silver card; put it on top of your deck. Each other player reveals a Victory card from his hand and puts it on his deck (or reveals a hand with no Victory cards).", attack=True, action = bureacratAction)
cellar = ActionCard("Cellar",2,"+1 Action, Discard and number of cards. +1 Card per card discarded.", action = cellarAction) 
chancellor = ActionCard("Chancellor",3,"+$2, You may immediately put your deck into your discard pile.", action = chancellorAction) 
chapel = ActionCard("Chapel",2,"Trash up to 4 cards from your hand.", action = chapelAction)
councilRoom = ActionCard("Council Room", 5, "+4 Cards, +1 Buy, Each other player draws a card.", action = councilRoomAction)
feast = ActionCard("Feast",3,"Trash this card. Gain a card costing up to 5.", action = feastAction) 
festival = ActionCard("Festival", 5, "+2 Actions, +1 Buy, +$2", action = festivalAction)
garden = Card("Garden", 4, "Worth 1VP for every 10 cards in your deck (rounded down).", vp=True) 
laboratory = ActionCard("Laboratory", 5, "+2 Cards, +1 Action", action = laboratoryAction)
library = ActionCard("Library", 5, "Draw until you have 7 cards in hand. You may set aside any Action cards drawn this way, as you draw them; discard the set aside cards after you finish drawing.", action = libraryAction)
market = ActionCard("Market", 5, "+1 Card, +1 Action, +1 Buy, +$1", action = marketAction)
militia = ActionCard("Militia", 5, "+$2, Each other player discards down to 3 cards in his hand.", attack=True, action = militiaAction)
mine = ActionCard("Mine", 5, "Trash a Treasure card from your hand. Gain a Treasure card costing up to $3 more; put it into your hand.", action = mineAction)
moat = ActionCard("Moat",2, "+2 Cards, Reaction: When another player plays an Attack card, you may reveal this from your hand. If you do, you are unaffected by that Attack.", isDefense=True, action = moatAction, reaction=True) 
moneylender = ActionCard("Moneylender", 4, "Trash a Copper card from your hand. If you do, +$3.", action = moneylenderAction)
remodel = ActionCard("Remodel", 4, "Trash a card from your hand. Gain a card costing up to $2 more than the trashed card.", action = remodelAction)
smithy = ActionCard("Smithy", 4,"+3 Cards", action = smithyAction)
spy = ActionCard("Spy", 4, "+1 Card, +1 Action, Each player (including you) reveals the top card of his deck and either discards it or puts it back, your choice.", attack=True, action = spyAction)
theif = ActionCard("Theif", 4, "Each other player reveals the top 2 cards of his deck. If they revealed any Treasure cards, they trash one of them that you choose. You may gain any or all of these trashed cards. They discard the other revealed cards.", attack=True, action = theifAction)
throneRoom = ActionCard("Throne Room", 4, "Choose an Action card in your hand. Play it twice.", action = throneRoomAction)
village = ActionCard("Village",3,"+1 Card, +2 Actions", action = villageAction) 
witch = ActionCard("Witch", 5, "+2 Cards, Each other player gains a Curse card.", attack=True, action = witchAction)
woodcutter = ActionCard("Woodcutter",3,"+1 Buy, +$2", action = woodcutterAction) 
workshop = ActionCard("Workshop",3,"Gain a card costing up to $4.", action = workshopAction) 
 











base = [adventurer, bureaucrat, cellar, chancellor, chapel, councilRoom, feast, festival, garden, laboratory, library, market, militia, mine, moat, moneylender, remodel, smithy, spy, theif, throneRoom, village, witch, woodcutter, workshop]