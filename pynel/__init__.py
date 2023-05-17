"""Pynel package."""

from . import last_complete_pynel as ModuleTest

import os as _os
from . import misc_functions
from . import std_si_data
from . import buttons
from . import base
from . import iterations

with open(_os.path.join(__path__[0], 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()

__all__ = ['base', 'buttons', 'std_si_data', 'misc_functions', 'iterations']
