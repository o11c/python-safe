# -*- encoding: utf-8 -*-

##    templates.py - allow generic copies of a class
##
##    Copyright © 2013 Ben Longbons <b.r.longbons@gmail.com>
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

from weakref import WeakValueDictionary

class template:
    ''' Decorator for template classes.

        Basically just does a cache.
    '''
    __slots__ = ('factory', 'cache')
    def __init__(self, factory):
        self.factory = factory
        self.cache = WeakValueDictionary()

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (args,)
        try:
            return self.cache[args]
        except KeyError:
            rv = self.cache[args] = self.factory(*args)
            argnames = ', '.join([
                (arg.__name__
                    if isinstance(arg, type)
                    else str(arg)
                ) for arg in args
            ])
            rv.__name__ = '%s[%s]' % (self.factory.__name__, argnames)
            return rv
