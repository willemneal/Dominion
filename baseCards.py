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
	#FIXME ADD ACTION

def bureaucratAction(turn):
	#FIXME ADD ACTION

def cellarAction(turn):
	#FIXME ADD ACTION

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
	turn.player.drawCards(3)

def spyAction(turn):
	#FIXME ADD ACTION

def theifAction(turn):
	#FIXME ADD ACTION

def throneRoomAction(turn):
	#FIXME ADD ACTION

def villageAction(turn):
	turn.player.drawCards(1)
	turn.updateActions(2)

def witchAction(turn):
	#FIXME ADD ACTION

def woodcutterAction(turn):
	#FIXME ADD ACTION

def workshopAction(turn):
	#FIXME ADD ACTION

#card = Card Type ("Name",Cost,"Description","action = action function")
adventurer = ActionCard("Adventurer",6,"Reveal cards from your deck until you reveal 2 Treasure card. Put those Tresure cards into your hand and discard the other revealed cards.", action = adventurerAction)
bureaucrat = ActionCard("Bureaucrat",4,"Gain a Silver card; put it on top of your deck. Each other player reveals a Victory card from his hand and puts it on his deck (or reveals a hand with no Victory cards)", action = bureacratAction)
cellar = ActionCard("Cellar",2,"+1 Card, +2 Actions", action = villageAction) 
chancellor = ActionCard("Chancellor",3,"+1 Card, +2 Actions", action = villageAction) 
chapel = ActionCard("Chapel",2,"Trash up to 4 cards from your hand.", action = chapelAction)
councilRoom = 
feast = ActionCard("Feast",3,"+1 Card, +2 Actions", action = villageAction) 
festival = 
garden = 
laboratory = 
library = 
market = 
militia =
mine = 
moat = ActionCard("Moat",3,"+1 Card, +2 Actions", action = villageAction) 
moneylender = 
remodel = 
smithy = ActionCard("Smithy",4,"+3 Cards", action = smithyAction)
spy = 
theif = 
throneRoom = 
village = ActionCard("Village",3,"+1 Card, +2 Actions", action = villageAction) 
witch = 
woodcutter = ActionCard("Woodcutter",3,"+1 Card, +2 Actions", action = villageAction) 
workshop = ActionCard("Workshop",3,"+1 Card, +2 Actions", action = villageAction) 
 











base = [adventurer, bureaucrat, cellar, chancellor, chapel, councilRoom, feast, festival, garden, laboratory, library, market, militia, mine, moat, moneylender, remodel, smithy, spy, theif, throneRoom, village, witch, woodcutter, workshop]