from deck import Deck 
from card import Card

class Player():
    def __init__(self,name,supply):
        self.supply = supply
        self.name     = name
        self.deck       = Deck()
        self.played     = []
        self.discard    = []
        self.hand       = []
        self.allCards   = [self.deck.deck,
                            self.played,
                            self.discard, 
                            self.hand]
        self.coinTokens = 0
        self.vpTokens   = 0
        self.drawHand()

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name) 

    def coinInHand(self):
        return sum([card.coin for 
                        card in self.treasuresInHand()])

    def discardCard(self,card):
        self.discard.append(card)

    def discardDeck(self):
        self.discardList(self.played)

    def discardHand(self):
        self.discard.extend(self.hand)
        self.hand = []

    def discardList(self,pile):
        self.discard.extend(pile)
        pile = []

    def discardPlayed(self):
        self.discardList(self.played)

    def drawCard(self):
        return self.drawCards(1)[0]

    def drawCards(self,num):
        '''
        If deck is empty the discard is shuffled
        into deck.
        '''
        drawnCards = []
        for i in range(num):
            newcard = self.deck.draw()
            if (not newcard):
                self.deck.addCards(self.discard)
                self.discard=[]
                self.deck.shuffle()
                newcard = self.deck.draw()
            drawnCards.append(newcard)
        return drawnCards

    def drawHand(self):
        assert 0 == len(self.hand)
        self.drawToHand(5)

    def drawToHand(self,num):
        self.hand.extend(self.drawCards(num))

    def getAllCards(self):
        res = []
        for Set in self.allCards:
            res.extend(Set)
        return res         

    def hasAction(self):
        for card in self.hand:
            if card.isAction():
                return True
        return False  

    def getReactionCards(self):
        reactionCards = []
        for card in self.hand:
            if card.isAction():
                if card.isReaction:
                    reactionCards.append(card)
        return reactionCards


    def minimalHand(self):
        hand = set(self.hand)
        hand = list(hand)

    def numOfCards(self):
        res = 0
        for cards in self.allCards:
            res += len(cards)
        return res

    def numOfVictoryPoints(self):
        return sum([card.vp for card in self.getAllCards()])

    def printDiscard(self):
        print len(self.discard),self.discard

    def printHand(self):
        print self.name,":",self.hand,[card.isTreasure() for card in self.hand]

    def printPlayed(self):
        print len(self.played),self.played

    def trashCard(self,card):
        self.supply.trashCard(card)

    def treasuresInHand(self):
        treasures = []
        for card in self.hand:
            if card.isTreasure():
                treasures.append(card)
        return treasures
