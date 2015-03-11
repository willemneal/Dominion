from gameObject import GameObject

class ChoiceType(object):
    action = "action"
    treasure = "treasure"
    drawnCards = "drawnCards"
    option = "option" 

class Choice(GameObject):
    def __init__(self, player, turn, kind):
        self.player = player
        self.turn = turn
        self.kind = kind
