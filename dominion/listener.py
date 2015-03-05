from event import Event
class Listener(dict):
    def update(self,listener):
        map(lambda key:self.addListener(key,listener[key]),listener.keys())

    def addListener(self,name,callback):
        event = self.setdefault(name,Event())
        event.append(callback)



class trigger(object):
    def __init__(self, event,listener):
        self.event = event
        self.listener = listener

    def __call__(self,*args,**kwargs):
        self.listener[self.event](*args,**kwargs)


L = Listener()

def foo():
    print "foo"

L.addListener('willem',foo)

@trigger('willem',L)
def faa():
    print "faa y'all"

faa()
