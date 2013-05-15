# -*- encoding: utf-8 -*-

##    args.py - Checking of function arguments
##
##    Copyright © 2012-2013 Ben Longbons <b.r.longbons@gmail.com>
##
##    This file is part of The Mana World (Athena server)
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inspect
from types import FunctionType

from .error import TypeSafetyError

def checked(a):
    if isinstance(a, type):
        return checked_class(a)
    if isinstance(a, FunctionType):
        return checked_function(a)

    assert False, 'Can only check functions and classes'

def checked_function(fn):
    ''' Decorator for type-checked arguments.

        Creates a new function that mimics the old one.
    '''
    spec = inspect.getfullargspec(fn)
    for name in fn.__code__.co_varnames:
        spec.annotations[name]
    spec.annotations['return']

    # lambda capture spec
    def check(*args, **kwargs):
        ''' Check types of arguments for captured function

            raises TypeError if any of them is invalid
        '''
        # explicit iterators so we can deal with the post-zip
        ai = iter(args)
        pni = iter(spec.args)
        for pn, a in zip(pni, ai):
            t = spec.annotations[pn]
            if not isinstance(a, t):
                raise TypeSafetyError(name='Argument %s(%s)' % (fn.__name__, pn), proper=t, actual=type(a))

        if spec.varargs is not None:
            t = spec.annotations[spec.varargs]
            for a in ai:
                if not isinstance(a, t):
                    raise TypeSafetyError(name='Variadic argument %s(*%s)' % (fn.__name__, spec.varargs), proper=t, actual=type(a))
        else:
            x = list(ai)
            if x:
                raise TypeError('%s() takes %d argument(s) (%d given)' % (func.__name__, len(spec.args), len(spec.args) + len(x)))
        if list(pni):
            pass # positional arguments omitted, need to check as keywords or defaults
        # we also don't check whether omitted keyword-only arguments have defaults

        if spec.varkw is not None:
            kt = spec.annotations[spec.varkw]
        else:
            kt = None
        for k, v in kwargs.items():
            t = spec.annotations.get(k, kt)
            if t is None:
                raise TypeError("%s() got an unexpected keyword argument '%s'" % (fn.__name__, k))
            if not isinstance(v, t):
                raise TypeSafetyError(name='Keyword argument %s(%s=)' % (fn.__name__, k), proper=t, actual=type(v))
        return
    # function check

    # lambda capture fn, check
    def inner(*args, **kwargs):
        check(*args, **kwargs)
        rv = fn(*args, **kwargs)
        # xrt = a.get('return', object)
        xrt = spec.annotations['return']
        if not isinstance(rv, xrt):
            raise TypeSafetyError(name='%s()->return' % fn.__name__, proper=xrt, actual=type(rv))
        return rv
    inner.__name__ = fn.__name__
    inner.__doc__ = fn.__doc__
    # expose, to be able to check without calling
    inner.check_args = check
    return inner

def checked_class(cls):
    ''' Add type-checkers to all of a class's methods.

        Requires first adjusting their annotations.
    '''
    for name, func in vars(cls).items():
        if not isinstance(func, FunctionType):
            continue
        assert 'self' not in func.__annotations__
        if 'self' == func.__code__.co_varnames[0]:
            func.__annotations__['self'] = cls
        setattr(cls, name, checked_function(func))
    return cls
