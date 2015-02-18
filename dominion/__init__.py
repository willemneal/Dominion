import os
from flask import Flask, g
from game import Game, base, allSets

app = Flask("Dominion")

DATABASE = os.path.join(app.root_path, 'database.db')
