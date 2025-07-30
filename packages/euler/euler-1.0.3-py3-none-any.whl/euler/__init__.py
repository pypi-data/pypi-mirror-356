"""A library for Euler angle computation and conversion."""

__version__ = "1.0.3"

from .utils import AxisTriple, AXIS_TRIPLES
from .matrix import *  # noqa
from .angles import *  # noqa
from .convert import *  # noqa
from .su2 import * # noqa

__all__ = (
    ("AxisTriple", "AXIS_TRIPLES", "matrix", "angles", "convert")  # noqa
    + ("su2_to_so3", "so3_to_su2")
    + tuple(f"matrix_{p}" for p in AXIS_TRIPLES)
    + tuple(f"angles_{p}" for p in AXIS_TRIPLES)
    + tuple(f"convert_{p}_{q}" for p in AXIS_TRIPLES for q in AXIS_TRIPLES)
)
