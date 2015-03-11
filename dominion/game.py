from baseCards import base, allSets
from player import Player
from supply import BaseSupply
from turn import Turn
from random import sample
from random import shuffle
import logging
from playerState import PlayerState


##logging.debug('This message should go to the log file')



class Game(object):
    def __init__(self, playerList, sets):
        self.log = []
        allCards = []
        for Set in sets:
            allCards.extend(Set)
        gameCards = sample(allCards,10) ## gets 10 random cards from inluded sets
        numOfPlayers = len(playerList)
        self.supply  = BaseSupply(gameCards,numOfPlayers)
        #print self.supply
        self.players = [Player(name,self.supply) for name in playerList]
        shuffle(self.players)
        self.playerDict = dict()
        self.playerStates = dict()
        for player in self.players:
            self.playerDict[player.name]  = player
            self.playerStates[player.name]= PlayerState(player,self)
        self.firstTurn()

    def firstTurn(self):
        for player in self.players:
            self.playerDict[player.name] = player
            self.playerStates[player.name] = PlayerState(player, self)
        self.round = 1
        self.currentPlayer = self.players.pop(0)
        self.firstPlayer   = self.currentPlayer
        self.log.append("Round 1")
        self.currentTurn = Turn(self.currentPlayer, self.players, self.round, self.log, self)

    def nextTurn(self):
        self.currentTurn.cleanupPhase()
        if self.supply.gameOver():
            self.log.append("The Game is Over!!")
            self.determineWinner()

        self.players.append(self.currentPlayer)
        self.currentPlayer = self.players.pop(0)
        if self.currentPlayer == self.firstPlayer:
            self.round += 1
            self.log.append("Round %d" % (self.round))
        self.currentTurn = Turn(self.currentPlayer, self.players, self.round, self.log, self)


    def determineWinner(self):
        winner = (None, 0)
        for player in self.players:
            vp = player.numOfVictoryPoints()
            if vp > winner[1]:
                winner = ([player], vp)
            elif vp == winner[1]:
                if winner[0]:
                    winner = (winner[1].append(player),winner[1])
                else:
                    winner = ([player], vp)
        winners = ''

        for player in winner[0]:
            if player == winner[0][-1]:
                winners += player
            else:
                winners += player + " and "
        self.log.append("%s Just won with %d Victory Points" % (winners, winner[1]))
        for player in self.players:
            if player not in winner[0]:
                self.log.append("%s scored %d Victory Points" % (player.name, player.numOfVictoryPoints()))


#
# playerList = ["Max","Willem"]
#
# G = Game(playerList, [base])
