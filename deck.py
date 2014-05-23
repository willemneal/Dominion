from random import shuffle

from baseCards import *

class Deck(object):
    def __init__(self):
        self.deck = []
        for i in range(7):
            self.deck.append(copper)
        for i in range(3):
            self.deck.append(estate)
        self.shuffle()

    def addCardOnTop(self, card):
        self.deck.insert(0, card)

    def addCards(self,cards):
        self.deck.extend(cards)


    def draw(self):
        if (len(self.deck) == 0): 
            return False
        return self.deck.pop(0)

    def shuffle(self):
        shuffle(self.deck)