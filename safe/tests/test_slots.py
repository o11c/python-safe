import unittest

from safe import TypeSafetyError, meta

class TestMeta(unittest.TestCase):
    def test_repr(self):
        class Foo(metaclass=meta):
            __slots__ = {}
        self.assertEqual(repr(Foo), "<safe class 'safe.tests.test_slots.Foo'>")

    def test_init(self):
        class Foo(metaclass=meta):
            __slots__ = {'x': int}
        with self.assertRaises(AttributeError):
            Foo()

    def test_external(self):
        class Foo(metaclass=meta):
            __slots__ = {'x': int, 'y': str}
            def __init__(self, x, y):
                self.x = x
                self.y = y

        foo = Foo(0, 'hi')

        self.assertEqual(foo.x, 0)
        self.assertEqual(foo.y, 'hi')

        with self.assertRaises(AttributeError):
            del foo.x

        with self.assertRaises(TypeSafetyError):
            foo.x = 'lo'
