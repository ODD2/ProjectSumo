"""
od/network/misc.py - Miscellaneous network layer utilities.
"""


class CastObject:
    """Lightweight placeholder used as the destination for broadcast packages.

    Its ``name`` attribute is set to a pipe-separated list of subscriber
    vehicle names before a broadcast package is created, enabling log
    messages to identify all intended recipients without carrying full
    object references.
    """
    name = ""
