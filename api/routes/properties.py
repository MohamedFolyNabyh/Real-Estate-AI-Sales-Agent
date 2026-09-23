from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import Property
from api.schemas import PropertyResponse
from api.enums import PropertyStatus


router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=list[PropertyResponse]
)
def get_properties(
    location: str | None = None,
    bedrooms: int | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Property)

    # Only available properties
    query = query.filter(
        Property.status == PropertyStatus.AVAILABLE
    )

    if location:

        query = query.filter(
            Property.location.ilike(f"%{location}%")
        )

    if bedrooms:

        query = query.filter(
            Property.bedrooms == bedrooms
        )

    if max_price:

        query = query.filter(
            Property.price <= max_price
        )

    return query.all()


@router.get(
    "/{property_id}",
    response_model=PropertyResponse
)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):

    property = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if not property:

        raise HTTPException(
            status_code=404,
            detail="Property not found."
        )

    return property