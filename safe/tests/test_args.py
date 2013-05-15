import unittest

from safe import checked, TypeSafetyError

class TestChecked(unittest.TestCase):
    def test_partial(self):
        with self.assertRaisesRegex(KeyError, "^'return'$"):
            @checked
            def foo():
                pass
        with self.assertRaisesRegex(KeyError, "^'x'$"):
            @checked
            def foo(x) -> str:
                pass
    def test_simple(self):
        @checked
        def foo() -> str:
            return ''
        foo()

        @checked
        def bar(x:str) -> str:
            return x
        bar('hello')

        with self.assertRaises(TypeSafetyError):
            bar(1)

        @checked
        def baz() -> str:
            return None

        with self.assertRaises(TypeSafetyError):
            baz()

    def test_more(self):
        @checked
        def foo(x:str, y:str='y') -> type(None):
            pass
        foo('x')
        foo('x', 'y')

        with self.assertRaises(TypeSafetyError):
            foo(1)
        with self.assertRaises(TypeSafetyError):
            foo('x', y=0)
        with self.assertRaises(TypeSafetyError):
            foo(x=0)

    def test_varargs(self):
        @checked
        def foo(first: int, *args:str) -> type(None):
            pass

        foo(0)
        foo(first=0)
        foo(0, 'x')
        foo(0, 'x', 'y')

        with self.assertRaises(TypeSafetyError):
            foo('x')
        with self.assertRaises(TypeSafetyError):
            foo(0, 1)
        with self.assertRaises(TypeSafetyError):
            foo(0, 1, 'a')
        with self.assertRaises(TypeSafetyError):
            foo(0, 'b', 1, 'a')

    def test_kwargs(self):
        @checked
        def foo(*, x:int, **kwargs: str) -> type(None):
            pass
        foo(x=0)
        foo(x=0, y='hello')
        foo(x=0, y='hello', z='happy')

        with self.assertRaises(TypeSafetyError):
            foo(x='goodbye')

        with self.assertRaises(TypeSafetyError):
            foo(x=1, y=0, z='sad')

        with self.assertRaises(TypeSafetyError):
            foo(x=1, y='sad', z=0)

    def test_attrs(self):
        @checked
        def foo() -> type(None):
            'docstring'

        self.assertEqual(foo.__name__, 'foo')
        self.assertEqual(foo.__doc__, 'docstring')

class TestClasses(unittest.TestCase):
    def test_normal(self):
        @checked
        class Foo:
            def __init__(self, value: int) -> type(None):
                self.value = value

        Foo(0)
        with self.assertRaises(TypeSafetyError):
            Foo('hello')

    def test_oops(self):
        with self.assertRaises(KeyError):
            @checked
            class Foo:
                def __init__(self):
                    'Missing -> return annotation'
