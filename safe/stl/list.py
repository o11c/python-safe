from safe import template, checked, TypeSafetyError

# TODO implement this properly
iterable = object

@template
def List(T: type):
    @checked
    class List:
        __slots__ = {'_impl': list}

        def __init__(self, arg: iterable = None) -> type(None):
            if arg is None:
                self._impl = []
            else:
                l = self._impl = list(arg)
                for e in l:
                    if not isinstance(e, T):
                        raise TypeSafetyError(name='list element', proper=T, actual=type(e))

        def __getitem__(self, idx:int) -> T:
            return self._impl[idx]

        def __setitem__(self, idx:int, val:T) -> type(None):
            self._impl[idx] = val

        def __len__(self) -> int:
            return len(self._impl)
    return List
