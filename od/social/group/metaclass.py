import inspect
from os import confstr_names


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
    def __init__(self, qos, pref, dyn):
        self.qos = qos
        self.pref = pref
        self.dyn = dyn


class SocialGroupAttr:
    def __init__(self, lname, fname, gid, config: SocialGroupConfig):
        self.lname = lname
        self.fname = fname
        self.gid = gid
        self.qos = config.qos
        self.pref = config.pref
        self.dyn = config.dyn

    def __repr__(self):
        return "<{}(QoS:{}, Gid:{})>".format(self.fname, self.qos, self.gid)

    def __str__(self):
        return self.fname

    def __index__(self):
        return self.gid

    def __hash__(self):
        return self.gid

    def __eq__(self, other):
        return self.gid == other.gid


class SocialGroupMeta(type):
    # Create SocialGroup Class Object, Initialize with predefined(static) groups.
    def __new__(cls, name, bases, dct):
        gserial = 0
        sg_attrs = []
        cname = name + str(bases)
        for key, value in dct.items():
            if(not key.startswith('_') and not inspect.isroutine(value)):
                sg_attrs.append(
                    SocialGroupAttr(
                        cname,  key, gserial, value
                    )
                )
                dct[key] = sg_attrs[-1]
                gserial += 1
        # __sg__attrs__ for iterability
        dct["__sg_attrs__"] = sg_attrs
        # __gserial__ for unique gid
        dct["__gserial__"] = gserial
        # __cname__ for SocailGroupAttr initialization
        dct["__cname__"] = cname

        return super(SocialGroupMeta, cls).__new__(cls, name, bases, dct)

    # Dynamically adds social group.
    def Create(cls, name, value):
        # append to __sg__attrs__ for iterability.
        cls.__sg_attrs__.append(
            SocialGroupAttr(
                cls.__cname__,
                name,
                cls.__gserial__,
                value
            )
        )
        # create social group entity.
        setattr(
            cls,
            name,
            cls.__sg_attrs__[-1]
        )
        # next social group gid.
        cls.__gserial__ += 1

    def __iter__(cls):
        return iter(cls.__sg_attrs__)

    def __call__(cls, gid: int):
        return (
            cls.__sg_attrs__[gid]
            if (gid < len(cls.__sg_attrs__) and gid > -1)
            else None
        )
