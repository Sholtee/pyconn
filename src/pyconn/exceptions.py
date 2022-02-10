""" Contains the `RpcException` class """

# RPC.NET-Connector
# exceptions.py
# Author: Denes Solti

class RpcException(Exception):
    """The exception that is thrown if a Remote Procedure Call failed."""
    def __init__(self, message: str, data: tuple) -> None:
        super().__init__(message)
        self.data = data
