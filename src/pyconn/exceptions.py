# RPC.NET-Connector
# exceptions.py
# Author: Denes Solti

from collections import namedtuple

class RpcException(Exception):
    """The exception that is thrown if the Remote Procedure Call failed."""
    def __init__(self, descriptor: namedtuple) -> None:
        super().__init__(descriptor.message)
        self.data = descriptor.data