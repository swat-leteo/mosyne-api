"""
DB - Contact model.
"""

# Enums
from api.angels.enums import RELATION

# Base model
from api.utils.models import MosyneModel

# Tortoise ORM
from tortoise import fields


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

    class Meta:
        """Meta info."""

        table = "contacts"

    class PydanticMeta:
        """Pydantic config."""

        max_recursion = 0
