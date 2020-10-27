"""
Schemas - Angel Schemas
"""
# models

from users.models import User

# Enums
from .enums import Countries,DETONANT,BLOOD_TYPE,RELATION

# Pydantic
from pydantic import BaseModel, Field

################
# Angels Schemas #
################

class AddNewAngelInfo(BaseModel):
    """Add New Angel Information.
    
    Validate the infomation that users
    bring about their angels and their 
    suffers.

    """

    guardian: User = Field(...) # I'm not secure about this
    guardian_relation: RELATION = Field(...)
    firstname: str = Field(...)
    lastname: str = Field(...)
    nationality: Countries = Field(...)
    about: Field(default="")
    address: str = Field(...)
    living_alone: bool = Field(default=False)
    suffering: str = Field(default="Alzheimer")
    blood_type: BLOOD_TYPE = Field(default = BLOOD_TYPE.ABn)
    health_info: str = Field(default="")
    surgeries: str = Field(default=[])
    alergies: str = Field(default=[])
    medicines: str = Field(default=[])
    detonant: DETONANT = Field(default=DETONANT.neurological)
    diabetes: bool = Field(default=False)
    hypertension: bool = Field(default=False)