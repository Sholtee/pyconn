""" Contains tests against the `internals` module """

# RPC.NET-Connector tests
# internals_tests.py
# Author: Denes Solti

from unittest import TestCase, TextTestRunner, defaultTestLoader

from internals import _load_json, _snake_case

# pylint: disable=missing-class-docstring, missing-function-docstring
class InternalsTests(TestCase):
    def test_snake_case(self):
        for (input_str, expected_str) in [('cica', 'cica'), ('Cica', 'cica'), ('CicaMica', 'cica_mica'), ('cicaMica', 'cica_mica'), ('ABC', 'ABC'), ('PropB', 'prop_b'), ('dABC', 'd_ABC'), ('ABCd', 'ABC_d')]:
            with self.subTest():
                self.assertEqual(_snake_case(input_str), expected_str)

    def test_load_json(self):
        val = _load_json('{"Prop": 1, "PropB": {"ValA": 1986}, "propC": [{"propD": "cica"}]}')
        self.assertEqual(val.prop, 1)
        self.assertEqual(val.prop_b.val_a, 1986)
        self.assertEqual(val.prop_c[0].prop_d, 'cica')

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(defaultTestLoader.loadTestsFromTestCase(InternalsTests))
