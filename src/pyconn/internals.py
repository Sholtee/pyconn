# RPC.NET-Connector
# internals.py
# Author: Denes Solti

from array import array
from collections import namedtuple

def _getprop(data: dict, name: str) -> object:
    """Gets a value from a dictionary associated with the given name (using case insensitive linear search)."""

    name = name.lower()
    for (key, value) in data.items():
        if key.lower() == name:
            return value
            
    return None

def _replacedict(data: object, name: str = None) -> tuple:
    """Replaces dict instances with a named tuples in the given object tree"""

    if isinstance(data, dict):
        for (key, val) in data.items():
            data[key] = _replacedict(val)

        return namedtuple('NamedTuple_{0}'.format(id(data)) if not name else name, data.keys())(*data.values())

    if isinstance(data, array):
        for (i, val) in enumerate(data):
            data[i] = _replacedict(val)
    
    return data