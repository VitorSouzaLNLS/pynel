"""Pynel package."""

from . import data_test_fix
from . import misc_functions
from .buttons import Button
from .base import Base
from . import iterations

#from . import std_si_data
#from . import last_complete_pynel as completePynel

import os as _os
with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['Base', 'Button', 'misc_functions', 'iterations', 'data_test_fix']
