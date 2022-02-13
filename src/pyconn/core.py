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

# pylint: disable-next=too-many-instance-attributes
class ApiConnection:
    """Represents an API connection against an RPC.NET backend"""

    def __init__(self, urlbase: str, property_fmt: Callable[[str], str] = _snake_case) -> None:
        self.headers = {}
        self.timeout = 10
        self.sessionid = None

        self.__urlbase = urlbase
        self.__result_fld = property_fmt('Result')
        self.__exception_fld = property_fmt('Exception')
        self.__exception_msg_fld = property_fmt('Message')
        self.__exception_dta_fld = property_fmt('Data')
        self.__property_fmt = property_fmt

    def __fetch_json(self, req: Request, prop_fmt: Callable[[str], str]) -> tuple:
        with urlopen(req, timeout=self.timeout) as resp:
            if resp.status != 200:
                raise Exception(resp.read() or resp.msg)

            # lookup is case insensitive, KeyError never raised
            if (content_type := (resp.headers['content-type'] or '').lower()) != 'application/json':
                raise Exception(f'Content type not supported: "{content_type}"')

            return _load_json(resp.read(), prop_fmt)

    def invoke(self, module: str, method: str, args: array = None) -> tuple:
        """Invokes a remote API identified by a module and method name"""

        if not args:
            args = []

        query = {'module': module, 'method': method}
        if self.sessionid:
            query['sessionid'] = self.sessionid

        req=Request(
            url = f'{self.__urlbase}?{urlencode(query)}',
            data = json.dumps(args).encode(),
            method = 'POST',
            headers = {**self.headers, **{'content-type': 'application/json'}}
        )

        data = self.__fetch_json(req, prop_fmt=self.__property_fmt)

        if (exception := getattr(data, self.__exception_fld)):
            raise RpcException(getattr(exception, self.__exception_msg_fld), getattr(exception, self.__exception_dta_fld))

        return getattr(data, self.__result_fld)

    def create_api(self, module: str) -> Any:
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
        # don't use prop_fmt so the method and property names remain untouched
        schema = self.__fetch_json(Request(f'{self.__urlbase}?{urlencode({"module": module})}', method = 'GET'), prop_fmt=None)

        if not (module_descr := getattr(schema, module, None)):
            raise Exception('Schema could not be found')

        # workaround to capture loop variables
        def lambda_factory(module, method):
            return lambda _, *args: self.invoke(module, method, [*args])

        typedescr = {'_conn': self}

        for method in module_descr.Methods._fields:
            typedescr[self.__property_fmt(method)] = lambda_factory(module, method)

        for prop in (props := module_descr.Properties)._fields:
            prop_descr = getattr(props, prop)

            typedescr[self.__property_fmt(prop)] = property(
                lambda_factory(module, f'get_{prop}') if prop_descr.HasGetter else None,
                lambda_factory(module, f'set_{prop}') if prop_descr.HasSetter else None
            )

        return type(module, (object, ), typedescr)()
