from flask import Flask
app = Flask(__name__)
from game import Game,base,playerList
from flask import render_template

@app.route('/')
def index():
    global G
    G = Game(playerList,[base])
    return 'Game Has Started'

@app.route('/player/<name>/hand')
def player(name):
    global G
    return render_template('/hand.html',name =name, hand=G.playerDict[name].hand)

@app.route('/supply')
def supply():
	global G
	return render_template('/supply.html', victoryCards = G.supply.victoryCards, 
										   treasureCards= G.supply.treasureCards,
										   kingdomCards=  G.supply.kingdomCards,
										   miscCards=     G.supply.miscCards,
										   nonSupplyCards=G.supply.nonSupplyCards)

if __name__ == '__main__':
    app.run(debug=True)