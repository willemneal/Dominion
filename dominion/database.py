import sqlite3
import pickle
import json
import os
from flask import Flask, g
from datetime import datetime
from game import Game, base, allSets
import game

app = Flask(__name__)

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


def createUser(username, password, firstName, lastName):
    db = get_db()
    values = (None, username, password, firstName, lastName, 0, 0, datetime.utcnow())
    db.cursor().execute(''' INSERT INTO users VALUES(?,?,?,?,?,?,?,?)''',
                        values)
    db.commit()


def createPendingGame(creator, sets=[base], numberOfPlayers=4):
    db = get_db()
    userid = getUserID(creator)
    if not userid:
        Flask.abort(402)

    db.cursor().execute('INSERT INTO games VALUES(?,?,?,?,?,?,?,?)',
                        (None, pickle.dumps(sets), None, datetime.utcnow(),
                            False, False, numberOfPlayers, userid))
    gameid = getLastRow("games", "gameid")
    print gameid, "lastrowid"

    db.cursor().execute('INSERT INTO userGames VALUES(?,?,?,?,?)', (None, userid, gameid, False, 0))
    db.commit()


def getCurrentGame(gameid):
    game = get_db().cursor().execute('''
            SELECT game from games
            where gameid = %d
        ''' % gameid).fetchone()
    if game is None:
        return False
    return pickle.loads(game[0])


def getLiveGames():
    return getGames(True, False)


def getPendingGames():
    return getGames(False, False)


def getFinishedGames():
    """

    :rtype : game
    """
    return getGames(True, True)


def getGames(started, done):
    db = get_db()
    games = db.cursor().execute("SELECT * FROM games WHERE started=:Started AND finished=:done",
                                {"Started": started, "done": done}).fetchall()
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
        print players, "players---"
        # if game[2] is None:
        #     g = None
        # else:
        #     g = pickle.loads(game[2])
        gamesList.append({"gameid": gameid,
                          "players": players,
                          "numberOfPlayers": game[6],
                          "creator": username,
                          "sets": sets
        })
    return gamesList


def getUser(username=None, userid=None):
    db = get_db()
    if username is None:
        if userid is None:
            return None
        user = db.cursor().execute("SELECT * FROM users WHERE userid =:id", {"id": userid})
    else:
        user = db.cursor().execute("SELECT * FROM users WHERE username =:name", {"name": username})
    user = user.fetchone()
    print user
    if user is None:
        return False
    return user


def getState(gameid, username):
    db = get_db()
    game = getCurrentGame(gameid)
    print [card['name'] for card in game.playerStates[username].getState()['hand']]

    return game.playerStates[username].getState()


def getUserID(username):
    db = get_db()
    print db.cursor().execute('SELECT * FROM users WHERE username="sirwillem"').fetchall()

    userid = db.cursor().execute("SELECT * FROM users WHERE username =:name", {"name": username}).fetchone()

    print userid
    if userid is None:
        print "no User with username %s" % username
        return False
    return userid[0]


def getLastRow(table, tableID):
    db = get_db()
    result = db.cursor().execute("select %s from %s order by %s Desc limit 1" % (tableID, table, tableID)).fetchone()[0]
    return result


def getPlayers(gameid):
    db = get_db()
    players = db.cursor().execute(
        "select username from users U, userGames uG where uG.gameid =%d and uG.userid = U.userid" % int(
            gameid)).fetchall()
    print db.cursor().execute("select * from users U, userGames uG where uG.gameid =%d and uG.userid = U.userid" % int(
        gameid)).fetchall(), "players..."
    if players is None:
        Flask.abort(402)
    elif len(players) == 0:
        return None
    return [str(player[0]) for player in players]


def getPassword(username):
    db = get_db()
    return db.cursor().execute("SELECT password FROM users WHERE username=:name", {"name": username}).fetchone()[0]


def joinGame(gameid, username):
    if username in getPlayers(gameid):
        return False
    db = get_db()
    if db.cursor().execute('SELECT * FROM userGames WHERE gameid=:id', {"id": gameid}).fetchone() is None:
        Flask.abort(402)
    db.cursor().execute('INSERT INTO userGames VALUES(?,?,?,?,?)', (None, getUserID(username), gameid, False, 0))
    db.commit()


def startGame(gameid):
    db = get_db()
    sets = db.cursor().execute("SELECT sets FROM games WHERE gameid=:id", {"id": gameid}).fetchone()
    if sets is None:
        Flask.abort(401)
    sets = [allSets[Set] for Set in pickle.loads(sets[0])]
    players = getPlayers(gameid)
    print players, "players New Game"
    updateGame(gameid, Game(players, sets))


def updateGame(gameid, game):
    for playerName in game.playerStates:
        game.playerStates[playerName].setState()
    db = get_db()
    db.cursor().execute('''UPDATE games
        SET game =:Game, started =:begin
        WHERE gameid=:id
        ''', {"Game": pickle.dumps(game), "id": gameid, "begin": True})
    db.commit()
