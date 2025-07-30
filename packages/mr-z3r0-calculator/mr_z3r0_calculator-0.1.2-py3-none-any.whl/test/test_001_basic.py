
import unittest

from src.basic import add_numbers


class Test001Basic(unittest):

    def test_001_add_numbers(self):
        self.assertEquals(add_numbers(1,2), 3)