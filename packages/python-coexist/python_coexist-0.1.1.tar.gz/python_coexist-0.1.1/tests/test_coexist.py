import unittest

from coexist import coexist


class TestCoexist(unittest.TestCase):
    def test_positive_coexist_execution(self):
        with coexist(max_workers=None) as pl:
            pl(lambda: print('Hello'))
            pl(lambda: print('World'))

    def test_negative_coexist_execution(self):
        try:
            with coexist(max_workers=None) as pl:
                pl(print('TypeError'))  # noqa
        except TypeError:
            pass
        else:
            raise AssertionError('TypeError not raised as expected')

    def test_coexist_max_workers(self):
        with coexist(max_workers=5) as pl:
            pl(lambda: print('Hello World'))
