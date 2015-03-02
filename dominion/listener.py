from event import Event
class Listener(dict):
    def update(self,listener):
        map(lambda key:self.addListener(key,listener[key]),listener.keys())

    def addListener(self,name,callback):
        event = self.setdefault(name,Event())
        event.append(callback)
