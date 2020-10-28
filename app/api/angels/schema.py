"""
Schemas - Angel Schemas
"""

# Pydantic
from pydantic.contrib.pydantic import pydantic_model_creator

# Enums
from .models import Angel, Contact

##################
# Angels Schemas #
##################

AngelDto = pydantic_model_creator(Angel, exclude=("guardian",))


class AngelCreateDto(AngelDto):
    """The same fields."""


ContactDto = pydantic_model_creator(Contact, exclude=("angel",))
