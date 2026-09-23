from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import Followup, User
from api.schemas import (
    FollowupCreate,
    FollowupResponse,
    FollowupStatusUpdate,
    FollowupUpdate
)
from api.enums import FollowupStatus

from api.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/followups",
    tags=["Followups"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/",
    response_model=FollowupResponse
)
def create_followup(
    followup: FollowupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_followup = Followup(
        customer_name=followup.customer_name,
        phone=followup.phone,
        date=followup.date,
        time=followup.time,
        property_id=followup.property_id,
        user_id=current_user.id,
        status=FollowupStatus.SCHEDULED
    )

    db.add(new_followup)

    db.commit()

    db.refresh(new_followup)

    return new_followup


@router.get(
    "/",
    response_model=list[FollowupResponse]
)
def get_followups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(Followup)
        .filter(Followup.user_id == current_user.id)
        .all()
    )


@router.patch(
    "/{followup_id}/status",
    response_model=FollowupResponse
)
def update_followup_status(
    followup_id: int,
    data: FollowupStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    followup = (
        db.query(Followup)
        .filter(
            Followup.id == followup_id,
            Followup.user_id == current_user.id
        )
        .first()
    )

    if not followup:

        raise HTTPException(
            status_code=404,
            detail="Followup not found."
        )

    followup.status = data.status

    db.commit()

    db.refresh(followup)

    return followup



@router.patch("/{followup_id}",response_model=FollowupResponse)
def update_followup(
    followup_id: int,
    data: FollowupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    followup = (
        db.query(Followup)
        .filter(
            Followup.id == followup_id,
            Followup.user_id == current_user.id
        )
        .first()
    )

    if not followup:
        raise HTTPException(
            status_code=404,
            detail="Followup not found."
        )

    followup.date = data.date
    followup.time = data.time

    db.commit()

    db.refresh(followup)

    return followup
