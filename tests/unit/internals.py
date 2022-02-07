# RPC.NET-Connector tests
# internals.py
# Author: Denes Solti

from unittest import TestCase

from pyconn.internals import _load_json, _snake_case

class InternalsTests(TestCase):
    def test_snake_case(self):
        self.assertEqual(_snake_case('cica'), 'cica')
        self.assertEqual(_snake_case('Cica'), 'cica')
        self.assertEqual(_snake_case('CicaMica'), 'cica_mica')
        self.assertEqual(_snake_case('cicaMica'), 'cica_mica')
        self.assertEqual(_snake_case('ABC'), 'ABC')
        self.assertEqual(_snake_case('PropB'), 'prop_b')
        self.assertEqual(_snake_case('dABC'), 'd_ABC')
        self.assertEqual(_snake_case('ABCd'), 'ABC_d')

    def test_load_json(self):
        val = _load_json('{"Prop": 1, "PropB": {"ValA": 1986}, "propC": [{"propD": "cica"}]}')
        self.assertEqual(val.prop, 1)
        self.assertEqual(val.prop_b.val_a, 1986)
        self.assertEqual(val.prop_c[0].prop_d, 'cica')
