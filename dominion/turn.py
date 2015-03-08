from listener import Listener
from gameObject import GameObject


class Turn(GameOject):
    gain = 'gain'
    buy = 'buy'
    fromHand = 'fromHand'

    def __init__(self, player, otherPlayers, roundNumber, log, game):
        self.game = game
        self.player = player
        self.otherPlayers = otherPlayers
        self.actions = 1
        self.buys = 1
        self.coins = 5
        self.hand = player.hand
        self.currentPlayer = player
        self.playerChoice = {}
        self.log = log
        self.prompt = ""
        self.log.append("It is %s's turn" % self.player)
        self.playerDecision = {}

        self.subscribePlayers()
        self.event('Start Turn',self)


        for player in otherPlayers:
            self.playerChoice[player.name] = None
        self.event('Action Phase')

    def startActionPhase(self):
        self.log.append("Action Phase")
        if self.player.hasActionCard():
            self.phase = "action"
            print "about to prompt!!"
            self.promptAction()
            print self.playerChoice[self.player.name], "choice"
        elif self.player.hasTreasureCard():
            self.startBuyPhase()
        else:
            self.endTurn()


    def subscribeListeners(self):
        '''Check to see if there are cards that react and must listen
           For now this is just reaction cards'''
        self.addSubcriber('Action Phase',self.startActionPhase)
        self.addSubcriber('Clean Up Phase',self.endTurn)
        self.addSubcriber('Buy', self.buyCard)
        self.addSubcriber('Gain', self.gainCard)
        listeners = [self.supply,self.player] + self.otherPlayers
        self.update(self.supply)
        map(lambda player:self.update(player),self.players+self.otherPlayers)




    def endTurn(self):
        self.phase = ["cleanup"]
        self.listener.event('cleanup')
        self.cleanupPhase()

    def toDict(self):
        return {"actions":self.actions,"buys":self.buys,
                "coins":self.coins}

    def startBuyPhase(self):
        self.log.append("Buy Phase")
        self.phase = "buy"
        self.promptBuy()

    def updateActions(self,num):
        self.actions += num

    def updateBuys(self, num):
        self.buys += num

    def buyCard(self, card):
        ##TODO: react to buying cards
        self.updateBuys(-1)
        self.coins -= card.cost
        self.log.append("%s bought a %s for $%d" % (self.currentPlayer, card.name, card.cost))
        self.gainCard(card)
        self.promptGain(self.coins, _type=buy)

    def gainCard(self,card):
        card = self.player.supply.gainCard(card)
        if card is None:
            return False
        self.player.discardCard(card, bu)


    def trashCard(self,card,player=None):
        if player is None:
            player = self.player
        player.hand.remove(card)
        player.supply.trashCard(card)

    def handleReactions(self,player):
        blocked = False
        reactionCards = player.getReactionCards()
        for card in reactionCards:
            if card.reaction(player):
                blocked = True
        return blocked

    def promptAction(self):
        self.promptCardFromHand("turn.playCard", kind="ActionCard", may=True)

    def promptBuy(self):
        self.promptCardFromHand('turn.playCard', kind="TreasureCard", may=True)

    def promptGain(self, cost, kind = None, player=None, _type=gain):
        if player is None:
            player = self.currentPlayer
        prompt = "Pick a card from the supply costing %d or less" % cost

        self.playerChoice[player.name] = {"type":_type,
                                          "cost":cost,
                                          "kind":str(kind),
                                          "prompt":prompt}

    def promptCardFromHand(self,callback, cost=None,kind=None,player=None,num=1, may = False, prompt = None):
        print "prompt Hand"
        if player is None:
            player = self.currentPlayer
        if prompt is None:
            if None is not kind:
                prompt = "Pick a %s card from your hand" % str(kind).lower()[:-4]
            else:
                prompt = "Pick a card from your hand"
            if cost is not None:
                prompt += " costing %d or less" % cost
        self.playerChoice[player.name] ={"type":fromHand,
                                        "kind":str(kind),
                                        "cost": cost,
                                        "callback":callback,
                                        "num":num,
                                        "may":may,
                                        "prompt":prompt}
        #print "CHOICE", self.playerChoice[player.name]

    def promptOptions(self,options,player=None):
        if player is None:
            player = self.currentPlayer
        prompt = "Pick one: "
        self.playerChoice[player.name] = {"type":"options","options":options, "prompt":prompt}


    def removePlayer(self, name):
        try:
            del self.playerChoice[name]
        except KeyError:
            pass


    def cleanupPhase(self):
        self.player.discardHand()
        self.player.discardPlayed()
        assert 0 == len(self.player.hand)
        self.player.drawHand()
        assert 5 == len(self.player.hand)
        self.player.played = []


    def playCard(self, card):
        if isinstance(card, basestring):
            card = self.player.supply.strToCard(card)

        if self.isActionPhase():
            self.playActionCard(card)
        elif self.isBuyPhase():
            self.playTreasureCard(card)
        else:
            return False

    def printAllCards(self):
        s = ""
        for player in self.otherPlayers + [self.player]:
            s += "%s\n" % player
            s += "hand\t%s\n" % (self.printSet(player.hand))
            s += "played\t%s\n" % (self.printSet(player.played))
            s +=  "discard\t%s\n" % (self.printSet(player.discard))
            s += "deck\t%s\n" % (self.printSet(player.deck.deck))
        s += ("%s" % player.supply.getPiles()) + "\n"
        print s

    def updateTurn(self, player_name):
        choice = self.playerChoice[player_name]

        if 'num' in choice and choice['num'] > 0:
            choice['num'] -= 1
        if choice['num'] == 0:
            if player_name == self.player.name:
                if self.phase == 'action':
                    if self.actions > 0 and self.player.hasActionCard():
                        self.promptAction()
                    else:
                        self.startBuyPhase()
                elif self.phase == 'buy' and self.buys > 0 :
                    self.promptBuy()
                else:
                    self.game.nextTurn()
            else:
                choice = None

    def skipChoice(self, playerName):
        self.playerChoice[playerName]['num'] = 1
        self.updateTurn(playerName)

    def playAllTreasures(self):
        treasureCards = self.player.treasuresInHand()
        for treasureCard in cards:
            self.player.hand.remove(card)
            card.play()

    def getPlayersToAttack(self):
        players = []
        for player in self.otherPlayers:
            if player.canAttack:
                players.append()
            else:
                player.canAttack = True
        return Players

    def isActionPhase(self):
        return self.phase == "action"

    def isBuyPhase(self):
        return self.phase == "buy"

    def playActionCard(self, card):
        assert self.actions > 0
        self.actions -= 1
        self.player.playCard(card,self)

    def playTreasureCard(self, card):
        self.player.playCard(card,self)

    @staticmethod # this means that it doesn't take self as a parameter. In other words it is just a vanilla function.
    def printSet(l):
        s = ''
        for i,element in enumerate(set(l)):
            s += "(%d) %s \t "% (l.count(element),element)

        return s+'\n'

    ## Function to check if string is a number
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
