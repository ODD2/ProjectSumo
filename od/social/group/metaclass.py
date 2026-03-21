"""
od/social/group/metaclass.py - Metaclass machinery for dynamic social groups.

SocialGroupMeta intercepts class creation so that each class-level attribute
declared as a SocialGroupConfig is replaced by a SocialGroupAttr with an
auto-assigned gid.  The class is also made iterable (iterates over all
SocialGroupAttr instances) and callable (SocialGroup(gid) → SocialGroupAttr).

New groups can be added after class creation via SocialGroup.Create(), which
appends a new SocialGroupAttr and increments the shared serial counter.
"""
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
    """Declaration-time descriptor for a social group's static properties.

    Used as the right-hand side of class attributes in SocialGroup.
    SocialGroupMeta converts each instance into a SocialGroupAttr at class
    creation time.

    Args:
        qos:    QoSLevel for this group.
        pref:   Preferred base station type list (first element = highest
                preference).
        reader: True if vehicles only receive data (no uplink data generation).
        dyn:    True if this is a dynamically created group (not predefined).
    """
    def __init__(self, qos, pref, reader, dyn):
        self.qos = qos
        self.pref = pref
        self.dyn = dyn
        self.reader = reader


class SocialGroupAttr:
    """Runtime representation of one social group.

    Attributes:
        lname:  Long name (class name + base class string) for uniqueness.
        fname:  Short human-readable name (e.g. "CRASH", "RCWS").
        gid:    Unique integer group ID used as dict key and list index.
        qos:    QoSLevel.
        pref:   Preferred BS type ordering.
        reader: Whether vehicles only receive (no uplink data).
        dyn:    Whether this is a dynamically created group.
    """
    def __init__(self, lname, fname, gid, config: SocialGroupConfig):
        self.lname = lname
        self.fname = fname
        self.gid = gid
        self.qos = config.qos
        self.pref = config.pref
        self.reader = config.reader
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
    """Metaclass that turns SocialGroupConfig class attributes into SocialGroupAttr.

    Also stores ``__sg_attrs__`` (list of all groups) for iteration and
    ``__gserial__`` (next available gid) for dynamic group creation.
    """
    def __new__(cls, name, bases, dct):
        """Build the SocialGroup class, converting config attributes to attrs."""
        gserial = 0
        sg_attrs = []
        cname = name + str(bases)
        for key, value in dct.items():
            if(not key.startswith('_') and not inspect.isroutine(value)):
                sg_attrs.append(
                    SocialGroupAttr(
                        cname, key, gserial, value
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

    def Create(cls, name, value):
        """Dynamically add a new social group to the class at runtime.

        Args:
            name:  Attribute name for the new group (e.g. "DYN_SG_0").
            value: SocialGroupConfig describing the new group's properties.
        """
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
        """Iterate over all registered SocialGroupAttr instances."""
        return iter(cls.__sg_attrs__)

    def __call__(cls, gid: int):
        """Look up a SocialGroupAttr by its integer gid.

        Returns None if gid is out of range.
        """
        return (
            cls.__sg_attrs__[gid]
            if (gid < len(cls.__sg_attrs__) and gid > -1)
            else None
        )
