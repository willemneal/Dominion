from baseCards import base, allSets
from player import Player
from supply import BaseSupply
from turn import Turn
from random import sample
from random import shuffle
import logging
from playerState import PlayerState
    
import threading
import copy

class Event(object):
    "A threading.Event that can be serialized."
    def __init__(self):
        self.evt = threading.Event()

    def set(self):
        return self.evt.set()

    def clear(self):
        return self.evt.clear()

    def isSet(self):
        return self.evt.isSet()

    def wait(self, timeout=0):
        return self.evt.wait(timeout)

    def __getstate__(self):
        d = copy.copy(self.__dict__)
        if self.evt.isSet():
            d['evt'] = True
        else:
            d['evt'] = False
        return d

    def __setstate__(self, d):
        self.evt = threading.Event()
        if d['evt']:
            self.evt.set()


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

class Game(object):
    def __init__(self, playerList,sets):
        self.log = []
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
        self.playerStates = dict()
        for player in self.players:
            self.playerDict[player.name]  = player
            self.playerStates[player.name]= PlayerState(player,self)
        self.event = Event()
        self.firstTurn()
        


        

    def firstTurn(self):
        for player in self.players:
            self.playerDict[player.name] = player
            self.playerStates[player.name] = PlayerState(player, self)
        self.round = 1
        self.currentPlayer = self.players.pop(0)
        self.firstPlayer   = self.currentPlayer
        self.log.append("Round 1")
        self.currentTurn = Turn(self.currentPlayer, self.players, self.round, self.log, self.event)
        self.event.wait()
        self.event.clear()
        self.nextTurn()

    def nextTurn(self):
        while not self.supply.gameOver():
            self.currentTurn.cleanupPhase()
            self.players.append(self.currentPlayer)
            self.currentPlayer = self.players.pop(0)
            if self.currentPlayer == self.firstPlayer:
                self.round += 1
                self.log.append("Round %d" % (self.round))
            self.currentTurn = Turn(self.currentPlayer, self.players, self.round, self.log)
            self.event.wait()
            self.event.clear()


        # while not self.supply.gameOver():
        #     self.currentPlayer = self.players.pop(0)
        #     print "It is %s's turn." % (self.currentPlayer)
        #     self.currentTurn = Turn(self.currentPlayer,self.players)
        #     self.currentTurn.actionPhase()
        #     ##logging.debug(currentTurn.printAllCards())
        #     print self.currentTurn.printAllCards()
        #     self.currentTurn.buyPhase()
        #     logging.debug(self.currentTurn.printAllCards())
        #     self.currentTurn.cleanupPhase()
        #     logging.debug(self.currentTurn.printAllCards())
        #     self.players.append(self.currentPlayer)

        # print "The game is over!! The scores are:\n"
        # winner = [0,""]
        # for player in self.players:
        #     print "%s had %d Victory Points." % (player, player.numOfVictoryPoints())
        #     if player.numOfVictoryPoints() > winner[0]:
        #         winner[0] = player.numOfVictoryPoints()
        #         winner[1] = player
        # print "And the Winner is: %s with %d Victory Points. The rest of you suck ass." %(winner[1],winner[0])



playerList = ["Max","Willem"]

#G = Game(playerList, [base])
#G.playGame()