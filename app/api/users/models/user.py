"""
DB - User model.
"""

# Base model
from api.utils.models import MosyneModel

# Tortoise ORM
from tortoise import fields


class User(MosyneModel):
    """User model. aka `Guardian`

    Make reference to any user of application.
    The main class is a guardian, the person who
    take care of an angel.
    """

    email = fields.CharField(
        max_length=80,
        unique=True,
        index=True,
        description="User email address.",
    )

    password = fields.CharField(
        max_length=80,
        description="User hashed password.",
    )

    is_verified = fields.BooleanField(
        default=False,
        description="Indicates if user email is verified.",
    )

    firstname = fields.CharField(max_length=54)
    lastname = fields.CharField(max_length=54)

    phone = fields.CharField(
        max_length=16,
        description="User phone number.",
        default="",
    )

    cel = fields.CharField(
        max_length=16,
        description="User mobile number.",
        default="",
    )

    photo = fields.CharField(
        max_length=516,
        description="Url to user photo.",
        default="",
    )

    address = fields.OneToOneField(
        model_name="models.Address",
        on_delete=fields.CASCADE,
        description="FK to user address",
    )

    class Meta:
        """Meta info."""

        table = "users"
