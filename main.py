from flask import Flask, Response, stream_with_context
import dominion
from dominion.database import *
from dominion.game import Game, base, allSets
from flask import render_template, session, redirect, url_for, request, jsonify
import thread


from hashlib import md5

import json, pdb
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect


app.secret_key = "\xf3Bg\x90\xec $xv\xee\xca`,A\"\'\x0f\\M&a\xf9\xbd\xdc"
app.config['DEBUG']= True
socketio = SocketIO(app)

def hashPassword(password, salt):
    return md5(password + salt).hexdigest()





@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return redirect(url_for('login'))


@app.route('/gain/<cardName>/<int:gameid>', methods=["POST"])
def gain(cardName, gameid):
    game = getCurrentGame(gameid)
    player = game.playerDict[session['username']]
    if player != game.currentPlayer:
        return "Not Current Player"
    card = game.supply.strToCard(cardName)
    game.currentTurn.gainCard(card)
    game.log.append("%s gained a %s" % (player.name, card.name))
    updateGame(gameid, game)


@app.route('/buy/<card>/<int:gameid>', methods=["POST"])
def buy(card, gameid):
    game = getCurrentGame(gameid)
    card = game.supply.strToCard(card)
    turn = game.currentTurn
    if turn.coins < card.cost:
        return "that card is too expensive"
    turn.buyCard(card)
    updateGame(gameid, game)
    return "%s bought a %s for $%d" % (turn.currentPlayer, card.name, card.cost)


@app.route('/buyPhase/<int:gameid>', methods=["POST"])
def buyPhase(gameid):
    game = getCurrentGame(gameid)
    game.currentTurn.startBuyPhase()
    updateGame(gameid, game)
    return "yay!yay!yay!yay!"


@app.route('/lobby', methods=["GET", "POST"])
def lobby():
    if 'username' not in session:
        return redirect(url_for('login'))
    games = getPendingGames()
    if request.method == 'POST':
        if "pending" in request.form and request.form['pending'] == 'See Pending Games':
            if len(games) == 0:
                return redirect(url_for('lobby', _method="GET"))
            return render_template("/lobby.html", pending=True, games=games)

        if "newGame" in request.form and request.form['newGame'] == "Create Game":
            print "creation"
            return render_template("/lobby.html", newGame=True, sets=[{"name": Set} for Set in allSets])
        if 'liveGames' in request.form:
            games = getLiveGames()
            print "games---", games
            return render_template('/lobby.html', liveGames=True, games=games)

        return redirect(url_for("game", gameid= gameid))
        # print  "redirect Bitches"
        #return redirect(url_for('ready'))
    return render_template("/lobby.html", welcome=True, numPending=len(games))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not getUserID(username):
            return render_template("/login.html", usernameWrong=True)

        if hashPassword(password, username[-2:]) != getPassword(username):
            return render_template('/login.html', passwordWrong=True)
        session['username'] = request.form['username']
        # print session['username']
        if request.form.has_key('remember_me') and request.form['remember_me'] == "on":
            session.permanent = True
        return redirect(url_for('lobby'))
    return render_template("/login.html")
    return redirect(url_for('lobby'))


@app.route('/hand/<int:gameid>')
def player(gameid):
    G = getCurrentGame(gameid)
    if G:
        name = session['username']
        # return render_template('/hand.html',name =name, hand=G.playerDict[name].hand)
        return json.dumps([card.getAttr() for card in G.playerDict[str(name)].hand])
    return redirect(url_for('/'))


@app.route('/ready/<gameid>', methods=["GET", "POST"])
def ready(gameid):
    if request.method == "POST":
        if request.form.has_key("join"):
            print "join"
            joinGame(gameid, session['username'])
            return redirect(url_for('lobby'))
        elif request.form.has_key("start"):
            startGame(gameid)
            return redirect(url_for("game", gameid=gameid))
    Flask.abort(301)


@app.route('/supply/<int:gameid>')
def supply(gameid):
    game = getCurrentGame(gameid)
    if not game:
        return Flask.abort(401)
    supply = game.supply
    print jsonify(supply.toDict())
    return jsonify(supply.toDict())


@app.route('/game')
@app.route('/game/<int:gameid>', methods=['GET', 'POST'])
def game(gameid=None):
    if gameid is None:
        gameid = session['gameid']
    print '/static/pages/game.html'
    return app.send_static_file('pages/game.html')
    return render_template('/game.html', game=Games[gameid])


@app.route('/play/treasures/<int:gameid>', methods=['POST'])
def playTreasures(gameid):
    game = getCurrentGame(gameid)
    game.currentTurn.playAllTreasures()
    updateGame(gameid, game)


@app.route('/play/<string:card>/<int:gameid>', methods=["POST"])
def play(card, gameid):
    #pdb.set_trace()
    #print type(card), card
    game = getCurrentGame(gameid)
    card = game.supply.strToCard(str(card))
    turn = game.currentTurn
    print request.values.has_key('callback')
    if not request.values.has_key('callback'):
        return "No callback given"
    func = eval(request.values['callback'])
    res = func(card)
    if res is None:
        turn.updateTurn(session['username'])
    print "played %s" % card.name
    updateGame(gameid, game)
    return "%s was played" % (card.name)


