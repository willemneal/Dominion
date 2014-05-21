class Turn():
    def __init__(self, player):
        self.player = player
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.hand = player.hand
        currentPlayer = player
        
        


    def updateActions(self,num):
        self.action += num
    
    def updateBuys(self, num):
        self.buys += num

    def chooseTrash(self,num,player):
        print "Choose cards to trash: \n"
        while num>0:
            cardToTrash = self.promptCards(player.hand)
            if cardToTrash:
                player.supply.trashCard(cardToTrash)
            num-=1

    def promptCards(self,cards):
        s = ""
        for (i,card) in enumerate(cards):
            s += " %s (%i)" % (card,i+1)
        print s+'\n'
        cardindex = raw_input('Which Card? (0 to skip): ')
        if cardindex.lower() == "a":
            return "all"
        cardindex = int(cardindex)
        cardindex -= 1
        if cardindex < 0:
            return None
        return cards.pop(cardindex)

    def actionPhase(self):
        print "Action Phase!"
        print self.hand,"player's hand"
        while self.actions > 0 and self.player.hasAction():
            print "Pick an action card from your hand: \n"
            card = self.promptCards(self.hand)
            if card is None:
                return
            if not card.isAction():
                print "That is not an action card. Please pick another: \n"
                continue
            card.play(self)
            self.updateActions(-1)
            
    def buyPhase(self):
        print "Buy Phase"
        numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])
        print self.hand,[card.isTreasure() for card in self.player.hand],"my hand Bitch"
        while numberOfTreasure > 0:
            print "Pick a Treasure card from your hand, or input 'all': \n"
            card = self.promptCards(self.hand)
            if card == "all":
                ##this is play all treasure option
                ## added the two necessary functions in the player object
                for card in self.player.treasuresInHand():
                    card.play(self)
                    self.hand.remove(card)
                    print card.coin, card, self.coins
                break

            if card is None:
                break
            if not card.isTreasure():
                print "That is not a Treasure card. Please pick another: \n"
                continue
            else:
                card.play(self)
            numberOfTreasure = sum([card.isTreasure() for card in self.player.hand])

        while self.buys > 0:
            if self.buys > 1:
                print "you have %d buys and %d coin"%(self.buys,self.coins)
            else:
                print "you have %d buy and %d coin"%(self.buys,self.coins)
            card = self.promptCards(self.player.supply.supply.keys())
            if card is None:
                break
            if card.cost > self.coins:
                print "Too exspensive. Need more money Bitch!!! \n"
                continue
            gainedCard  = self.player.supply.gainCard(card)
            if gainedCard is None:
                print "Please choose another. \n"
                continue
            self.player.discardCard(gainedCard)
            self.coins -= card.cost
            self.updateBuys(-1)


    def cleanupPhase(self):
        self.player.discardHand()
        self.player.discardPlayed()
        assert 0 == len(self.player.hand)
        self.player.drawHand()
        assert 5 == len(self.player.hand)





