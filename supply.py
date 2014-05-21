from baseCards import *

class BaseSupply():
    def __init__(self,numOfPlayers=4):
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
        self.trash = []
    
                    
    def gainCard(self,card):
        if len(self.supply[card])==0:
            print "There are no more %s cards. \n" % (card)
            return None
        if len(self.supply[card]) == 1:
            self.numberOfPilesGone += 1
        return self.supply[card].pop()

    def trashCard(self,card):
        self.trash.append(card)

    def addPile(self,card):
        self.supply[card] = [card]*10

    def __str__(self):
        s =''
        for card in self.supply:
            s+= "%s(%d$, %d left)\n" % (card,len(self.supply[card]),card.cost)
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
