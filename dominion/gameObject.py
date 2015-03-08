from listener import Listener

class GameObject(object):
    def __init__(self):
        self.listener = Listener()

    def hasEvent(self,name):
        return name in self

    def updateListener(self,GameObject):
        self.listener.update(GameObject.listener)

    def mergeListeners(self,listeners):
        map(lambda listener: self.updateListener(listener),listeners)

    def addSubscriber(self,name,callback):
        self.listener.addListener(name, callback)

    def event(self,name,*args, **kwargs):
        if name in self.listener:
            self.listener[name](*args,**kwargs)
        return False

TO = GameObject()
GO = GameObject()
def foo(x):
    print x

def go(*args):
    print "go"
TO.addSubscriber('willem',foo)
GO.listener.addListener("willem",go)
GO.update(TO)

GO.event("willem",2)
