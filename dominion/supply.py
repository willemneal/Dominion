from baseCards import *

class BaseSupply(object):
    def __init__(self,kingdomCards,numOfPlayers=4):
        numOfVictories =12
        if (numOfPlayers == 2):
            numOfVictories = 8
        self.numberOfPilesGone = 0
        self.supply={curse:     [curse]*30,
                    duchy:      [duchy]*numOfVictories,
                    province:   [province]*numOfVictories,
                    estate:     [estate]*numOfVictories,
                    copper:     [copper]*60,
                    silver:     [silver]*40,
                    gold:       [gold]*30
                    }
        self.victoryCards  = [estate, duchy, province]
        self.treasureCards = [copper, silver, gold]
        self.miscCards     = [curse]
        self.nonSupplyCards= []
        self.cardDict = {}


        #add in cards we are playing with.
        self.addPiles(kingdomCards)
        #print kingdomCards,"kingdomCards"
        self.kingdomCards = kingdomCards
        self.kingdomCards.sort()

        for card in self.supply:
            self.cardDict[card.name] = card
        for card in base:
            self.cardDict[card.name] = card
        self.trash = []


    def strToCard(self, card):
        #print self.cardDict
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

        dic = {"kingdomCards":[card.getAttr() for card in self.kingdomCards],
                "treasureCards":[card.getAttr() for card in self.treasureCards],
                "victoryCards":[card.getAttr() for card in self.victoryCards],
                "miscCards":[card.getAttr() for card in self.miscCards],
                "nonSupplyCards":[card.getAttr() for card in self.nonSupplyCards]}
        for card in self.supply:
            dic[card.name] = card.getAttr()
            if card not in dic["nonSupplyCards"]:
                dic[card.name]["numberLeft"] = self.cardsLeft(card)
        dic["categories"] = ["victoryCards","treasureCards",'kingdomCards',"miscCards","nonSupplyCards"]
        return dic

    def cardsLeft(self, card):
        assert isinstance(card, Card)
        card = self.strToCard(card.name)
        assert card in self.supply
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
        return  0 == self.cardsLeft(province)  or self.numberOfPilesGone == 3

    def getPiles(self):
        return sorted(self.supply.keys())

# class ProsperitySupply(BaseSupply):
#     def __init__(self,numOfPlayers=4):
#         BaseSupply.__init__(numOfPlayers)
#         BaseSupply.supply[colony]   = [colony]*numOfVictories
#         BaseSupply.supply[platinum] = [platinum]*12
