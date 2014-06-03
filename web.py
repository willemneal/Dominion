from flask import Flask
app = Flask(__name__)
from game import Game,base,playerList
from flask import render_template

Games = {}
@app.route('/')
def index():
    Games[1] = Game(playerList,[base])
    return 'Game Has Started'

@app.route('/<gameid>/player/<name>/hand')
def player(gameid,name):
    if Games[gameid]:
        return render_template('/hand.html',name =name, hand=G.playerDict[name].hand)
    return redirect(url_for('/'))
@app.route('/<gameid>/supply')
def supply(gameid):
    if Games[gameid]:
       return render_template('/supply.html',  victoryCards   = G.supply.victoryCards, 
                                               treasureCards  = G.supply.treasureCards,
                                               kingdomCards   = G.supply.kingdomCards,
                                               miscCards      = G.supply.miscCards,
                                               nonSupplyCards = G.supply.nonSupplyCards)
    return redirect(url_for('/'))

if __name__ == '__main__':
    app.run(debug=True)