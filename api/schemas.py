from pydantic import BaseModel, Field,EmailStr
from datetime import date, time

from api.enums import (
    PropertyStatus,
    LeadStatus,
    FollowupStatus
)


# =========================
# Property
# =========================

class PropertyResponse(BaseModel):

    id: int

    location: str

    bedrooms: int

    price: float

    area: float

    payment_plan: str

    status: PropertyStatus

    class Config:
        from_attributes = True


# =========================
# Lead
# =========================

class LeadCreate(BaseModel):

    name: str

    phone: str = Field(
        pattern=r"^01[0125][0-9]{8}$"
    )

    property_id: int


class LeadResponse(BaseModel):

    id: int

    name: str

    phone: str

    property_id: int

    status: LeadStatus

    class Config:
        from_attributes = True


# =========================
# Followup
# =========================

class FollowupCreate(BaseModel):

    customer_name: str

    phone: str = Field(
        pattern=r"^01[0125][0-9]{8}$"
    )

    date: date

    time: time

    property_id: int | None = None


class FollowupResponse(BaseModel):

    id: int

    customer_name: str

    phone: str

    date: date

    time: time

    property_id: int | None

    status: FollowupStatus

    class Config:
        from_attributes = True


class LeadStatusUpdate(BaseModel):

    status: LeadStatus
class FollowupStatusUpdate(BaseModel):

    status: FollowupStatus


class FollowupUpdate(BaseModel):
    date: date
    time: time

class ChatRequest(BaseModel):

    message: str

  


class ChatResponse(BaseModel):

    message: str

    thread_id: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str=Field(
        min_length=8,
        description="Password must be at least 8 characters long."
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

