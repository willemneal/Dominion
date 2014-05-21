from card import *

class Turn():
    def __init__(self, player,otherPlayers):
        self.player = player
        self.otherPlayers = otherPlayers
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.hand = player.hand
        currentPlayer = player
        
        


    def updateActions(self,num):
        self.actions += num
    
    def updateBuys(self, num):
        self.buys += num

    def chooseTrash(self,num,player):
        print "Choose cards to trash: \n"
        while num>0:
            cardToTrash = self.promptCards(player.hand)
            if cardToTrash:
                player.supply.trashCard(cardToTrash)
            num-=1


    def promptCards(self,cards,kind=Card):
        s = ""
        for (i,card) in enumerate(cards):
            if i % 5 ==4:
                s += " %s-(%i)\n" % (card,i+1)
            else:
                s += " %s-(%i)" % (card,i+1)
        print s+'\n'
        cardindex = raw_input('Which Card? (0 to skip): ')
        if cardindex.lower() == "a" or cardindex.lower() == "all":
            return "all"
        cardindex = int(cardindex)
        cardindex -= 1
        if cardindex < 0:
            return None
        if not isinstance(cards[cardindex],kind):
            return False
        return cards.pop(cardindex)

    def promptCardsIndex(self,cards,kind=Card):
        s = ""
        for (i,card) in enumerate(cards):
            if i % 5 ==4:
                s += " %s-(%i)\n" % (card,i+1)
            else:
                s += " %s-(%i)" % (card,i+1)
        print s+'\n'
        cardindex = raw_input('Which Card? (0 to skip): ')
        if cardindex.lower() == "a" or cardindex.lower() == "all":
            return "all"
        cardindex = int(cardindex)
        cardindex -= 1
        if cardindex < 0:
            return None
        if not isinstance(cards[cardindex],kind):
            return False
        return cardindex

    def actionPhase(self):
        print "Action Phase!"
        print self.hand,"player's hand"
        while self.actions > 0 and self.player.hasAction():
            print "Actions:",self.actions,"Pick an action card from your hand: \n"
            card = self.promptCards(self.hand,ActionCard)
            if card is None:
                return
            if not card: ## promptCards returns false if not an action card
                print "That is not an action card. Please pick another: \n"
                continue
            card.play(self)
            self.player.played.append(card)
            self.updateActions(-1)
            
    def buyPhase(self):
        print "Buy Phase"
        numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])
        print self.hand,[card.isTreasure() for card in self.player.hand],"my hand Bitch"
        while numberOfTreasure > 0:
            print "Pick a Treasure card from your hand, or input 'all': \n"
            card = self.promptCards(self.hand,TreasureCard)
            if card == "all":
                ##this is play all treasure option
                ## added the two necessary functions in the player object
                for card in self.player.treasuresInHand():
                    card.play(self)
                    self.hand.remove(card)
                    self.player.played.append(card)
                    print card.coin, card, self.coins
                break

            if card is None:
                break
            if not card: ##promptCards returns false if not a treasure
                print "That is not a Treasure card. Please pick another: \n"
                continue
            else:
                card.play(self)
                self.player.played.append(card)
            numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])

        while self.buys > 0:
            if self.buys > 1:
                print "you have %d buys and %d coin"%(self.buys,self.coins)
            else:
                print "you have %d buy and %d coin"%(self.buys,self.coins)
            card = self.promptBuy(self.player.supply.getPiles())
            if card is None:
                break
            if card.cost > self.coins:
                print "Too exspensive. Need more money Bitch!!! \n"
                continue
            gainedCard  = self.player.supply.gainCard(card)
            if gainedCard is None:
                print "Please choose another. \n"
                continue
            self.player.discardCard(gainedCard)
            self.coins -= card.cost
            self.updateBuys(-1)


    def cleanupPhase(self):
        self.player.discardHand()
        self.player.discardPlayed()
        assert 0 == len(self.player.hand)
        self.player.drawHand()
        assert 5 == len(self.player.hand)

    def promptBuy(self,cards,kind=Card):
        s = ""
        for (i,card) in enumerate(cards):
            if i % 5 ==4:
                s += " %s-$%d,%d left(%i)\n" % (card,card.cost,turn.player.supply.cardsLeft(),i+1)
            else:
                s += " %s-$%d,%d left(%i)" % (card,card.cost,turn.player.supply.cardsLeft(),i+1)
        print s+'\n'
        cardindex = raw_input('Which Card? (0 to skip): ')
        if cardindex.lower() == "a" or cardindex.lower()=="all":
            return "all"
        cardindex = int(cardindex)
        cardindex -= 1
        if cardindex < 0:
            return None
        if not isinstance(cards[cardindex],kind):
            return False
        return cards.pop(cardindex)








