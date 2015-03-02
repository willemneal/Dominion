from event import Event
class Listener(dict):
    def update(self,listener):
        EL = listener
        for key in EL:
            if key in self.keys():
                self[key].append(EL[key])
            else:
                self[key] = EL[key]

    def addListener(self,name,callback):
        event = self.setdefault(name,Event())
        event.append(callback)


    def __call__(self, event, *args, **kwargs):
        self[event](*args, **kwargs)
