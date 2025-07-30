"""
pyCFS.data.extras
=================

Library of modules to read from, convert to, and write in various formats.

This subpackage provides:

- Readers and writers for various mesh and result file formats.
- Conversion utilities to and from the CFS format.

Modules
-------
- ansys_io, ansys_to_cfs_element_types
- cgns_io, cgns_types
- ensight_io, vtk_types
- exodus_io, exodus_to_cfs_element_types
- nihu_io, nihu_types
- psv_io
- stl_io

Examples
--------
>>> from pyCFS.data import extras
>>> mesh = extras.cgns_io.read_mesh("example.cgns")
>>> mesh = extras.exodus_io.read_exodus("example.e")
>>> mesh, result = extras.ensight_io.convert_to_cfs("example.case", quantities=['quantity1'], region_dict={'region1': 'Region_1'})
>>> mesh = extras.stl_io.read_mesh("example.stl")
"""

import importlib.util

if importlib.util.find_spec("ansys") is not None:
    from . import ansys_io  # noqa
    from . import ansys_to_cfs_element_types  # noqa
if importlib.util.find_spec("vtk") is not None:
    from . import ensight_io  # noqa
    from . import vtk_types  # noqa
from . import cgns_io  # noqa
from . import cgns_types  # noqa
from . import exodus_io  # noqa
from . import exodus_to_cfs_element_types  # noqa
from . import nihu_io  # noqa
from . import nihu_types  # noqa
from . import psv_io  # noqa
from . import stl_io  # noqa

__all__ = [
    "cgns_io",
    "cgns_types",
    "exodus_io",
    "exodus_to_cfs_element_types",
    "nihu_io",
    "nihu_types",
    "psv_io",
    "stl_io",
]

if importlib.util.find_spec("ansys") is not None:
    __all__ += [
        "ansys_io",
        "ansys_to_cfs_element_types",
    ]
if importlib.util.find_spec("vtk") is not None:
    __all__ += [
        "ensight_io",
        "vtk_types",
    ]
