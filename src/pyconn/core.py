# RPC.NET-Connector
# core.py
# Author: Denes Solti

from array import array
import json
from types import FunctionType
from typing import Any
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

    def invoke(self, module: str, method: str, args: array = []) -> tuple:
        """Invokes a remote API identified by a module and method name"""

        query = {'module': module, 'method': method}
        if self.sessionid:
            query['sessionid'] = self.sessionid

        req=Request(
            url = '{0}?{1}'.format(self.urlbase, urlencode(query)),
            data = json.dumps(args).encode(),
            method = 'POST',
            headers = {**self.headers, **{'content-type': 'application/json'}}
        )

        with urlopen(req, timeout=self.timeout) as resp:
            if resp.status != 200:
                raise Exception(resp.msg)

            # lookup is case insensitive, KeyError never raised
            if (ct := (resp.headers['content-type'] or '').lower()) != 'application/json':
                raise Exception('Content type not supported: "{0}"'.format(ct))

            data = _load_json(resp.read())
       
        if data.exception:
            raise RpcException(data.exception)
       
        return data.result
        
    def create_api(self, module: str, methods_id: str = 'Methods', props_id: str = 'Properties', prop_fmt: FunctionType = _snake_case) -> Any:
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

        with urlopen(Request('{0}?{1}'.format(self.urlbase, urlencode({'module': module})), method = 'GET'), timeout=self.timeout) as resp:
            schema = _load_json(resp.read(), prop_fmt=None)

        if not (module_descr := getattr(schema, module, None)):
            raise Exception('Schema could not be found')

        # workaround to capture loop variables
        def lambda_factory(module, method):
            return lambda _, *args: self.invoke(module, method, [*args])

        typedescr = {'_conn': self}
    
        for method in getattr(module_descr, methods_id)._fields:
            typedescr[_snake_case(method)] = lambda_factory(module, method)
        
        for prop in (props := getattr(module_descr, props_id))._fields:
            prop_descr = getattr(props, prop)

            typedescr[_snake_case(prop)] = property(
                lambda_factory(module, 'get_{0}'.format(prop)) if prop_descr.HasGetter else None,
                lambda_factory(module, 'set_{0}'.format(prop)) if prop_descr.HasSetter else None
            )

        return type(module, (object, ), typedescr)()
            
if __name__ == '__main__':
    # This block will be invoked if the core.py module is being run directly (not via import)
    pass