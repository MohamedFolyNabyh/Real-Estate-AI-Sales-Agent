import requests

API_URL = "http://127.0.0.1:8000"


def search_properties(
    location: str | None = None,
    bedrooms: int | None = None,
    max_price: float | None = None,
):
    params = {
        "location": location,
        "bedrooms": bedrooms,
        "max_price": max_price,
    }

    response = requests.get(f"{API_URL}/properties/", params=params)
    response.raise_for_status()
    return response.json()


def get_property_details(property_id: int):
    response = requests.get(f"{API_URL}/properties/{property_id}")
    response.raise_for_status()
    return response.json()


def create_lead(name: str, phone: str, property_id: int, token: str):
    data = {"name": name, "phone": phone, "property_id": property_id}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{API_URL}/leads/",
        json=data,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def schedule_followup(
    customer_name: str,
    phone: str,
    date: str,
    time: str,
    token: str,
    property_id: int | None = None,
):
    data = {
        "customer_name": customer_name,
        "phone": phone,
        "date": date,
        "time": time,
        "property_id": property_id,
    }
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(
        f"{API_URL}/followups/",
        json=data,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

def update_followup( followup_id: int, date: str, time: str, token: str):
    data = {
        "date": date,
        "time": time
    }
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.patch(
        f"{API_URL}/followups/{followup_id}",
        json=data,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()