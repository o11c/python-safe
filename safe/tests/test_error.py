import unittest

from safe import TypeSafetyError

class TestError(unittest.TestCase):
    def test_error(self):
        with self.assertRaisesRegex(TypeSafetyError, '^foo should be a str, not a int$'):
            raise TypeSafetyError(name='foo', proper=str, actual=int)
