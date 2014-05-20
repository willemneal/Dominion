from baseCards import *
from player import Player
from supply import BaseSupply
from turn import Turn
from random import sample
from random import shuffle


class Game():
    def __init__(self, playerList,sets):
        allCards = []
        print sets
        for Set in sets:
            allCards.extend(Set)

        gameCards = sample(allCards,10) ## gets 10 random cards from inluded sets
        numOfPlayers = len(playerList)
        self.supply  = BaseSupply(numOfPlayers)
        
        for card in gameCards:
            self.supply.addPile(card) 
        	## this adds the card to the supply

        self.players = [Player(name,self.supply) for name in playerList]
        shuffle(self.players)
        print self.players


    def playGame(self):
        while not self.supply.gameOver():
            currentPlayer = self.players.pop(0)
            print "It is %s's turn." % (currentPlayer)
            currentTurn = Turn(currentPlayer)
            currentTurn.actionPhase()
            currentTurn.buyPhase()
            currentTurn.cleanupPhase()
            self.players.append(currentPlayer)

        print "The game is over!! The scores are:\n"
        winner = [0,""]
        for player in self.players:
            print "%s had %d Victory Points." % (player, player.numOfVictoryPoints())
            if player.numOfVictoryPoints() > winner[0]:
                winner[0] = player.numOfVictoryPoints()
                winner[1] = player
        print "And the Winner is: %s with %d Victory Points. The rest of you suck ass." %(winner[1],winner[0])


playerList = ["Max","Willem"]

G = Game(playerList, [base])
G.playGame()