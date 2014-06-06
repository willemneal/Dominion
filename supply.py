from baseCards import *

class BaseSupply():
    def __init__(self,kingdomCards,numOfPlayers=4):

        numOfVictories =12
        if (numOfPlayers == 2):
            numOfVictories = 8
        self.numberOfPilesGone = 0
        self.supply={curse:[curse]*30,
                    duchy: [duchy]*numOfVictories,
                    province: [province]*numOfVictories,
                    estate:[estate]*numOfVictories,
                    copper:[copper]*60,
                    silver: [silver]*40,
                    gold: [gold]*30
                    }
        self.victoryCards  = [estate, duchy, province]
        self.treasureCards = [copper, silver, gold]
        self.miscCards     = [curse]
        self.nonSupplyCards= []
        self.cardDict = {}


        #add in cards we are playing with.
        self.addPiles(kingdomCards)
        self.kingdomCards = kingdomCards

        for card in self.supply:
            self.cardDict[card.name] = card
        self.trash = []
    
    def strToCard(card):
        return self.cardDict[card]
                    
    def gainCard(self,card):
        if len(self.supply[card])==0:
            print "There are no more %s cards. \n" % (card)
            return None
        if len(self.supply[card]) == 1:
            self.numberOfPilesGone += 1
        return self.supply[card].pop()

    def trashCard(self,card):
        self.trash.append(card)

    def toDict(self):
        return {"kingdomCards":[card.getAttr() for card in self.kingdomCards],
                "treasureCards":[card.getAttr() for card in self.treasureCards],
                "victoryCards":[card.getAttr() for card in self.victoryCards],
                "miscCards":[card.getAttr() for card in self.miscCards],
                "nonSupplyCards":[card.getAttr() for card in self.nonSupplyCards]}

    def cardsLeft(self,card):
        return len(self.supply[card])

    def addPiles(self,cards):
        for card in cards:
            self.supply[card] = [card]*10

    def __str__(self):
        s =''
        for card in self.getPiles():
            s+= "%s(%d$, %d left)\n" % (card,card.cost,len(self.supply[card]))
        return s[:-1]

    def gameOver(self):
        return  len(self.supply[province]) == 0 or self.numberOfPilesGone == 3

    def getPiles(self):
        return sorted(self.supply.keys())

# class ProsperitySupply(BaseSupply):
#     def __init__(self,numOfPlayers=4):
#         BaseSupply.__init__(numOfPlayers)
#         BaseSupply.supply[colony]   = [colony]*numOfVictories
#         BaseSupply.supply[platinum] = [platinum]*12
