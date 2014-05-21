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


def chapelAction(turn):
	turn.chooseTrash(4, turn.player)

def smithyAction(turn):
	turn.player.drawCards(3)

def villageAction(turn):
	turn.player.drawCards(1)
	turn.updateActions(2)

cellar = ActionCard("Cellar",3,"+1 Card, +2 Actions", action = villageAction) 
moat   = ActionCard("Moat",3,"+1 Card, +2 Actions", action = villageAction) 
chancellor = ActionCard("Chancellor",3,"+1 Card, +2 Actions", action = villageAction) 
woodcutter = ActionCard("Woodcutter",3,"+1 Card, +2 Actions", action = villageAction) 
workshop = ActionCard("Workshop",3,"+1 Card, +2 Actions", action = villageAction) 
bureaucrat = ActionCard("Bureaucrat",3,"+1 Card, +2 Actions", action = villageAction) 

feast = ActionCard("Feast",3,"+1 Card, +2 Actions", action = villageAction) 




chapel = ActionCard("Chapel",2,"Trash up to 4 cards from your hand.",
			action = chapelAction)

smithy = ActionCard("Smithy",4,"+3 Cards", action = smithyAction)

village = ActionCard("Village",3,"+1 Card, +2 Actions", action = villageAction) 

#cellar = ActionCard("Cellar",2,"",)

base = [cellar, chapel, smithy, village, moat,
        chancellor, woodcutter, workshop, bureaucrat, feast]