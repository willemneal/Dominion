from flask import Flask
app = Flask(__name__)
from game import Game,base,playerList
from flask import render_template, session, redirect, url_for, escape, request
from random import randint
Games = {}
GAMESIZE = 1
readyPlayers = []
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/lobby',methods = ["GET","POST"])
def lobby():
    if not session['username']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        gameid = randint(0,1000)
        while gameid not in Games:
            gameid = randint(0,1000)
        session['gameid'] = gameid
        readyPlayers.append(session['username'])
        return redirect(url_for('ready'))
    return render_template("/lobby.html")

@app.route('/player/hand', methods = ['GET'])
def hand():
    name = session['username']
    G = Games[session['gameid']]
    return render_template("/hand.html",name =name, hand=G.playerDict[name].hand)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('lobby'))
    return render_template("/index.html")

@app.route('/<gameid>/player/<name>/hand')
def player(gameid,name):
    if Games[gameid]:
        return render_template('/hand.html',name =name, hand=G.playerDict[name].hand)
    return redirect(url_for('/'))

@app.route('/ready')
def ready():
    while len(readyPlayers)<GAMESIZE:
        continue
    Games[gameid] = Game(readyPlayers,[base])
    redirect(url_for('game'))
    Games[gameid].playGame()
    return redirect(url_for("game"))

@app.route('/<gameid>/supply')
def supply(gameid):
    if 'username' not in session:
        return redirect(url_for('/'))
    elif 'gameid' not in session:
        return redirect(url_for('lobby'))
    return render_template('/supply.html',  victoryCards   = G.supply.victoryCards, 
                                            treasureCards  = G.supply.treasureCards,
                                            kingdomCards   = G.supply.kingdomCards,
                                            miscCards      = G.supply.miscCards,
                                            nonSupplyCards = G.supply.nonSupplyCards)
    
@app.route('/game')
def game():
    return render_template('/game.html',)

app.secret_key = "\xf3Bg\x90\xec $xv\xee\xca`,A\"\'\x0f\\M&a\xf9\xbd\xdc"
if __name__ == '__main__':
    app.run(debug=True)