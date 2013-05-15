import unittest

from safe import template, Meta, TypeSafetyError

class TestTemplate(unittest.TestCase):
    def test_ident(self):
        @template
        def Same(*T):
            class Same:
                pass
            return Same
        self.assertIs(Same[int], Same[int])
        self.assertIs(Same[Same[str]], Same[Same[str]])
        self.assertIsNot(Same[int], Same[str])

        value = Same[int]()
        self.assertIsInstance(value, Same[int])
        self.assertNotIsInstance(value, Same[str])

    def test_name(self):
        @template
        def Named(A):
            class Named:
                pass
            return Named
        self.assertEqual(Named[int].__name__, 'Named[int]')
        self.assertEqual(Named[0].__name__, 'Named[0]')

    def test_safe(self):
        @template
        def Wrapper(T):
            class Wrapper(metaclass=Meta):
                ''' Just hold a T
                '''
                __slots__ = {'value': T}
                def __init__(self, v):
                    self.value = v
            return Wrapper

        my_int = Wrapper[int](0)
        with self.assertRaises(TypeSafetyError):
            my_int.value = 'oops'
        my_int.value = 1
