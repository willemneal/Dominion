from event import Event
class Listener(dict):
    def update(self,listener):
        map(lambda key:self.addListener(key,listener[key]),listener.keys())

    def addListener(self,name,callback):
        event = self.setdefault(name,Event())
        event.append(callback)

    def trigger(funcargs):


class trigger(object):
    def __init__(self, event,listener):
        if event is not None:
            listener[event]

L = Listener()

def foo():
    print "foo"

L.addListener('willem',foo)

@trigger('willem',listener)
def faa():
    print "faa y'all"

faa()
