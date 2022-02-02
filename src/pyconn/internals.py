# RPC.NET-Connector
# internals.py
# Author: Denes Solti

from collections import namedtuple

def _getprop(data: dict, name: str) -> object:
    """Gets a value from a dictionary associated with the given name (using case insensitive linear search)."""

    name = name.lower()
    for (key, value) in data.items():
        if key.lower() == name:
            return value
            
    return None

def _as_namedtuple(data: dict, name: str = None) -> tuple:
    """Converts a dictionary to a named tuple"""

    for (key, val) in data.items():
        if isinstance(val, dict):
            data[key] = _as_namedtuple(val)

    return namedtuple('NamedTuple_{0}'.format(id(data)) if not name else name, data.keys())(*data.values())