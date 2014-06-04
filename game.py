from baseCards import base
from player import Player
from supply import BaseSupply
from turn import Turn
from random import sample
from random import shuffle
import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
##logging.debug('This message should go to the log file')

"""
def reloadAll():
    
    reload(turn)
    reload(baseCards)
    reload(card)
    reload(player)
    reload(supply)

reloadAll()
"""

class Game():
    def __init__(self, playerList,sets):
        allCards = []
        for Set in sets:
            allCards.extend(Set)
        gameCards = sample(allCards,10) ## gets 10 random cards from inluded sets
        numOfPlayers = len(playerList)
        self.supply  = BaseSupply(gameCards,numOfPlayers)
        print self.supply
        self.players = [Player(name,self.supply) for name in playerList]
        shuffle(self.players)

        self.playerDict = dict()
        for player in self.players:
            self.playerDict[player.name] = player

        

    def playGame(self):


        while not self.supply.gameOver():
            self.currentPlayer = self.players.pop(0)
            print "It is %s's turn." % (self.currentPlayer)
            currentTurn = Turn(self.currentPlayer,self.players)
            currentTurn.actionPhase()
            ##logging.debug(currentTurn.printAllCards())
            print currentTurn.printAllCards()
            currentTurn.buyPhase()
            logging.debug(currentTurn.printAllCards())
            currentTurn.cleanupPhase()
            logging.debug(currentTurn.printAllCards())
            self.players.append(self.currentPlayer)

        print "The game is over!! The scores are:\n"
        winner = [0,""]
        for player in self.players:
            print "%s had %d Victory Points." % (player, player.numOfVictoryPoints())
            if player.numOfVictoryPoints() > winner[0]:
                winner[0] = player.numOfVictoryPoints()
                winner[1] = player
        print "And the Winner is: %s with %d Victory Points. The rest of you suck ass." %(winner[1],winner[0])


playerList = ["Max","Willem"]

#G = Game(playerList, [base])
#G.playGame()