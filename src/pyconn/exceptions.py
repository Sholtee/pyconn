# RPC.NET-Connector
# exceptions.py
# Author: Denes Solti

from typing import NamedTuple

class RpcException(Exception):
    """The exception that is thrown if a Remote Procedure Call failed."""
    def __init__(self, descriptor: NamedTuple) -> None:
        super().__init__(descriptor.message)
        self.data = descriptor.data