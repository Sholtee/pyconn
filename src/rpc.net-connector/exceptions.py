# RPC.NET-Connector
# exceptions.py
# Author: Denes Solti

from internals import _getprop

class RpcException(Exception):
    """The exception that is thrown if the Remote Procedure Call failed."""
    def __init__(self, descriptor: dict) -> None:
        super().__init__(_getprop(descriptor, 'message'))
        self.data = _getprop(descriptor, 'data')