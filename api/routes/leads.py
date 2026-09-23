# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from api.database import SessionLocal
# from api.models import Lead, Property, User
# from api.schemas import LeadCreate, LeadResponse, LeadStatusUpdate
# from api.enums import (
#     LeadStatus,
#     PropertyStatus
# )

# from api.dependencies.auth import get_current_user


# router = APIRouter(
#     prefix="/leads",
#     tags=["Leads"]
# )


# def get_db():

#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()


# @router.post(
#     "/",
#     response_model=LeadResponse
# )
# def create_lead(
#     lead: LeadCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):

#     property = (
#         db.query(Property)
#         .filter(Property.id == lead.property_id)
#         .first()
#     )

#     if not property:

#         raise HTTPException(
#             status_code=404,
#             detail="Property not found."
#         )

#     if property.status == PropertyStatus.SOLD:

#         raise HTTPException(
#             status_code=400,
#             detail="This property has already been sold."
#         )

#     existing_lead = (
#         db.query(Lead)
#         .filter(
#             Lead.phone == lead.phone,
#             Lead.property_id == lead.property_id,
#             Lead.user_id == current_user.id
#         )
#         .first()
#     )

#     if existing_lead:

#         return existing_lead

#     new_lead = Lead(
#         name=lead.name,
#         phone=lead.phone,
#         property_id=lead.property_id,
#         user_id=current_user.id,
#         status=LeadStatus.NEW
#     )

#     db.add(new_lead)

#     db.commit()

#     db.refresh(new_lead)

#     return new_lead


# @router.get(
#     "/",
#     response_model=list[LeadResponse]
# )
# def get_leads(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):

#     return (
#         db.query(Lead)
#         .filter(Lead.user_id == current_user.id)
#         .all()
#     )


# @router.patch(
#     "/{lead_id}/status",
#     response_model=LeadResponse
# )
# def update_lead_status(
#     lead_id: int,
#     data: LeadStatusUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):

#     lead = (
#         db.query(Lead)
#         .filter(
#             Lead.id == lead_id,
#             Lead.user_id == current_user.id
#         )
#         .first()
#     )

#     if not lead:

#         raise HTTPException(
#             status_code=404,
#             detail="Lead not found."
#         )

#     lead.status = data.status

#     db.commit()

#     db.refresh(lead)

#     return lead


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import Lead, Property, User
from api.schemas import LeadCreate, LeadResponse, LeadStatusUpdate
from api.enums import (
    LeadStatus,
    PropertyStatus
)

from api.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/leads",
    tags=["Leads"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/",
    response_model=LeadResponse
)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    property = (
        db.query(Property)
        .filter(Property.id == lead.property_id)
        .first()
    )

    if not property:

        raise HTTPException(
            status_code=404,
            detail="Property not found."
        )

    if property.status == PropertyStatus.SOLD:

        raise HTTPException(
            status_code=400,
            detail="This property has already been sold."
        )

    existing_lead = (
        db.query(Lead)
        .filter(
            Lead.phone == lead.phone,
            Lead.property_id == lead.property_id,
            Lead.user_id == current_user.id
        )
        .first()
    )

    if existing_lead:

        return existing_lead

    new_lead = Lead(
        name=lead.name,
        phone=lead.phone,
        property_id=lead.property_id,
        user_id=current_user.id,
        status=LeadStatus.NEW
    )

    db.add(new_lead)

    db.commit()

    db.refresh(new_lead)

    return new_lead


@router.get(
    "/",
    response_model=list[LeadResponse]
)
def get_leads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(Lead)
        .filter(Lead.user_id == current_user.id)
        .all()
    )


@router.patch(
    "/{lead_id}/status",
    response_model=LeadResponse
)
def update_lead_status(
    lead_id: int,
    data: LeadStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id,
            Lead.user_id == current_user.id
        )
        .first()
    )

    if not lead:

        raise HTTPException(
            status_code=404,
            detail="Lead not found."
        )

    lead.status = data.status

    db.commit()

    db.refresh(lead)

    return lead