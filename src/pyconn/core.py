# RPC.NET-Connector
# core.py
# Author: Denes Solti

from array import array
import json
from typing import Iterator, Union
from urllib import request
from urllib.parse import urlencode

from exceptions import RpcException
from internals import _as_namedtuple, _getprop

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

        req=request.Request(
            url = '{0}?{1}'.format(self.urlbase, urlencode(query)),
            data = json.dumps(args).encode(),
            method = 'POST',
            headers = {**self.headers, **{'content-type': 'application/json'}}
        )

        with request.urlopen(req, timeout=self.timeout) as resp:
            if resp.status != 200:
                raise Exception(resp.msg)

            if (ct := (_getprop(resp.info(), 'content-type') or '').lower()) != 'application/json':
                raise Exception('Content type not supported: "{0}"'.format(ct))

            data = json.loads(resp.read())
       
        if exception := _getprop(data, 'exception'):
            raise RpcException(exception)
       
        if isinstance(result := _getprop(data, 'result'), dict):
            result = _as_namedtuple(result, '{0}Result'.format(module))

        return result

    def create_api(self, schema: Union[str, dict]) -> Iterator[object]:
        """Creates a new API set according to the given schema

        A basic schema looks like:

        {
            "IServiceName": {
                "methods": {
                    "Method_1": {
                        "alias": "method_1"
                    }
                },
                "properties": {
                    "Prop_1": {
                        "alias": "prop_1",
                        "hasgetter": true,
                        "hassetter": false
                    }
                }
            }
        }
        """

        if isinstance(schema, str):
            with request.urlopen(schema) as resp:
                schema = json.loads(resp.read())

        if not isinstance(schema, dict):
            raise Exception('Malformed schema')

        # workaround to capture loop variables
        def lambda_factory(module, method):
            return lambda _, *args: self.invoke(module, method, [*args])

        for (module, module_descr) in schema.items():
            typedescr = {'_conn': self}
        
            if isinstance(methods := _getprop(module_descr, 'methods'), dict):
                for (method, method_descr) in methods.items():
                    if not isinstance(method_descr, dict):
                        raise Exception('Invalid method descriptor: {0}'.format(method_descr))

                    typedescr[_getprop(method_descr, 'alias') or method] = lambda_factory(module, method)
            
            if isinstance(props := _getprop(module_descr, 'properties'), dict):
                for (prop, prop_descr) in props.items():
                    if not isinstance(prop_descr, dict):
                        raise Exception('Invalid property descriptor: {0}'.format(prop_descr))

                    typedescr[_getprop(prop_descr, 'alias') or prop] = property(
                        lambda_factory(module, 'get_{0}'.format(prop)) if _getprop(prop_descr, 'hasgetter') else None,
                        lambda_factory(module, 'set_{0}'.format(prop)) if _getprop(prop_descr, 'hassetter') else None
                    )

            yield type(module, (object, ), typedescr)()
            

if __name__ == '__main__':
    # This block will be invoked if the core.py module is being run directly (not via import)
    pass