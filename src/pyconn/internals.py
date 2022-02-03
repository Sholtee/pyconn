# RPC.NET-Connector
# internals.py
# Author: Denes Solti

from collections import namedtuple
import json
import re

_snake_case_regexp = re.compile(r'(?<!^)(?=[A-Z])')

def _snake_case(s: str) -> str:
    """Converts the given string to 'snake_case'"""

    return _snake_case_regexp.sub('_', s).lower()

def _load_json(s: str) -> tuple:
    """Loads the given JSON string. Object properties are parsed as ``NamedTuple`` using 'snake_case' naming."""

    def as_namedtuple(kvps: list[tuple]) -> tuple:
        cls = namedtuple('NamedTuple_{0}'.format(id(kvps)), [_snake_case(k) for (k, _) in kvps])
        return cls(*[v for (_, v) in kvps])

    return json.loads(s, object_pairs_hook=as_namedtuple)

def _getprop(data: dict, name: str) -> object:
    """Gets a value from a dictionary associated with the given name (using case insensitive linear search)."""

    name = name.lower()
    for (key, value) in data.items():
        if key.lower() == name:
            return value
            
    return None