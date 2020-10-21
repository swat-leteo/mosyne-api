"""
DB - Angel model.
"""

# Base model
from api.utils.models import MosyneModel

# Tortoise ORM
from tortoise import fields

# Enums
from .enums import BLOOD_TYPE, DETONANT, RELATION


class Angel(MosyneModel):
    """Angel model.

    Make reference to the person with Alzheimer
    or another related suffering.
    """

    guardian = fields.ForeignKeyField(
        model_name="models.User",
        related_name="angels",
        on_delete=fields.CASCADE,
        description="The person who take care of the angel.",
    )

    guardian_relation = fields.CharEnumField(
        enum_type=RELATION,
        max_length=10,
        description="The relation between the angel and guardian.",
    )

    firstname = fields.CharField(max_length=54)
    lastname = fields.CharField(max_length=54)
    nationality = fields.CharField(max_length=30)
    about = fields.CharField(max_length=30, null=True)

    address = fields.OneToOneField(
        model_name="models.Address",
        on_delete=fields.CASCADE,
        description="FK to user address.",
    )

    living_alone = fields.BooleanField(
        default=False,
        description="Indicate if the angel live alone.",
    )

    suffering = fields.CharField(
        max_length=30,
        default="Alzheimer",
        description="The angel suffering.",
    )

    blood_type = fields.CharEnumField(enum_type=BLOOD_TYPE, max_length=3)
    health_info = fields.TextField(null=True)

    surgeries = fields.JSONField(default=[])
    alergies = fields.JSONField(default=[])
    medicines = fields.JSONField(default=[])

    detonant = fields.CharEnumField(
        max_length=30,
        enum_type=DETONANT,
        description="The suffering detonant.",
    )

    diabetes = fields.BooleanField(
        default=False,
        description="Indicate if the angel suffer diabetes.",
    )

    hypertension = fields.BooleanField(
        default=False,
        description="Indicate if the angel suffer hypertension.",
    )

    class Meta:
        """Meta info."""

        table = "angel_profile"
