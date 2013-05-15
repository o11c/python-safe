# -*- encoding: utf-8 -*-

##    duck.py - a metaclass to check duck-typing
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

from types import FunctionType

class Duck(type):
    def __call__(self, *args, **kwargs):
        raise TypeError('Duck types cannot be directly instantiated')

    def __instancecheck__(self, instance):
        rv = True
        for cls in self.mro():
            for name, value in cls.__dict__.items():
                if not isinstance(value, FunctionType):
                    continue
                has = getattr(instance, name, None) is not None
                rv = rv and has
        return rv
