from card import *
from gameLog import GameLog
from baseCards import feast

class Turn():
    def __init__(self, player,otherPlayers):
        self.player = player
        self.otherPlayers = otherPlayers
        self.actions = 1
        self.buys = 1
        self.coins = 5
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

    def handleReactions(self,player):
        blocked = False
        reactionCards = player.getReactionCards()
        for card in reactionCards:
            if card.reaction(player):
                blocked = True
        return blocked

    def promptCards(self,cards,kind=Card):
        s = ""
        for (i,card) in enumerate(cards):
            if i % 5 ==4:
                s += " %s-(%i)\n" % (card,i+1)
            else:
                s += " %s-(%i)" % (card,i+1)
        print s+'\n'
        cardindex = raw_input('Which Card? (0 to skip): ')
        while not is_number(cardindex):
            print "That is not a number. Try again."
            cardindex = raw_input('Which Card? (0 to skip): ')
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
        while not is_number(cardindex):
            print "That is not a number. Try again."
            cardindex = raw_input('Which Card? (0 to skip): ')
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
            self.updateActions(-1)
            
    def buyPhase(self):
        print "Buy Phase"
        numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])
        print self.hand, " is your hand Bitch"
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
            print "you bought",card
            numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])

        while self.buys > 0:
            print "%s has %d buy(s) and %d coin"%(self.player,self.buys,self.coins)
            card = self.promptGain(self.coins)
            if card is None:
                break
            if False == card:
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
        while feast in self.player.played:
            self.player.played.remove(feast)
            self.player.trashCard(feast)
        self.player.discardPlayed()
        assert 0 == len(self.player.hand)
        self.player.drawHand()
        assert 5 == len(self.player.hand)

    def promptGain(self,coinsToSpend,kind=Card):
        cards=self.player.supply.getPiles()
        s = ""
        for (i,card) in enumerate(cards):
            if i % 5 ==4:
                s += " %s-$%d,%d left(%i)\n" % (card,card.cost,self.player.supply.cardsLeft(card),i+1)
            else:
                s += " %s-$%d,%d left(%i)" % (card,card.cost,self.player.supply.cardsLeft(card),i+1)
        print s+'\n'
        while True:
            cardindex = raw_input('Which Card? (0 to skip): ')
            cardindex = int(cardindex)
            cardindex -= 1
            if cardindex < 0:
                return None
            if not isinstance(cards[cardindex],kind):
                continue
            if cards[cardindex].cost >coinsToSpend:
                return False
            return cards.pop(cardindex)

    ## Fuction to check if string is a number
    @staticmethod 
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
