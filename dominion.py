from flask import Flask
app = Flask(__name__)
from game import Game,base,playerList
from flask import render_template, session, redirect, url_for, escape, request, jsonify
from random import randint
import thread, json

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
        print "lobbypost"
        gameid = randint(0,1000)
        while gameid in Games:
            gameid = randint(0,1000)
        print 'ready/'+str(gameid)
        session['gameid'] = gameid
        readyPlayers.append(session['username'])
        ## change this later
        Games[gameid] = Game(readyPlayers,[base])
        print Games
        thread.start_new_thread(Games[gameid].playGame,())
        print Games
        return redirect(url_for("game",gameid=gameid))
        #print  "redirect Bitches"
        #return redirect(url_for('ready'))
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
    return render_template("/login.html")

@app.route('/hand/<int:gameid>')
def player(gameid):
    if Games[gameid]:
        G = Games[gameid]
        name = session['username']
        #return render_template('/hand.html',name =name, hand=G.playerDict[name].hand)
        return json.dumps([card.getAttr() for card in G.playerDict[name].hand])    
    return redirect(url_for('/'))

@app.route('/ready/<gameid>')
def ready():
    Games[gameid] = Game(readyPlayers,[base])
    Games[gameid].playGame()
    return redirect(url_for("game",gameid=gameid))

@app.route('/supply/<int:gameid>')
def supply(gameid):
    supply = Games[gameid].supply
    return jsonify(supply.toDict())
    return render_template('/supply.html', game = Games[gameid])

@app.route('/game')
@app.route('/game/<int:gameid>', methods=['GET','POST'])
def game(gameid=None):
    print "hello"
    if gameid is None:
        gameid = session['gameid']
    g = Games[gameid]
    print gameid,"about to render_template"
    print '/static/pages/game.html'
    return app.send_static_file('pages/game.html')
    return render_template('/game.html',game=Games[gameid])


@app.route('/play/<card>/<int:gameid>',methods=['GET','POST'])
def playCard(gameid,card):
    if request.method == 'POST':
        card = card.lower()
        player = Games[gameid].playerDict[session['username']]
        if player is not Games[gameid].currentPlayer:
            return "Not your Turn"
        Games[gameid].currentTurn.playCard(card)
        return json.dumps([card.getAttr() for card in player.hand])

@app.route('/discard/<card>/<int:gameid>',methods=['GET','POST'])
def discard(gameid,card):
    if request.method == 'POST':
        player = Games[gameid].playerDict[session['username']]
        if player is not Games[gameid].currentPlayer:
            return "Not your Turn"
        card = Games[gameid].currentTurn.strToCard(card)
        player.discardCard(card)
        return json.dumps([card.getAttr() for card in player.hand])

app.secret_key = "\xf3Bg\x90\xec $xv\xee\xca`,A\"\'\x0f\\M&a\xf9\xbd\xdc"
if __name__ == '__main__':
    app.run(debug=True)