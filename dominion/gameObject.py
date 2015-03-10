from callMe import Listener

class GameObject(object):
    def __init__(self):
        self.listener = Listener()

    def hasEvent(self, name):
        return name in self.listener

    def addListener(self, gameObject):
        self.listener + gameObject.listener

    def removeListener(self, gameObject):
        self.listener - gameObject.listener


    def mergeGameObjects(self,GameObjects):
        map(lambda GO: self.addListener(GO.listener),GameObjects)

    def trigger(self,*args, **kwargs):
        return self.listener.trigger(*args, **kwargs)

    def listen(self,*args, **kwargs):
        return self.listener.listen(*args, **kwargs)

    def addSubscriber(self,name,callback):
        self.listener.addSub(name, callback)

    def removeSubscriber(self,name,callback):
        self.listener.removeSub(name, callback)

    def event(self,name,*args, **kwargs):
        if name in self.listener:
            self.listener(name,*args,**kwargs)
        return False

    def __add__(self,gameObject):
        self.addListener(gameObject)

    def __sub__(self,gameObject):
        self.removeListener(gameObject)



# TO = GameObject()
# GO = GameObject()
# @TO.listen('willem')
# def foo(x):
#     print x
#
# def go(*args):
#     print "go"
# #TO.addSubscriber('willem',foo)
# GO.listener.addSub("willem",go)
# GO + TO
#
# @GO.trigger('willem')
# def faa(x):
#     return x
#
# GO.willemEvent()
# GO - TO
# print GO.listener
# faa(3)
