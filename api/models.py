from sqlalchemy import Column, Integer, String, Float, Enum,Date,Time,DateTime,ForeignKey
from api.database import Base
from api.enums import PropertyStatus, LeadStatus, FollowupStatus
from datetime import datetime
from sqlalchemy.orm import relationship
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    area = Column(Float, nullable=False)
    payment_plan = Column(String, nullable=False)

    status = Column(
        Enum(PropertyStatus),
        nullable=False,
        default=PropertyStatus.AVAILABLE
    )


class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    property_id = Column(Integer, nullable=False)

    status = Column(
        Enum(LeadStatus),
        nullable=False,
        default=LeadStatus.NEW
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_leads_user_id_users"),
        nullable=False
    )
    # Define the relationship to the User model


    user = relationship(
        "User",
        back_populates="leads"
    )

    
class Followup(Base):

    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    date = Column(Date, nullable=False)

    time = Column(Time, nullable=False)

    property_id = Column(Integer, nullable=True)

    status = Column(
        Enum(FollowupStatus),
        nullable=False,
        default=FollowupStatus.SCHEDULED
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_followups_user_id_users"),
        nullable=False
    )
    user = relationship(
        "User",
        back_populates="followups"
    )
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    leads = relationship(
        "Lead",
        back_populates="user"
    )

    followups = relationship(
        "Followup",
        back_populates="user"
    )


