import unittest

import safe

class TestError(unittest.TestCase):
    def test_error(self):
        with self.assertRaisesRegex(safe.TypeSafetyError, '^foo should be a str, not a int$'):
            raise safe.TypeSafetyError(field_name='foo', proper_type=str, actual_type=int)
