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