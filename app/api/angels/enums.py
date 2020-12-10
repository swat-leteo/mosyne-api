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
    grandchild = "nieto"
    granddaugther = "nieta"
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


class NATIONALITY(str, Enum):
    Argentina = "Argentina"
    Bolivia = "Boliviana"
    Chile = "Chilena"
    Guatemala = "Gautemalteca"
    Honduras = "Hondureña"
    Mexico = "Mexicana"
    Panama = "Panameña"
    Peru = "Peruana"
    Spain = "Española"
    Venezuela = "Venezolana"
