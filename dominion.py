from flask import Flask, Response, stream_with_context
import pickle
from game import Game,base,playerList,allSets
from flask import render_template, session, redirect, url_for, escape, request, jsonify
from random import randint
import thread, json
import sqlite3
from flask import g
from datetime import datetime
from hashlib import md5
import redis


app = Flask(__name__)

import os

DATABASE = os.path.join(app.root_path, 'database.db')

'''
This is the database code 
get_db() connects you to the database
close_connection() is called if the app ever ends
init_db() creates a blank database with the schema.sql file.
'''
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

'''
The following are functions for making it easier to interact with the database.
Their names make them very easy to understand.

TODO: Test these functions for bugs
'''

def createUser(username, password, firstName,lastName):
    db = get_db()
    values = (None, username, password, firstName, lastName, 0, 0, datetime.utcnow())
    print len(values)
    db.cursor().execute(''' insert into users values(?,?,?,?,?,?,?,?)''',
        values)
    db.commit()

def createPendingGame(creator,sets=[base],numberOfPlayers=4):
    db = get_db()
    userid = getUserID(creator)
    db.cursor().execute('insert into games values(?,?,?,?,?,?,?,?)',
        (None,pickle.dumps(sets),None,datetime.utcnow(),False,False,numberOfPlayers,userid))
    gameid = getLastRow("games","gameid")
    print gameid, "lastrowid"
    
    if not userid:
        flask.abort(402)
    db.cursor().execute('insert into userGames values(?,?,?,?,?)', (None, userid, gameid, False,0))
    db.commit()

def getCurrentGame(gameid):
    game = get_db().cursor().execute('''
            select game from games
            where gameid = %d

        ''' % gameid).fetchone()
    if game is None:
        return False
    return pickle.loads(game[0])



def getLiveGames():
   return getGames(True,False)

def getPendingGames():
    return getGames(False,False)

def getFinishedGames():
    return getGames(True,True)


def getGames(started, done):
    db = get_db()
    games = db.cursor().execute("select * from games where started=:Started and finished=:done",{"Started":started,"done":done}).fetchall()
    gamesList = []
    if games is None:
        return gamesList
    for game in games:
        gameid = game[0]
        creatorid = game[7]
        username = getUser(userid=creatorid)[1]
        sets = pickle.loads(game[1])
        if game is None:
            continue
        players = getPlayers(gameid)
        print players,"players---"
        if game[2] is None:
            g =None
        else:
            g = pickle.loads(game[2])
        gamesList.append({"game":g ,
                          "gameid":gameid,
                          "players":players,
                          "numberOfPlayers":game[6],
                          "creator":username,
                          "sets": sets
                        })
    return gamesList

def getUser(username=None,userid=None):
    db = get_db()
    if username is None:
        if userid is None:
            return None
        user = db.cursor().execute("select * from users where userid =:id",{"id":userid})
    else:
        user = db.cursor().execute("select * from users where username =:name",{"name":username})
    user = user.fetchone()
    print user
    if user is None:
        return False
    return user

def getState(gameid,username):
    db = get_db()
    game = getCurrentGame(gameid)
    return json.dumps(game.playerStates[username].getState())

def getUserID(username):
    db = get_db()
    print db.cursor().execute('select * from users where username="sirwillem"').fetchall()

    userid = db.cursor().execute("select * from users where username =:name", {"name":username}).fetchone()
    
    print userid
    if userid is None:
        print "no User with username %s" % username 
        return False
    return userid[0]

def getLastRow(table,tableID):
    db = get_db()
    result = db.cursor().execute("select %s from %s order by %s Desc limit 1"%(tableID, table,tableID)).fetchone()[0]
    return result

def getPlayers(gameid):
    db = get_db()
    players = db.cursor().execute("select username from users U, userGames uG where uG.gameid =%d and uG.userid = U.userid"%int(gameid)).fetchall()
    print db.cursor().execute("select * from users U, userGames uG where uG.gameid =%d and uG.userid = U.userid"%int(gameid)).fetchall(),"players..."
    if players is None:
        flask.abort(402)
    elif len(players)==0:
        return None
    return [str(player[0]) for player in players]

def getPassword(username):
    db = get_db()
    return db.cursor().execute("select password from users where username=:name",{"name":username}).fetchone()[0]

def joinGame(gameid, username):
    if username  in getPlayers(gameid):
        return False
    db = get_db()
    if db.cursor().execute('select * from userGames where gameid=:id',{"id":gameid}).fetchone() is None:
        flask.abort(402)
    db.cursor().execute('insert into userGames values(?,?,?,?,?)',(None,getUserID(username),gameid,False,0))
    db.commit()


def startGame(gameid):
    db = get_db()
    sets = db.cursor().execute("select sets from games where gameid=:id",{"id":gameid}).fetchone()
    if sets is None:
        flask.abort(401)
    sets = [allSets[Set] for Set in pickle.loads(sets[0])]
    players = getPlayers(gameid)
    print players,"players New Game"
    updateGame(gameid,Game(players,sets))


def updateGame(gameid, game):
    db = get_db()
    db.cursor().execute('''update games
        set game =:Game, started =:begin
        where gameid=:id
        ''',{"Game": pickle.dumps(game),"id":gameid, "begin": True})
    db.commit()



