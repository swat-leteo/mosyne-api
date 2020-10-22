"""
DB - Address model.
"""

# Base model
from api.utils.models import MosyneModel

# Tortoise ORM
from tortoise import fields


class Address(MosyneModel):
    """Address model.

    Make reference to any user (guardian or angel) address.
    """

    city = fields.CharField(max_length=54)

    municipality = fields.CharField(
        max_length=54,
        description="User municipality ref to: `Municipio/delegación`",
    )

    neighborhood = fields.CharField(
        max_length=54,
        description="User neighborhood ref to: `Colonia`",
    )

    street = fields.CharField(max_length=54)
    num_int = fields.CharField(max_length=5)
    num_ext = fields.CharField(max_length=5)

    cp = fields.CharField(max_length=8, description="Postal code")

    class Meta:
        """Meta info."""

        table = "address"
