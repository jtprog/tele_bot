from unittest import TestCase

from apis.cbrf import str_to_float


class CBRFTestCase(TestCase):

    def test_str_to_float_int(self):
        r = str_to_float('1')
        self.assertEqual(r, 1.0)

    def test_str_to_float_real(self):
        r = str_to_float('1,23')
        self.assertEqual(r, 1.23)

    def test_str_to_float(self):
        r = str_to_float('2.34')
        self.assertEqual(r, 2.34)
