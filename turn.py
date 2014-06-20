from card import *
from baseCards import feast

class Turn(object):
    def __init__(self, player, otherPlayers, roundNumber, log):
        self.player = player
        self.otherPlayers = otherPlayers
        self.actions = 1
        self.buys = 1
        self.coins = 5
        self.hand = player.hand
        self.currentPlayer = player
        self.playerChoice={}
        self.log = log
        self.prompt = ""
        self.log.append("It is %s's turn" % self.player)
        self.playerDecision = {}
        if self.player.hasAction():
            self.log.append("Action Phase")
            self.phase = "action"
            self.playerChoice[self.player.name] = self.promptCardFromHand(kind=ActionCard)
        elif self.player.hasTreasure():
            self.log.append("Buy Phase")
            self.phase = "buy"
            self.playerChoice[self.player.name] = self.promtCardFromHand(kind=TreasureCard)
        else:
            self.endTurn()
 
    def endTurn(self):
        self.phase = ["cleanup"]
        self.cleanupPhase()

    def toDict(self):
        return {"actions":self.actions,"buys":self.buys,
                "coins":self.coins}

    def startBuyPhase(self):
        self.phase = "buy"
        self.promptCardFromHand(kind=TreasureCard)

    def updateActions(self,num):
        self.actions += num
    
    def updateBuys(self, num):
        self.buys += num

    def buyCard(self, card):
        ##TODO: react to buying cards
        self.coins -= card.cost
        self.gainCard(card)

    def gainCard(self,card):
        if self.player.supply.gainCard(card) is None:
            return False
        self.player.discardCard(card)


    def chooseTrash(self,num,player):
        print "Choose cards to trash: \n"
        while num>0:
            cardToTrash = self.promptCards(player.hand)
            if cardToTrash:
                player.supply.trashCard(cardToTrash)
            num-=1

    def handleReactions(self,player):
        blocked = False
        reactionCards = player.getReactionCards()
        for card in reactionCards:
            if card.reaction(player):
                blocked = True
        return blocked

    def promptGain(self,cost, kind = None, player=None):
        if player is None:
            player = self.currentPlayer
        prompt = "Pick a card from the supply costing less than %d" % cost

        self.playerChoice[player.name] = {"choice":{"type":"gain",
                                                    "gain":{"cost":cost, "kind":str(kind)}},
                                          "prompt":prompt}

    def promptCardFromHand(self,cost=None,kind=None,player=None):
        if player is None:
            player = self.currentPlayer
        if None is not kind:
            prompt = "Pick a %s card from your hand" % str(kind).lower()[:-4]
        else:
            prompt = "Pick a card from your hand"
        if cost is not None:
            prompt += " costing %d or less" % cost 
        self.playerChoice[player.name] =\
            {"choice":{"type":"fromHand","fromHand":{"kind":str(kind),
                        "cost": cost}},
             "promt":prompt} 

    def promptOptions(self,options,player=None):
        if player is None:
            player = self.currentPlayer
        prompt = "Pick one: "
        self.playerChoice[player.name] = {"choice":{"type":"options","options":options}, "prompt":prompt}


    def removePlayer(self, name):
        try:
            del self.playerChoice[name]
        except KeyError:
            pass

    # def promptCards(self,cards,kind=Card):
    #     s = ""
    #     for (i,card) in enumerate(cards):
    #         if i % 5 ==4:
    #             s += " %s-(%i)\n" % (card,i+1)
    #         else:
    #             s += " %s-(%i)" % (card,i+1)
    #     print s+'\n'
    #     cardindex = raw_input('Which Card? (0 to skip): ')
    #     print cardindex, "cardindex",self.is_number(cardindex)
    #     if TreasureCard == kind:
    #         if (cardindex.lower() == "a" or cardindex.lower()=="all"):
    #             return "all"
    #     while not self.is_number(cardindex):
    #         print "That is not a number. Try again."
    #         cardindex = raw_input('Which Card? (0 to skip): ')
    #     while int(cardindex) >= len(cards):
    #         print "That is out of range. Try again."
    #         cardindex = raw_input('Which Card? (0 to skip): ')
    #     cardindex = int(cardindex)
    #     cardindex -= 1
    #     if cardindex < 0:
    #         return None
    #     if not isinstance(cards[cardindex],kind):
    #         return False
    #     return cards.pop(cardindex)

    # def promptCardsIndex(self,cards,kind=Card):
    #     s = ""
    #     for (i,card) in enumerate(cards):
    #         if i % 5 ==4:
    #             s += " %s-(%i)\n" % (card,i+1)
    #         else:
    #             s += " %s-(%i)" % (card,i+1)
    #     print s+'\n'
    #     cardindex = raw_input('Which Card? (0 to skip): ')
    #     while not self.is_number(cardindex):
    #         print "That is not a number. Try again."
    #         cardindex = raw_input('Which Card? (0 to skip): ')
    #     cardindex = int(cardindex)
    #     cardindex -= 1
    #     if cardindex < 0:
    #         return None
    #     if not isinstance(cards[cardindex],kind):
    #         return False
    #     return cardindex

    # def actionPhase(self):
    #     print "Action Phase!"
    #     while self.actions > 0 and self.player.hasAction():
    #         print "Actions:",self.actions,"\nPick an action card from your hand: \n"
    #         card = self.promptCards(self.hand,ActionCard)
    #         if card is None:
    #             return
    #         if not card: ## promptCards returns false if not an action card
    #             print "That is not an action card. Please pick another: \n"
    #             continue
    #         card.play(self)
    #         self.updateActions(-1)
            
    # def buyPhase(self):
    #     print "Buy Phase"
    #     numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])
    #     while numberOfTreasure > 0:
    #         print "Pick a Treasure card from your hand, or input 'all': \n"
    #         card = self.promptCards(self.hand,TreasureCard)
    #         if card == "all":
    #             ##this is play all treasure option
    #             ## added the two necessary functions in the player object
    #             for card in self.player.treasuresInHand():
    #                 card.play(self)
    #                 self.hand.remove(card)
    #                 self.player.played.append(card)
    #                 print card.coin, card, self.coins
    #             break

    #         if card is None:
    #             break
    #         if not card: ##promptCards returns false if not a treasure
    #             print "That is not a Treasure card. Please pick another: \n"
    #             continue
    #         card.play(self)
    #         self.player.played.append(card)
    #         print "you bought",card
    #         numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])

    #     while self.buys > 0 and self.coins > 0:
    #         print "%s has %d buy(s) and %d coin"%(self.player,self.buys,self.coins)
    #         card = self.promptGain(self.coins)
    #         if card is None:
    #             break
    #         gainedCard  = self.player.supply.gainCard(card)
    #         if gainedCard is None:
    #             print "Please choose another. \n"
    #             continue
    #         self.player.discardCard(gainedCard)
    #         self.coins -= card.cost
    #         self.updateBuys(-1)
    #         print "%s bought a %s" % (self.player, card)


    def cleanupPhase(self):
        self.player.discardHand()
        self.player.discardPlayed()
        assert 0 == len(self.player.hand)
        self.player.drawHand()
        assert 5 == len(self.player.hand)
        self.player.played = []

    # def promptGain(self,coinsToSpend,kind=Card):
    #     cards=self.player.supply.getPiles()
    #     s = ""
    #     for (i,card) in enumerate(cards):
    #         if i % 2 ==0:
    #             s += "(%i) $%d, %d -%s\t\t" % (i+1,
    #                                             card.cost,
    #                                             self.player.supply.cardsLeft(card),
    #                                             card)
    #         else:
    #             s += "(%i) $%d, %d -%s\n" % (i+1,card.cost,self.player.supply.cardsLeft(card),card)
    #     print s+'\n'
    #     while True:
    #         cardindex = raw_input('Pick a card %d or less (0 to skip): '%( coinsToSpend))
    #         cardindex = int(cardindex)
    #         cardindex -= 1
    #         if cardindex < 0:
    #             return None
    #         if not isinstance(cards[cardindex],kind):
    #             continue
    #         if cards[cardindex].cost >coinsToSpend:
    #             return False
    #         return cards.pop(cardindex)
    
    def playCard(self,card):
        if isinstance(card, basestring):
            card = self.player.supply.strToCard(card)
        self.player.hand.remove(card)
        self.player.played.append(card)
        card.play(self)
        self.updateActions(-1)

    def printAllCards(self):
        s = ""
        for player in self.otherPlayers + [self.player]:
            s += "%s\n" % player
            s += "hand\t%s\n" % (self.printSet(player.hand))
            s += "played\t%s\n" % (self.printSet(player.played))
            s +=  "discard\t%s\n" % (self.printSet(player.discard))
            s += "deck\t%s\n" % (self.printSet(player.deck.deck))
        s += ("%s" % player.supply.getPiles()) + "\n"

    @staticmethod #this means that it doesn't take self as a parameter. In other words it is just a vanilia function.
    def printSet(List):
        s = ''
        for i,element in enumerate(set(List)):
            s += "(%d) %s \t "% (List.count(element),element)

        return s+'\n'

    ## Fuction to check if string is a number
    @staticmethod 
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
