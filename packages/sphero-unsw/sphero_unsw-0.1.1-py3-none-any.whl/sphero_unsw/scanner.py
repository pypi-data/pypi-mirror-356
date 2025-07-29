"""
This module implements extended functionality of spherov2.scanner for Sphero BOLT+ to support Sphero BOLT+ robot.
"""


# ------------------------------------------------------------------------- #
# [1] Import necessary libraries
# ------------------------------------------------------------------------- #

# Import all necessary classes and functions from spherov2
from spherov2.scanner import *
# Import our new implementation of BOLTPLUS from our new library spherov2_boltplus3
from sphero_unsw.toy.boltplus import BOLTPLUS



# ------------------------------------------------------------------------- #
# [2] Create a new function to find toys of type BOLT+
# ------------------------------------------------------------------------- #
find_BOLTPLUS: Callable[..., BOLTPLUS] = partial(find_toy, toy_types=[BOLTPLUS])