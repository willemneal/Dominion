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
        self.type = self.getType()
        self.src  = self.getImageLocation()

    def __str__(self):
        return self.name

    def getImageLocation(self):
        return "/static/images/%s.png" % (self.name.lower().replace(" ", ""))

    def isVictory(self):
    	return self.vp > 0

    def isCurse(self):
        return self.vp < 0

    def isTreasure(self):
		return isinstance(self, TreasureCard)

    def isAction(self):
		return isinstance(self, ActionCard)

    def getType(self):
        return str(type(self)).split(".")[1][:-2]

    def getAttr(self):
        return {"name":self.name,"src":self.src,
                "type":self.type,"cost":self.cost,
                "desc":self.desc,"vp":self.vp}

    def __repr__(self):
        return self.name

    def __cmp__(self, other):
        if other.cost > self.cost:
            return -1
        elif other.cost < self.cost:
            return  1
        return 0


class ActionCard(Card):

    def __init__(self, name, cost, desc, attack=False,
        isDefense = False, vp = 0,  action=(),
         reaction = False, actions=0, plusCards=0,reactionAction = ()):
        Card.__init__(self,name,cost,desc,vp)
        self.isDefense          = isDefense
        self.attack             = attack
        self.reaction           = reaction
        self.actions            = plusCards
        self.action             = action
        self.reactionAction     = reactionAction
        self.type = self.getType()

    def isAttack(self):
        return self.attack

    def isReaction(self):
        return self.reaction

    def reaction(self, player):
        if self.isReaction():
            return self.reactionAction(player)

    def play(self,turn):
        if self.isAttack():
            turn.event("Attack")
        self.action(turn)
        turn.log.append(str(turn.player.name) + " played "+ str(self.name) +": "+ str(self.desc))



class TreasureCard(Card):
    def __init__(self, name, cost, desc = "", vp = 0,
                coin = 0,reaction=False):
        Card.__init__(self, name, cost, desc=desc, vp=vp)
        self.coin     = coin
        self.type = self.getType()
        self.reaction = reaction

    def isReaction(self):
        return self.reaction


    def play(self,turn):
        turn.coins += self.coin
        return "tresure"
