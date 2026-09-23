from pydantic import BaseModel, Field


class SearchPropertiesInput(BaseModel):
    location: str = Field(
        default=None,
        description="The location where the customer wants to buy a property."
    )

    bedrooms: int | None = Field(
        default=None,
        description="The number of bedrooms the customer wants."
    )

    max_price: float | None = Field(
        default=None,
        description="The maximum budget of the customer."
    )


class GetPropertyDetailsInput(BaseModel):
    property_id: int = Field(
        description="The ID of the property."
    )


class CreateLeadInput(BaseModel):
    name: str = Field(
        description="The customer's full name."
    )

    phone: str = Field(
        description=(
            "The customer's Egyptian mobile phone number. "
            "It must contain exactly 11 digits and start with "
            "010, 011, 012, or 015."
        ),
        pattern=r"^01[0125][0-9]{8}$"
    )

    property_id: int = Field(
        description="The ID of the property."
    )






class ScheduleFollowupInput(BaseModel):

    customer_name: str = Field(
        description="The customer's name."
    )

    phone: str = Field(
        description="The customer's phone number."
    )

    date: str = Field(
        description="The follow-up date in YYYY-MM-DD format."
    )

    time: str = Field(
        description="The follow-up time in HH:MM format."
    )

    property_id: int | None = Field(
        default=None,
        description=(
            "The property ID related to the follow-up. "
            "Optional. Use it when the follow-up is related "
            "to a specific property."
        )
    )

class UpdateFollowupInput(BaseModel):
    followup_id: int = Field(
        description="The ID of the follow-up to update."
    )

    date: str = Field(
        description="The new follow-up date in YYYY-MM-DD format."
    )

    time: str = Field(
        description="The new follow-up time in HH:MM format."
    )