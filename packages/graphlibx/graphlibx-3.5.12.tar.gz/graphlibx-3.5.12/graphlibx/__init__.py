"""
graphlibx
========

graphlibx is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

See https://graphlibx.org for complete documentation.
"""

__version__ = "3.5.12"


# These are imported in order as listed
from graphlibx.lazy_imports import _lazy_import

from graphlibx.exception import *

from graphlibx import utils
from graphlibx.utils import _clear_cache, _dispatchable

# load_and_call entry_points, set configs
config = utils.backends._set_configs_from_environment()
utils.config = utils.configs.config = config  # type: ignore[attr-defined]

from graphlibx import classes
from graphlibx.classes import filters
from graphlibx.classes import *

from graphlibx import convert
from graphlibx.convert import *

from graphlibx import convert_matrix
from graphlibx.convert_matrix import *

from graphlibx import relabel
from graphlibx.relabel import *

from graphlibx import generators
from graphlibx.generators import *

from graphlibx import readwrite
from graphlibx.readwrite import *

# Need to test with SciPy, when available
from graphlibx import algorithms
from graphlibx.algorithms import *

from graphlibx import linalg
from graphlibx.linalg import *

from graphlibx import drawing
from graphlibx.drawing import *


def __getattr__(name):
    if name == "random_tree":
        raise AttributeError(
            "nx.random_tree was removed in version 3.4. Use `nx.random_labeled_tree` instead.\n"
            "See: https://graphlibx.org/documentation/latest/release/release_3.4.html"
        )
    raise AttributeError(f"module 'graphlibx' has no attribute '{name}'")
