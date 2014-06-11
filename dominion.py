from flask import Flask
import pickle
from game import Game,base,playerList
from flask import render_template, session, redirect, url_for, escape, request, jsonify
from random import randint
import thread, json
import sqlite3
from flask import g
from datetime import datetime
from hashlib import md5

app = Flask(__name__)

import os

DATABASE = os.path.join(app.root_path, 'database.db')


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

def getUserID(username):
    db = get_db()
    print db.cursor().execute('select * from users where username="sirwillem"').fetchall()

    userid = db.cursor().execute("select * from users where username =:name", {"name":username}).fetchone()
    
    print userid
    if userid is None:
        print "no User with username %s" % username 
        return False
    return userid[0]

def


def createUser(username, password, firstName,lastName):
    db = get_db()
    values = (None, username, password, firstName, lastName, 0, 0, datetime.utcnow())
    print len(values)
    db.cursor().execute(''' insert into users values(?,?,?,?,?,?,?,?)''',
        values)
    db.commit()

def createReadyGame(creator,sets=[base]):
    db = get_db()
    db.cursor().execute('insert into games values(?,?,?,?)',(None,pickle.dumps(sets),"not Started",datetime.utcnow()),False,False)
    gameid = db.cursor().lastrowid
    userid = getUserID(creator)
    if not userid:
        abort(402)
    db.cursor().execute('insert into userGames values(?,?,?,?,?)', (None, gameid, userid, False,0)
    db.commit()

def getPassword(username):
    db = get_db()
    return db.cursor().execute("select password from users where username=:name",{"name":username}).fetchone()[0]


def getCurrentGame(gameid):
    pointer = get_db().cursor.execute('''
            select pointer from games
            where gameid = %d

        ''' % gameid).fetchone()
    if pointer is None:
        return False
    return pickle.loads(pointer[0])

Games = {}
GAMESIZE = 1
readyPlayers = []
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/lobby',methods = ["GET","POST"])
def lobby():
    if not session.has_key('username'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        db = get_db()
        print "lobbypost"
        gameid = randint(0,1000)
        while gameid in Games:
            gameid = randint(0,1000)
        print 'ready/'+str(gameid)
        session['gameid'] = gameid

        readyPlayers.append(session['username'])
        ## change this later
        Games[gameid] = Game(readyPlayers,[base])
        db.cursor().execute('insert into games values(?,?,?,?)',(gameid,pickle.dumps([base]),pickle.dumps(Games[gameid]),datetime.utcnow()),False)
        db.commit()
        print Games
        thread.start_new_thread(Games[gameid].playGame,())
        print Games
        return redirect(url_for("game",gameid=gameid))
        #print  "redirect Bitches"
        #return redirect(url_for('ready'))
    return render_template("/lobby.welcome.html")


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not getUserID(username):
            return render_template("/login.html",username=True)
        
        print hashPassword(password,username[-2:]) , getPassword(username)
        if hashPassword(password,username[-2:]) != getPassword(username):

            return render_template('/login.html',password=True)
        session['username'] = request.form['username']
        if request.form['remember_me'] == "on":
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
        return json.dumps([card.getAttr() for card in G.playerDict[name].hand])    
    return redirect(url_for('/'))

@app.route('/ready/<gameid>')
def ready():
    Games[gameid] = Game(readyPlayers,[base])
    Games[gameid].playGame()
    return redirect(url_for("game",gameid=gameid))

@app.route('/supply/<int:gameid>')
def supply(gameid):
    game = getCurrentGame(gameid)
    if not game:
        return abort(401)
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

@app.route('/state/<int:gameid>')
def state(gameid):
    player = Games[gameid].playerDict[session['username']]
    turn = Games[gameid].currentTurn
    while player not in turn.playerChoice:
        continue
    return jsonify.dumps(player.game.state())

@app.route('/games/online')
def players():
    global Games
    print Games
    return jsonify.dumps(Games)

@app.route('/new/User', methods = ['GET','POST'])
def newUser():
    if request.method == "POST":
        if getUserID(request.form['username']):
            return render_template('/newuser.html', user=True)
        if request.form['password']!=request.form['password2']:
            return render_template('/newuser.html',password=True)
        createUser(username = request.form['username'],
                      password = hashPassword(request.form['password'],request.form['username'][-2:]),
                      firstName = request.form['firstName'],
                      lastName  = request.form['lastName'])
        return redirect(url_for('lobby'))
    else:
        return render_template('/newuser.html')

app.secret_key = "\xf3Bg\x90\xec $xv\xee\xca`,A\"\'\x0f\\M&a\xf9\xbd\xdc"


def hashPassword(password,salt):
    return md5(password+salt).hexdigest()

if __name__ == '__main__':
    app.run(debug=True)