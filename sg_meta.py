import inspect


class SocialGroupIterator:
    ''' Iterator class '''

    def __init__(self, sg):
        # Team object reference
        self.sg = sg
        # member variable to keep track of current index
        self._index = 0
        self._sg_var = [
            i[1] for i in inspect.getmembers(sg)
            if not i[0].startswith('_') and not inspect.isroutine(i[1])
        ]

    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < len(self._sg_var):
            result = self._sg_var[self._index]
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration


class SocialGroupAttr:
    def __init__(self, lname, fname, qos, gid):
        self.lname = lname
        self.fname = fname
        self.qos = qos
        self.gid = gid

    def __repr__(self):
        return "<{}(QoS:{}, Gid:{}>".format(self.fname, self.qos, self.gid)

    def __str__(self):
        return self.fname

    def __index__(self):
        return self.gid

    def __hash__(self):
        return self.gid

    def __eq__(self, other):
        return self.gid == other.gid


class SocialGroupMeta(type):
    def __new__(cls, name, bases, dct):
        gid = 0
        for key, value in dct.items():
            if(not key.startswith('_') and not inspect.isroutine(value)):
                dct[key] = SocialGroupAttr(
                    name+str(bases), key, value, gid
                )
                gid += 1
        return super(SocialGroupMeta, cls).__new__(cls, name, bases, dct)

    def __iter__(self):
        return SocialGroupIterator(self)
