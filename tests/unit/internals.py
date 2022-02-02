# RPC.NET-Connector tests
# internals.py
# Author: Denes Solti

from unittest import TestCase

from pyconn.internals import _getprop

class InternalsTests(TestCase):
    def test_getprop_caseinsensitivity(self):
        dict = {'cica': 'mica'}
        self.assertEqual(_getprop(dict, 'CICA'), 'mica')
        self.assertEqual(_getprop(dict, 'cica'), 'mica')

    def test_getprop_ifnomatch(self):
        self.assertEqual(_getprop({}, 'x'), None)