''' The 'safe' package is a way of checking, at runtime, for errors related
    to types in Python3 code.

    Everything important is imported into the top-level __init__ file;
    modules within this package are just for better source control.
'''
from .error import TypeSafetyError
from .args import checked
from .slots import Meta
from .templates import template
from .duck import Duck
