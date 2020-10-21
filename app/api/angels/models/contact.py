"""
DB - Contact model.
"""

# Base model
from api.utils.models import MosyneModel

# Tortoise ORM
from tortoise import fields

# Enums
from .enums import RELATION


class Contact(MosyneModel):
    """Angel contact model.

    Represents all angel emergencie contacts.
    """

    angel = fields.ForeignKeyField(
        model_name="models.Angel",
        related_name="contacts",
        on_delete=fields.CASCADE,
    )

    angel_relation = fields.CharEnumField(
        enum_type=RELATION,
        max_length=10,
        description="The relation between the angel and contact.",
    )

    name = fields.CharField(
        max_length=80,
        description="Contact name",
    )

    phone = fields.CharField(
        max_length=16,
        description="Contact phone number.",
    )

    cel = fields.CharField(
        max_length=16,
        description="Contact mobile number.",
    )

    class Meta(MosyneModel.Meta):
        """Meta info."""

        table = "contacts"
        abstract = False

    class PydanticMeta:
        """Pydantic config."""

        max_recursion = 0
