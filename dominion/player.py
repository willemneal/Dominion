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
        self.prompt = ''
        self.canAttack = True

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

    def discardFromHand(self, card):
        assert card in self.hand
        self.discardCard(card)
        self.removeListener(card)
        self.hand.remove(card)

    def discardHand(self):
        map(lambda card: self.discardFromHand(card),self.hand)


    def discardList(self,pile):
        self.discard.extend(pile)
        pile = []

    def discardPlayed(self):
        self.discardList(self.played)

    def drawCard(self):
        card = self.deck.draw()
        if not card:
            self.deck.addCards(self.discard)
            self.discard=[]
            self.deck.shuffle()
            card = self.deck.draw()
        if not card:
            return False
        return card



    def drawCards(self,num):
        '''
        If deck is empty the discard is shuffled
        into deck.
        '''
        drawnCards = []
        for i in range(num):
            card = self.drawCard()
            if not card:
                return drawCards
            drawnCards.append(card)
        return drawnCards

    def drawHand(self):
        assert 0 == len(self.hand)
        self.drawToHand(5)

    def playCard(self,card, turn):
        assert card in self.hand
        self.hand.remove(card)
        self - card
        card.play(turn)

    def drawToHand(self,num):
        cards = self.drawCards(num)
        self.mergeGameObjects(cards)
        self.hand.extend(cards)

    def getAllCards(self):
        return [card for Set in self.allCards for card in Set]

    def hasActionCard(self):
        return len([card for card in self.hand if card.isAction()]) > 0

    def hasTreasureCard(self):
        return len(self.treasuresInHand()) > 0

    def gainCard(self,card):
        self.discardCard(card)

    def getReactionCards(self):
        return [card for card in self.hand if card.isReaction()]


    def minimalHand(self):
        hand = set(self.hand)
        return [(card, self.hand.count(card)) for card in hand]


    def numOfCards(self):
        return sum([len(cards) for cards in self.allCards])

    def numOfVictoryPoints(self):
        return sum([card.vp for card in self.getAllCards()])

    def printDiscard(self):
        print len(self.discard),self.discard

    def printHand(self):
        print self.name,":",self.hand,[card.isTreasure() for card in self.hand]

    def printPlayed(self):
        print len(self.played),self.played

    def setUpdate(self, Bool):
        self.update = Bool


    def trashCard(self,card):
        self.supply.trashCard(card)
        self.event('trash',card)

    def trashCardFromHand(self,card):
        assert card in self.hand
        self.hand.remove(card)
        self.trashCard(card)

    def treasuresInHand(self):
        return [card for card in self.hand if card.isTreasure()]
