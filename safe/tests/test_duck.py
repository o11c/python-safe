import unittest

from safe import Duck

class TestDuck(unittest.TestCase):
    def test_duck(self):
        class iterable(metaclass=Duck):
            def __iter__(self):
                pass
        class iterator(iterable):
            def __next__(self):
                pass

        class MyIterator:
            def __init__(self, value):
                self.value = value

            def __iter__(self):
                return self

            def __next__(self):
                if not self.value:
                    raise StopIteration
                self.value -= 1
                return self.value

        class MyIterable:
            def __init__(self, value):
                self.value = value

            def __iter__(self):
                return MyIterator(self.value)

        my_it = MyIterable(3)
        self.assertIsInstance(my_it, iterable)
        self.assertIsInstance(iter(my_it), iterable)
        self.assertIsInstance(iter(my_it), iterator)
        self.assertNotIsInstance(my_it, iterator)
        self.assertIsInstance([], iterable)
        self.assertIsInstance('hello', iterable)
        self.assertIsInstance((x for x in []), iterable)
