from pydantic import BaseModel,Field # type: ignore
from typing import Optional, List



class UserInfo(BaseModel):
    age: int = Field(..., description="Age of the user in years", example=68)
    income: float = Field(..., description="Monthly income of the user in USD", example=1200.50)
    veteran_status: bool = Field(..., description="Is the user a military veteran?", example=True)
    disability_status: bool = Field(..., description="Does the user have a registered disability?", example=False)
    location: str = Field(..., description="User's residential location (state)", example="California")
    employement_status: str = Field(..., description="User's employement status", example="Retired")


class Scheme(BaseModel):
    scheme_id: str = Field(..., description="Unique ID of the scheme", example="SC001")
    name: str = Field(..., description="Name of the scheme", example="Senior Medicare Plan")
    description: str = Field(..., description="Details about the scheme")
    eligibility_criteria: str = Field(..., description="Eligibility criteria for this scheme")