@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/lobby',methods = ["GET","POST"])
def lobby():
    if not session.has_key('username'):
        return redirect(url_for('login'))
    games = getPendingGames()
    if request.method == 'POST':
        if request.form.has_key('pending') and request.form['pending']=='See Pending Games':
            if len(games) == 0:
                return redirect(url_for('lobby', _method="GET"))
            return render_template("/lobby.html", pending = True, games = games)

        if request.form.has_key('newGame') and request.form['newGame'] == "Create Game":
            print "creation"
            return render_template("/lobby.html",newGame = True,sets = [{"name":Set} for Set in allSets])
        if request.form.has_key('liveGames'):
            games = getLiveGames()
            print "games---",games
            return render_template('/lobby.html',liveGames = True, games = games)
        

        return redirect(url_for("game",gameid=gameid))
        #print  "redirect Bitches"
        #return redirect(url_for('ready'))
    return render_template("/lobby.html",welcome=True,numPending= len(games))


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not getUserID(username):
            return render_template("/login.html",username=True)
        
        print hashPassword(password,username[-2:]) == getPassword(username)

        if hashPassword(password,username[-2:]) != getPassword(username):
            return render_template('/login.html',password=True)
        session['username'] = request.form['username']
        print session['username']
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
        #return render_template('/hand.html',name =name, hand=G.playerDict[name].hand)
        return json.dumps([card.getAttr() for card in G.playerDict[str(name)].hand])    
    return redirect(url_for('/'))



@app.route('/ready/<gameid>',methods=["GET","POST"])
def ready(gameid):
    if request.method == "POST":
        if request.form.has_key("join"):
            print "join"
            joinGame(gameid, session['username'])
            return redirect(url_for('lobby'))
        elif request.form.has_key("start"):
            startGame(gameid)
            return redirect(url_for("game",gameid=gameid))
    flask.abort(301)

@app.route('/supply/<int:gameid>')
def supply(gameid):
    game = getCurrentGame(gameid)
    if not game:
        return flask.abort(401)
    supply = game.supply
    return jsonify(supply.toDict())

@app.route('/game')
@app.route('/game/<int:gameid>', methods=['GET','POST'])
def game(gameid=None):
    if gameid is None:
        gameid = session['gameid']
    print '/static/pages/game.html'
    return app.send_static_file('pages/game.html')
    return render_template('/game.html',game=Games[gameid])


@app.route('/play/<card>/<int:gameid>',methods=['GET','POST'])
def playCard(gameid,card):
    if request.method == 'POST':
        card = card.lower()
        game = getCurrentGame(gameid)
        player = game.playerDict[session['username']]
        if player is not Games[gameid].currentPlayer:
            return "Not your Turn"
        game.currentTurn.playCard(card)
        return json.dumps([card.getAttr() for card in player.hand])

@app.route('/discard/<card>/<int:gameid>',methods=['GET','POST'])
def discard(gameid,card):
    if request.method == 'POST':
        game = getCurrentGame(gameid)
        player = game.playerDict[session['username']]
        if player is not game.currentPlayer:
            return "Not your Turn"
        card = game.currentTurn.strToCard(card)
        player.discardCard(card)
        return json.dumps([card.getAttr() for card in player.hand])

@app.route('/state/<int:gameid>',methods = ["GET","POST"])
def state(gameid):
    game = getCurrentGame(gameid)
    player = game.playerDict[session['username']]
    turn = game.currentTurn
        
    if request.method== "POST":
        return json.dumps(game.playerStates[player.name].getState())
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

@app.route('/games/pending')
def pending():
    return json.dumps( getPendingGames())

@app.route('/games/live')
def gamesInProgress():
    return json.dumps(getLiveGames())


@app.route('/new/Game', methods = ['GET','POST'])
def newGame():
    if request.method == "POST":
        sets = []
        for Set in allSets:
            if Set in request.form:
                sets.append(Set)
        username = session['username']
        createPendingGame(username,sets,request.form['numberOfPlayers'])
        return redirect(url_for('lobby',_method="POST",pending="See Pending Games"))
    else:
        flask.abort(304)


@app.route('/new/User', methods = ['GET','POST'])
def newUser():
    if request.method == "POST":
        if getUserID(request.form['username']):
            return render_template('/newuser.html', user=True)
        print "here111"
        if request.form['password'] != request.form['password2']:
            return render_template('/newuser.html',password=True)
        
        createUser(username = request.form['username'],
                      password = hashPassword(request.form['password'],
                                            request.form['username'][-2:]),
                      firstName = request.form['firstName'],
                      lastName  = request.form['lastName'])
        return redirect(url_for('lobby'))
    else:
        return render_template('/newuser.html')

@app.route('/log/<int:gameid>')
def getLog(gameid):
    game = getCurrentGame(gameid)
    return json.dumps(game.log)


red = redis.StrictRedis()

@app.route('/update/<int:gameid>', methods=['GET'])
def post(gameid):
    players = getPlayers(gameid)
    for player in players:
        state = getState(gameid, player)
        red.publish(player, "%s" % state)
    return Response(status=204)

def event_stream():
    print session
    pubsub = red.pubsub()
    pubsub.subscribe(session['username'])
    
    for message in pubsub.listen():
        print message," listen"
        yield 'data: %s\n\n' % message['data']

@app.route('/stream')
def stream():
    return Response(stream_with_context(event_stream()),
                          mimetype="text/event-stream")



app.secret_key = "\xf3Bg\x90\xec $xv\xee\xca`,A\"\'\x0f\\M&a\xf9\xbd\xdc"


def hashPassword(password,salt):
    return md5(password+salt).hexdigest()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)