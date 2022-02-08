# RPC.NET-Connector tests
# internals.py
# Author: Denes Solti

from unittest import TestCase

from pyconn.internals import _load_json, _snake_case

class InternalsTests(TestCase):
    def test_snake_case(self):
        for (str, expected) in [('cica', 'cica'), ('Cica', 'cica'), ('CicaMica', 'cica_mica'), ('cicaMica', 'cica_mica'), ('ABC', 'ABC'), ('PropB', 'prop_b'), ('dABC', 'd_ABC'), ('ABCd', 'ABC_d')]:
            with self.subTest():
                self.assertEqual(_snake_case(str), expected)

    def test_load_json(self):
        val = _load_json('{"Prop": 1, "PropB": {"ValA": 1986}, "propC": [{"propD": "cica"}]}')
        self.assertEqual(val.prop, 1)
        self.assertEqual(val.prop_b.val_a, 1986)
        self.assertEqual(val.prop_c[0].prop_d, 'cica')
