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

        prev_is_upper = False
        curr_is_upper = False
        next_is_upper = s_len > 0 and s[0] in upper_chrs

        for (i, c) in enumerate(s):
            prev_is_upper = curr_is_upper
            curr_is_upper = next_is_upper
            next_is_upper = i < s_len - 1 and s[i + 1] in upper_chrs

            if curr_is_upper and not prev_is_upper:
                if i > 0:
                    yield "_"
                if not next_is_upper:
                    yield c.lower()
                    curr_is_upper = False
                    continue

            if not curr_is_upper and prev_is_upper:
                yield "_"

            yield c

    return ''.join(core())

def _load_json(s: str, prop_fmt: FunctionType = _snake_case) -> tuple:
    """Loads the given JSON string. If the string represents an object a ``NamedTuple`` is returned."""

    def as_namedtuple(kvps: list[tuple]) -> tuple:
        cls = namedtuple('NamedTuple_{0}'.format(id(kvps)), [prop_fmt(k) for (k, _) in kvps] if prop_fmt else [k for (k, _) in kvps])
        return cls(*[v for (_, v) in kvps])

    return json.loads(s, object_pairs_hook=as_namedtuple)