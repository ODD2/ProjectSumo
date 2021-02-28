import inspect


# class SocialGroupIterator:
#     ''' Iterator class '''

#     def __init__(self, sg):
#         # Team object reference
#         self._sg_attrs = sg.sg_attrs
#         # member variable to keep track of current index
#         self._index = 0

#     def __next__(self):
#         ''''Returns the next value from team object's lists '''
#         if self._index < len(self._sg_attrs):
#             result = self._sg_attrs[self._index]
#             self._index += 1
#             return result
#         # End of Iteration
#         raise StopIteration

class SocialGroupConfig:
    def __init__(self, qos, pref):
        self.qos = qos
        self.pref = pref


class SocialGroupAttr:
    def __init__(self, lname, fname, gid, config: SocialGroupConfig):
        self.lname = lname
        self.fname = fname
        self.gid = gid
        self.qos = config.qos
        self.pref = config.pref

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
        sg_attrs = []
        for key, value in dct.items():
            if(not key.startswith('_') and not inspect.isroutine(value)):
                sg_attrs.append(
                    SocialGroupAttr(
                        name+str(bases),  key, gid, value
                    )
                )
                dct[key] = sg_attrs[-1]
                gid += 1
        dct["sg_attrs"] = sg_attrs
        return super(SocialGroupMeta, cls).__new__(cls, name, bases, dct)

    def __iter__(cls):
        return iter(cls.sg_attrs)

    def __call__(cls, gid: int):
        return cls.sg_attrs[gid] if gid < len(cls.sg_attrs) else None
