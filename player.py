from deck import Deck 
from card import Card

class Player():
    def __init__(self,name,supply):
        self.supply = supply
        self.name     = name
        self.allCardPiles = []
        self.deck     = Deck()
        self.setup()

    def setup(self):
        self.played     = []
        self.discard    = []
        self.hand       = []
        self.allCardPiles   = [self.deck.deck,
                            self.discard, 
                            self.hand]
        self.coinTokens = 0
        self.vpTokens   = 0
        self.drawHand()
        self.printHand()

	def __str__(self):
		return str(self.name)

    def numOfVictoryPoints(self):
        return sum([card.vp for card in self.getAllCards()])

    def numOfCards(self):
        res = 0
        for cards in self.allCardPiles:
            res += len(cards)
        return res

    def printHand(self):
        print self.name,":",self.hand,[card.isTreasure() for card in self.hand]

    def getAllCards(self):
        res = []
        for Set in self.allCardPiles:
            res.extend(Set)
        return res

    def discardCard(self,card):
        self.discard.append(card)

    def drawHand(self):
        self.drawCards(5)


    def discardHand(self):
        for card in self.hand:
            self.discardCard(self.hand.pop())

    def discardPlayed(self):
        for card in self.played:
           self.discardCard(self.played.pop())

    def discardDeck(self):
        card = self.deck.draw()
        while(card):
            self.discardCard(card)
            card = self.deck.draw()

    def hasAction(self):
        for card in self.hand:
            if card.isAction():
                return True
        return False

    def treasuresInHand(self):
        treasures = []
        for card in self.hand:
            if card.isTreasure():
                treasures.append(card)
        return treasures

    def coinInHand(self):
        return sum([card.coin for card in self.treasuresInHand()])


    def drawCards(self,num):
        '''
        If deck is empty the discard is shuffled
        into deck.
        '''
        for i in range(num):
            newcard = self.deck.draw()
            if (not newcard):
                self.deck.addCards(self.discard)
                self.discard=[]
                self.deck.shuffle()
                newcard = self.deck.draw()
            self.hand.append(newcard)

    def __repr__(self):
        return self.name
