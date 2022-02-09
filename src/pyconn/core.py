""" Contains the core functionality of the `pyconn` library. Notable class is `ApiConnection` """

# RPC.NET-Connector
# core.py
# Author: Denes Solti

from array import array
import json
from typing import Any, Callable
from urllib.request import urlopen, Request
from urllib.parse import urlencode

from exceptions import RpcException
from internals import _load_json, _snake_case

class ApiConnection:
    """Represents an API connection against an RPC.NET backend"""

    def __init__(self, urlbase: str) -> None:
        self.urlbase = urlbase
        self.headers = {}
        self.timeout = 10
        self.sessionid = None

    def invoke(self, module: str, method: str, args: array = None) -> tuple:
        """Invokes a remote API identified by a module and method name"""

        if not args:
            args = []

        query = {'module': module, 'method': method}
        if self.sessionid:
            query['sessionid'] = self.sessionid

        req=Request(
            url = f'{self.urlbase}?{urlencode(query)}',
            data = json.dumps(args).encode(),
            method = 'POST',
            headers = {**self.headers, **{'content-type': 'application/json'}}
        )

        with urlopen(req, timeout=self.timeout) as resp:
            if resp.status != 200:
                raise Exception(resp.msg)

            # lookup is case insensitive, KeyError never raised
            if (content_type := (resp.headers['content-type'] or '').lower()) != 'application/json':
                raise Exception(f'Content type not supported: "{content_type}"')

            data = _load_json(resp.read())

        if data.exception:
            raise RpcException(data.exception)

        return data.result

    def create_api(self, module: str, methods_id: str = 'Methods', props_id: str = 'Properties', fmt: Callable[[str], str] = _snake_case) -> Any:
        """Creates a new API set according to the given schema

        A basic schema looks like:

        {
            "IServiceName": {
                "Methods": {
                    "Method_1": {
                        "Layout": "TODO"
                    }
                },
                "Properties": {
                    "Prop_1": {
                        "HasGetter": true,
                        "HasSetter": false,
                        "Layout": "TODO"
                    }
                }
            }
        }
        """

        with urlopen(Request(f'{self.urlbase}?{urlencode({"module": module})}', method = 'GET'), timeout=self.timeout) as resp:
            schema = _load_json(resp.read(), prop_fmt=None)

        if not (module_descr := getattr(schema, module, None)):
            raise Exception('Schema could not be found')

        # workaround to capture loop variables
        def lambda_factory(module, method):
            return lambda _, *args: self.invoke(module, method, [*args])

        typedescr = {'_conn': self}

        for method in getattr(module_descr, methods_id)._fields:
            typedescr[fmt(method)] = lambda_factory(module, method)

        for prop in (props := getattr(module_descr, props_id))._fields:
            prop_descr = getattr(props, prop)

            typedescr[fmt(prop)] = property(
                lambda_factory(module, f'get_{prop}') if prop_descr.HasGetter else None,
                lambda_factory(module, f'set_{prop}') if prop_descr.HasSetter else None
            )

        return type(module, (object, ), typedescr)()
