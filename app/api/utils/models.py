"""
Mosyne base model.
"""

# DB - Tortoise
from tortoise import fields, models


class MosyneModel(models.Model):
    """Mosyne base model.

    All models inherit from this model and set
    trhee fields:

    - id - The pk represented by UUID v4 string.
    - created - The creation datetime.
    - updated - The datetime of latest update.
    """

    id = fields.UUIDField(pk=True)

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    class Meta:
        """Meta info."""

        abstract = True
        ordering = ["-created", "-updated"]

    class PydanticMeta:
        """Pydantic meta settings.

        Add query properties:

        - max_recursion: Automatic fetch all related fields
        with one level of deep.
        """

        max_recursion = 1
