# RPC.NET-Connector tests
# core.py
# Author: Denes Solti

from importlib import reload
from types import MethodType
from unittest import TestCase, TextTestRunner, defaultTestLoader
from unittest.mock import MagicMock, patch

import core
from exceptions import RpcException

class ApiConnectionTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        reload(core)

    @patch('urllib.request.urlopen')
    def test_invoke_should_throw_on_invalid_status(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.msg = 'Error message'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        
        with self.assertRaises(Exception) as error:
            conn.invoke('IModule', 'Method', [])
        self.assertEqual(str(error.exception), 'Error message')

    @patch('urllib.request.urlopen')
    def test_invoke_should_throw_on_invalid_content(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'wrong'}
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        
        with self.assertRaises(Exception) as error:
            conn.invoke('IModule', 'Method', [])
        self.assertEqual(str(error.exception), 'Content type not supported: "wrong"')

    @patch('urllib.request.urlopen')
    def test_invoke_should_assemble_a_proper_query(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = '{"exception": null, "result": "null"}'
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        conn.sessionid = 'cica'
        conn.invoke('IModule', 'Method', [])

        (req,) = mock_urlopen.call_args[0]
        self.assertEqual(req.full_url, 'http://localhost:1986/api?module=IModule&method=Method&sessionid=cica')

    @patch('urllib.request.urlopen')
    def test_invoke_should_throw_RpcException_in_case_of_remote_exception(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = '{"exception": {"message": "cica", "data": {}}, "result": "null"}'
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        
        with self.assertRaises(RpcException) as error:
            conn.invoke('IModule', 'Method', [])
        self.assertEqual(str(error.exception), 'cica')

    @patch('urllib.request.urlopen')
    def test_invoke_should_return_the_result(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = '{"exception": null, "result": 3}'
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        conn.sessionid = 'cica'
        self.assertEqual(conn.invoke('IModule', 'Method', []), 3)

    @patch('urllib.request.urlopen')
    def test_create_api_should_throw_if_the_schema_cannot_be_found(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = '{}'
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        with self.assertRaises(Exception) as error:
            conn.create_api('IModule')
        self.assertEqual(str(error.exception), 'Schema could not be found')

    @patch('urllib.request.urlopen')
    def test_create_api_should_process_method_descriptors(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = '{"IModule": {"Methods": {"MethodA": {}}, "Properties": {}}}'
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        api = conn.create_api('IModule')
        self.assertTrue(hasattr(api, 'method_a'))
        self.assertIsInstance(api.method_a, MethodType)

    @patch('urllib.request.urlopen')
    def test_create_api_should_process_property_descriptors(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = '{"IModule": {"Methods": {}, "Properties": {"Prop": {"HasGetter": true, "HasSetter": false}}}}'
        mock_urlopen.return_value = mock_response

        reload(core)

        conn = core.ApiConnection('http://localhost:1986/api')
        api = conn.create_api('IModule')

        prop = getattr(api.__class__, 'prop', None)

        self.assertTrue(prop)
        self.assertIsInstance(prop, property)

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(defaultTestLoader.loadTestsFromTestCase(ApiConnectionTests))