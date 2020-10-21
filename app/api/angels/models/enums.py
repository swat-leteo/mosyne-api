"""
Enums - Angel enums.
"""

# Built in
from enum import Enum


class RELATION(str, Enum):
    """Familiar relation."""

    son = "hijo"
    daugther = "hija"
    mom = "madre"
    dad = "padre"
    grandma = "abuela"
    grandpa = "abuelo"
    friend = "amig@"
    uncle = "tio"
    aunt = "tia"
    cousin = "prim@"
    other = "other"


class BLOOD_TYPE(str, Enum):
    """Blood type."""

    An = "A-"
    Ap = "A+"
    Bn = "B-"
    Bp = "B+"
    ABn = "AB-"
    ABp = "AB+"
    On = "O-"
    Op = "O+"


class DETONANT(str, Enum):
    """Detonant angel suffering type."""

    depression = "depression"
    neurological = "neurological"
