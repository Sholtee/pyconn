# RPC.NET-Connector
# internals.py
# Author: Denes Solti

from collections import namedtuple
import json
import string
from types import FunctionType
from typing import Iterable

def _snake_case(s: str) -> str:
    """Converts the given string to 'snake_case'"""

    def core() -> Iterable[str]:
        upper_chrs = set(string.ascii_uppercase)
        s_len = len(s)

        previous_chr = None
        for (i, c) in enumerate(s):
            if c in upper_chrs and not previous_chr in upper_chrs and (i == s_len - 1 or not s[i + 1] in upper_chrs):
                if (i > 0):
                    yield "_"
                yield c.lower()
            else:
                yield c

            previous_chr = c

    return ''.join(core())

def _load_json(s: str, prop_fmt: FunctionType = _snake_case) -> tuple:
    """Loads the given JSON string. If the string represents an object a ``NamedTuple`` is returned."""

    def as_namedtuple(kvps: list[tuple]) -> tuple:
        cls = namedtuple('NamedTuple_{0}'.format(id(kvps)), [prop_fmt(k) for (k, _) in kvps] if prop_fmt else [k for (k, _) in kvps])
        return cls(*[v for (_, v) in kvps])

    return json.loads(s, object_pairs_hook=as_namedtuple)