@app.route('/skip/<int:gameid>', methods=['POST'])
def skipChoice(gameid):
    game = getCurrentGame(gameid)
    choice = game.currentTurn.playerChoice[session['username']]
    if choice['may']:
        game.currentTurn.skipChoice(session['username'])
    updateGame(gameid, game)
    return "attempted skip"


@app.route('/endTurn/<int:gameid>', methods=["POST"])
def endTurn(gameid):
    #pdb.set_trace()
    game = getCurrentGame(gameid)
    game.nextTurn()
    updateGame(gameid, game)
    return "it's %s's turn" % (game.currentPlayer)


# @app.route('/play/<card>/<int:gameid>',methods=['GET','POST'])
# def playCard(gameid,card):
# if request.method == 'POST':
#         game = getCurrentGame(gameid)
#         card = game.supply.strToCard(card)
#         player = game.playerDict[session['username']]
#         if player is not game.currentPlayer:
#             return "Not your Turn"
#         game.currentTurn.playCard(card)
#         updateGame(gameid, game)
#         return json.dumps([card.getAttr() for card in player.hand])

@app.route('/discard/<card>/<int:gameid>', methods=['GET', 'POST'])
def discard(gameid, card):
    if request.method == 'POST':
        game = getCurrentGame(gameid)
        player = game.playerDict[session['username']]
        if player is not game.currentPlayer:
            return "Not your Turn"
        card = game.currentTurn.strToCard(card)
        player.discardCard(card)
        return json.dumps([card.getAttr() for card in player.hand])


@app.route('/state/<int:gameid>', methods=["GET", "POST"])
def state(gameid):
    game = getCurrentGame(gameid)
    player = game.playerDict[session['username']]
    turn = game.currentTurn

    if request.method == "POST":
        return json.dumps(getState(gameid, player.name))

        # if player.update:
        #     player.setUpdate(False)
        #     print player.update, "now False"
        #     updateGame(gameid, game)
        #     return json.dumps(game.playerStates[player.name].getState())
        # while player.name not in turn.playerChoice or player.update is False:
        #     continue
        # state = game.playerStates[player.name].getState()
        # turn.removePlayer(player.name)
        # for key in state:
        #     print key, state[key]
        #     print ""

        # updateGame(gameid, game)
        # return json.dumps(state)


@app.route('/choice/<option>/<int:gameid>')
def choice(option, gameid):
    game = getCurrentGame(gameid)
    turn = game.currentTurn
    turn.playerDecision[session['username']] = option
    updateGame(gameid, game)


@app.route('/games/pending')
def pending():
    return json.dumps(getPendingGames())


@app.route('/games/live')
def gamesInProgress():
    return json.dumps(getLiveGames())


@app.route('/new/Game', methods=['GET', 'POST'])
def newGame():
    if request.method == "POST":
        sets = []
        for Set in allSets:
            if Set in request.form:
                sets.append(Set)
        username = session['username']
        createPendingGame(username, sets, request.form['numberOfPlayers'])
        return redirect(url_for('lobby', _method="POST", pending="See Pending Games"))
    else:
        Flask.abort(304)


@app.route('/new/User', methods=['GET', 'POST'])
def newUser():
    if request.method == "POST":
        if getUserID(request.form['username']):
            return render_template('/newuser.html', user=True)
        #print "here111"
        if request.form['password'] != request.form['password2']:
            return render_template('/newuser.html', password=True)

        createUser(username=request.form['username'],
                   password=hashPassword(request.form['password'],
                                         request.form['username'][-2:]),
                   firstName=request.form['firstName'],
                   lastName=request.form['lastName'])
        return redirect(url_for('lobby'))
    else:
        return render_template('/newuser.html')


@app.route('/log/<int:gameid>')
def getLog(gameid):
    game = getCurrentGame(gameid)
    return json.dumps(game.log)


'''
The following is for pushing state to the user.

'''
@socketio.on('join', namespace='/update')
def join(message):
    join_room(message['room'])
    print "joined",message['room'],"room", type(message['room'])
    emit('message',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms)})

@socketio.on('Game Event', namespace='/update')
def game_update(message):
    print "game Event", int(message['room'])
    emit('getState',
         {'room': message['room']},
          room=message['room'])

@socketio.on('getUpdate', namespace='/update')
def room_update(message):
    print type(message['room']),
    state = getState(int(message['room']),session['username'])
    print session['username']
    #print state
    emit('state',
         {'room': message['room'],
         'state': state})

@app.route('/update/<int:gameid>', methods=['GET'])
def post(gameid):
    players = getPlayers(gameid)
    for player in players:
        print "player in update!", player, session['username']
        state = getState(gameid, player)
        thread.start_new_thread(red.publish, (player, "%s" % state))
    return Response(status=204)




if __name__ == '__main__':
    socketio.run(app,port=80)
