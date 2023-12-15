"""Pynel package.

---> Misalign_analysis package.
"""

import os as _os

from . import fitting, functions as functions, si_data
from .base import Base
from .buttons import Button

with open(_os.path.join(__path__[0], "VERSION"), "r") as _f:
    __version__ = _f.read().strip()

__all__ = ["Base", "Button", "functions", "fitting", "si_data"]
