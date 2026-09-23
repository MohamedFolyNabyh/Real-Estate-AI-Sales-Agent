from datetime import date, time, timedelta

from api.database import SessionLocal
from api.models import (
    User,
    Property,
    Lead,
    Followup,
)
from api.enums import (
    PropertyStatus,
    LeadStatus,
    FollowupStatus,
)


# =========================================================
# Database
# =========================================================

db = SessionLocal()


# =========================================================
# Get User
# =========================================================

user = db.query(User).first()

if not user:
    print("No users found.")
    print("Please create a user first.")
    db.close()
    exit()


print(f"Using user: {user.name} - ID: {user.id}")


# =========================================================
# Properties Data
# =========================================================

properties_data = [

    {
        "location": "Cairo",
        "bedrooms": 2,
        "price": 2500000,
        "area": 120,
        "payment_plan": "10% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Cairo",
        "bedrooms": 3,
        "price": 3800000,
        "area": 155,
        "payment_plan": "15% down payment - 6 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Cairo",
        "bedrooms": 3,
        "price": 4200000,
        "area": 165,
        "payment_plan": "10% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Cairo",
        "bedrooms": 4,
        "price": 6500000,
        "area": 210,
        "payment_plan": "20% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Nasr City",
        "bedrooms": 2,
        "price": 2200000,
        "area": 115,
        "payment_plan": "10% down payment - 5 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Nasr City",
        "bedrooms": 3,
        "price": 3100000,
        "area": 145,
        "payment_plan": "15% down payment - 6 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Maadi",
        "bedrooms": 3,
        "price": 4500000,
        "area": 170,
        "payment_plan": "20% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Maadi",
        "bedrooms": 4,
        "price": 6800000,
        "area": 230,
        "payment_plan": "20% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "6th of October",
        "bedrooms": 2,
        "price": 1900000,
        "area": 110,
        "payment_plan": "10% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "6th of October",
        "bedrooms": 3,
        "price": 2800000,
        "area": 150,
        "payment_plan": "10% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Sheikh Zayed",
        "bedrooms": 3,
        "price": 5200000,
        "area": 175,
        "payment_plan": "15% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Sheikh Zayed",
        "bedrooms": 4,
        "price": 7500000,
        "area": 240,
        "payment_plan": "20% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Capital",
        "bedrooms": 2,
        "price": 2300000,
        "area": 105,
        "payment_plan": "10% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Capital",
        "bedrooms": 3,
        "price": 3500000,
        "area": 145,
        "payment_plan": "10% down payment - 9 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Capital",
        "bedrooms": 4,
        "price": 5900000,
        "area": 205,
        "payment_plan": "15% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Alexandria",
        "bedrooms": 2,
        "price": 1700000,
        "area": 100,
        "payment_plan": "10% down payment - 5 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Alexandria",
        "bedrooms": 3,
        "price": 2500000,
        "area": 140,
        "payment_plan": "15% down payment - 6 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "North Coast",
        "bedrooms": 2,
        "price": 3800000,
        "area": 115,
        "payment_plan": "20% down payment - 6 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "North Coast",
        "bedrooms": 3,
        "price": 5500000,
        "area": 160,
        "payment_plan": "20% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "North Coast",
        "bedrooms": 4,
        "price": 8200000,
        "area": 230,
        "payment_plan": "25% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Ain Sokhna",
        "bedrooms": 2,
        "price": 2900000,
        "area": 110,
        "payment_plan": "10% down payment - 6 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Ain Sokhna",
        "bedrooms": 3,
        "price": 4100000,
        "area": 150,
        "payment_plan": "15% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Cairo",
        "bedrooms": 4,
        "price": 6000000,
        "area": 200,
        "payment_plan": "20% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Cairo",
        "bedrooms": 2,
        "price": 3200000,
        "area": 125,
        "payment_plan": "10% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Maadi",
        "bedrooms": 2,
        "price": 3000000,
        "area": 110,
        "payment_plan": "15% down payment - 6 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Sheikh Zayed",
        "bedrooms": 2,
        "price": 3900000,
        "area": 125,
        "payment_plan": "10% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "6th of October",
        "bedrooms": 4,
        "price": 4700000,
        "area": 190,
        "payment_plan": "15% down payment - 8 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "New Capital",
        "bedrooms": 5,
        "price": 9000000,
        "area": 280,
        "payment_plan": "25% down payment - 9 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "Alexandria",
        "bedrooms": 4,
        "price": 3900000,
        "area": 190,
        "payment_plan": "15% down payment - 7 years",
        "status": PropertyStatus.AVAILABLE,
    },

    {
        "location": "North Coast",
        "bedrooms": 5,
        "price": 10500000,
        "area": 300,
        "payment_plan": "25% down payment - 8 years",
        "status": PropertyStatus.SOLD,
    },
]


# =========================================================
# Insert Properties
# =========================================================

properties = []

for data in properties_data:

    property = Property(**data)

    db.add(property)

    properties.append(property)


db.commit()


for property in properties:
    db.refresh(property)


print(f"Added {len(properties)} properties.")


# =========================================================
# Leads
# =========================================================

lead_names = [
    ("Ahmed Ali", "01012345678"),
    ("Mohamed Hassan", "01123456789"),
    ("Omar Khaled", "01234567890"),
    ("Youssef Ahmed", "01534567891"),
    ("Mahmoud Samir", "01045678912"),
    ("Karim Adel", "01156789123"),
    ("Amr Mohamed", "01267891234"),
    ("Hassan Ali", "01578912345"),
    ("Mostafa Ahmed", "01089123456"),
    ("Khaled Mahmoud", "01191234567"),
    ("Tarek Hassan", "01212345678"),
    ("Sherif Adel", "01523456789"),
    ("Islam Mohamed", "01034567891"),
    ("Hany Ahmed", "01145678912"),
    ("Adel Mahmoud", "01256789123"),
    ("Mina Samir", "01567891234"),
    ("Ossama Khaled", "01078912345"),
    ("Ehab Ali", "01189012345"),
    ("Wael Hassan", "01290123456"),
    ("Sameh Mohamed", "01501234567"),
]


# =========================================================
# Lead Statuses
# =========================================================

lead_statuses = [
    LeadStatus.NEW,
    LeadStatus.CONTACTED,
    LeadStatus.INTERESTED,
    LeadStatus.QUALIFIED,
    LeadStatus.CONVERTED,
    LeadStatus.LOST,
]


# =========================================================
# Insert Leads
# =========================================================

leads = []

for index, (name, phone) in enumerate(lead_names):

    property_index = index % len(properties)

    lead = Lead(
        name=name,
        phone=phone,
        property_id=properties[property_index].id,
        user_id=user.id,
        status=lead_statuses[index % len(lead_statuses)],
    )

    db.add(lead)

    leads.append(lead)


db.commit()


for lead in leads:
    db.refresh(lead)


print(f"Added {len(leads)} leads.")


# =========================================================
# Followups
# =========================================================

followups = []

today = date.today()


for index in range(20):

    lead = leads[index]

    followup = Followup(
        customer_name=lead.name,
        phone=lead.phone,
        date=today + timedelta(days=index + 1),
        time=time(
            hour=10 + (index % 8),
            minute=0
        ),
        property_id=lead.property_id,
        user_id=user.id,
        status=FollowupStatus.SCHEDULED,
    )

    db.add(followup)

    followups.append(followup)


db.commit()


print(f"Added {len(followups)} followups.")


# =========================================================
# Finish
# =========================================================

db.close()

print()
print("========================================")
print("Database seeding completed successfully")
print("========================================")