# RPC.NET-Connector integration tests
# tests.py
# Author: Denes Solti

from io import TextIOWrapper
from math import pi
from os import getcwd, path
from subprocess import CREATE_NEW_CONSOLE, PIPE, Popen
from unittest import TestCase, TextTestRunner, defaultTestLoader

from core import ApiConnection
from exceptions import RpcException

class IntergrationTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._proc = Popen([path.join(getcwd(), '.tmp', 'backend', 'Solti.Utils.Rpc.Server.Sample.exe')], stdout=PIPE, creationflags=CREATE_NEW_CONSOLE)
        for line in TextIOWrapper(cls._proc.stdout, encoding="utf-8"):
            if line.startswith('Server is running'):
                break

    @classmethod
    def tearDownClass(cls):
        cls._proc.terminate()

    def test_api(self):
        api = ApiConnection('http://localhost:1986/api').create_api('ICalculator')
        self.assertEqual(api.add(1, 2), 3)
        self.assertEqual(api.parse_int('1986'), 1986)
        self.assertAlmostEqual(api.PI, pi)
        with self.assertRaises(Exception) as error:
            api.parse_int('invalid')
        self.assertEqual(str(error.exception), 'Input string was not in a correct format.')

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(defaultTestLoader.loadTestsFromTestCase(IntergrationTests))