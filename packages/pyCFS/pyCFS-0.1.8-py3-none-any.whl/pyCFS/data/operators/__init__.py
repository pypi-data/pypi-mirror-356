"""
pyCFS.data.operators
====================

Libraries to perform various operations on pyCFS.data objects.

Modules
-------
- interpolators
- modal_analysis
- projection_interpolation
- sngr
- transformation

"""

from . import interpolators  # noqa
from . import modal_analysis  # noqa
from . import projection_interpolation  # noqa
from . import sngr  # noqa
from . import transformation  # noqa

__all__ = [
    "interpolators",
    "modal_analysis",
    "projection_interpolation",
    "sngr",
    "transformation",
]
