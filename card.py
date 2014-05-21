class Card(object):
    """
	This is the main class for a Card.
	A card can be an action, a treasure or a victory.
	It can aslo be a combination of victory and one of the the other two.

	Todo: add potion cards
    """
    def __init__(self, name, cost, desc="", vp=0):
    	self.name = name
    	self.cost = cost
    	self.desc = desc
    	self.vp   = vp

    def __str__(self):
        return self.name

    def isVictory(self):
    	return self.vp > 0

    def isCurse(self):
        return self.vp < 0

    def isTreasure(self):
		return isinstance(self, TreasureCard)

    def isAction(self):
		return isinstance(self, ActionCard)

    def __repr__(self):
        return self.name
	

class ActionCard(Card):
    
    def __init__(self, name, cost, desc, attack=False,
        isDefense = False, vp = 0,  action=(),
         reaction = False, actions=0, plusCards=0):
        Card.__init__(self,name,cost,desc,vp)
        self.isDefense          = isDefense
        self.attack             = attack
        self.reaction           = reaction
        self.actions            = plusCards
        self.action             = action
 

    def isAttack(self):
        return self.attack

    def isReaction(self):
        return self.reaction

    def play(self,turn):
        self.action(turn)



class TreasureCard(Card):
    def __init__(self, name, cost, desc = "", vp = 0, 
                coin = 0):
        Card.__init__(self, name, cost, desc=desc, vp=vp)
        self.coin     = coin


    def play(self,turn):
        turn.coins += self.coin






