from random import shuffle

from baseCards import *

class Deck(list):
    def __init__(self):
        for i in range(7):
            self.append(copper)
        self.extend([village, festival, chapel])
        self.shuffle()

    def addCardOnTop(self, card):
        self.insert(0, card)

    def addCards(self,cards):
        self.extend(cards)

    def draw(self):
        if (len(self) == 0):
            return False
        return self.pop(0)

    def shuffle(self):
        shuffle(self)
