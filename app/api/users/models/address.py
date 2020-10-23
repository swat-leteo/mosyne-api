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

    city = fields.CharField(max_length=54, default="")

    municipality = fields.CharField(
        max_length=54,
        description="User municipality ref to: `Municipio/delegación`",
        default="",
    )

    neighborhood = fields.CharField(
        max_length=54,
        description="User neighborhood ref to: `Colonia`",
        default="",
    )

    street = fields.CharField(max_length=54, default="")
    num_int = fields.CharField(max_length=5, default="")
    num_ext = fields.CharField(max_length=5, default="")

    cp = fields.CharField(max_length=8, description="Postal code", default="")

    class Meta:
        """Meta info."""

        table = "address"
