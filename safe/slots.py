# -*- encoding: utf-8 -*-

##    slots.py - checking of class slots
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

from abc import ABCMeta

from .error import TypeSafetyError

class SlotTypeDescriptor:
    __slots__ = ('name', 'next_descriptor', 'type')
    def __init__(self, name, next_descriptor, type):
        self.name = name
        self.next_descriptor = next_descriptor
        self.type = type

    def __get__(self, obj, type):
        return self.next_descriptor.__get__(obj, type)

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            raise TypeSafetyError(name=self.name, proper=self.type, actual=type(value))
        self.next_descriptor.__set__(obj, value)

    def __delete__(self, obj):
        raise AttributeError('Attempt to delete attribute ' + self.name)

class Meta(type):
    ''' A metaclass for type-safety of attributes
    '''
    def __call__(self, *args, **kwargs):
        ''' calls __new__ and __init__ and return the new object instance
        '''
        rv = type.__call__(self, *args, **kwargs)
        for s in self.__slots__:
            getattr(rv, s)
        return rv

    def __init__(scls, name, bases, dict):
        ''' Initialize a new safe class
        '''
        type.__init__(scls, name, bases, dict)
        for k, v in scls.__slots__.items():
            current_descriptor = getattr(scls, k)
            new_descriptor = SlotTypeDescriptor(k, current_descriptor, v)
            setattr(scls, k, new_descriptor)

    def __repr__(self):
        return type.__repr__(self).replace('<', '<safe ')
