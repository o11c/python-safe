import unittest

from safe import TypeSafetyError
from safe.stl import List

class TestList(unittest.TestCase):
    def test_init(self):
        List[int]([0, 1, 2])

        with self.assertRaises(TypeSafetyError):
            List[int](['hello'])

    def test_item(self):
        ls = List[str]('abc def ghi'.split())
        self.assertEqual(ls[0], 'abc')
        ls[1] = 'xyz'
        self.assertEqual(ls[1], 'xyz')

        with self.assertRaises(TypeSafetyError):
            ls[2] = None

    def test_len(self):
        self.assertEqual(len(List[int]()), 0)
        self.assertEqual(len(List[int]([1, 2, 3])), 3)
