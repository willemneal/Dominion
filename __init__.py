import turn
import baseCards
import supply
import player
import card


def reloadAll():
    reload(turn)
    reload(baseCards)
    reload(card)
    reload(player)
    reload(supply)

reloadAll()