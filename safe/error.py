# -*- encoding: utf-8 -*-

##    error.py - a specific exception type for typecheck violations
##
##    Copyright © 2012 Ben Longbons <b.r.longbons@gmail.com>
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

class TypeSafetyError(TypeError):
    __slots__ = ('field_name', 'actual_type', 'proper_type')
    def __init__(self, *, field_name, actual_type, proper_type):
        TypeError.__init__(self, '%s should be a %s, not a %s' % (field_name, proper_type.__name__, actual_type.__name__))
        self.field_name = field_name
        self.actual_type = actual_type
        self.proper_type = proper_type
