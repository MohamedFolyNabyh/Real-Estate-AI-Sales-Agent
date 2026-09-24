from datetime import date, time
import requests
import streamlit as st

# =========================================================
# Configuration
# =========================================================

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)
# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Real Estate AI Sales Agent",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* Sidebar Text */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* Typography */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a !important;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 15px;
        color: #475569 !important;
        margin-bottom: 20px;
    }

    /* Cards Styling */
    .metric-card, .property-card, .lead-card {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        color: #0f172a !important;
    }

    .metric-title {
        color: #64748b !important;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        color: #0f172a !important;
        font-size: 28px;
        font-weight: 700;
        margin-top: 4px;
    }

    /* General Inputs & Text Controls */
    p, span, label {
        color: #0f172a;
    }

    /* Chat Text Box Adjustments */
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #000000 !important;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Session State Initialization
# =========================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# =========================================================
# API Helpers
# =========================================================

def get_headers():
    if not st.session_state.token:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}


def api_get(endpoint):
    try:
        return requests.get(f"{API_URL}{endpoint}", headers=get_headers())
    except requests.exceptions.RequestException:
        return None


def api_post(endpoint, data):
    try:
        return requests.post(f"{API_URL}{endpoint}", json=data, headers=get_headers())
    except requests.exceptions.RequestException:
        return None


def api_patch(endpoint, data):
    try:
        return requests.patch(f"{API_URL}{endpoint}", json=data, headers=get_headers())
    except requests.exceptions.RequestException:
        return None

# =========================================================
# Streaming Chat Helper
# =========================================================

def stream_chat(message):
    try:
        response = requests.post(
            f"{API_URL}/chat/",
            json={"message": message},
            headers=get_headers(),
            stream=True,
        )
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk

    except requests.exceptions.RequestException as e:
        raise RuntimeError("Failed to connect to AI Agent.") from e

# =========================================================
# Authentication Pages
# =========================================================

def login():
    st.markdown('<div class="main-title" style="text-align:center;">🏠 Real Estate AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle" style="text-align:center;">AI-powered real estate sales platform</div>', unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="user@example.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

    if st.button("🔐 Login", use_container_width=True, key="login_btn"):
        if not email or not password:
            st.warning("Please enter email and password.")
            return

        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                data={"username": email, "password": password},
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]

                user_response = api_get("/auth/me")
                if user_response and user_response.status_code == 200:
                    st.session_state.user = user_response.json()

                st.session_state.page = "Dashboard"
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Login failed. Check your credentials.")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI backend.")


def register():
    st.markdown('<div class="main-title" style="text-align:center;">Create Account</div>', unsafe_allow_html=True)

    name = st.text_input("Name", placeholder="Mohamed", key="reg_name")
    email = st.text_input("Email", placeholder="user@example.com", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")

    if st.button("📝 Create Account", use_container_width=True, key="reg_btn"):
        if not name or not email or not password:
            st.warning("Please fill all fields.")
            return

        try:
            response = requests.post(
                f"{API_URL}/auth/register",
                json={"name": name, "email": email, "password": password},
            )

            if response.status_code in [200, 201]:
                st.success("Account created! Switch to Login tab.")
            else:
                st.error("Registration failed.")

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend.")


def logout():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.chat_messages = []
    st.session_state.page = "Dashboard"
    st.rerun()

# =========================================================
# Dashboard Page
# =========================================================

def dashboard():
    st.markdown('<div class="main-title">Dashboard</div>', unsafe_allow_html=True)
    name = st.session_state.user.get("name", "User") if st.session_state.user else "User"
    st.markdown(f'<div class="subtitle">Welcome back, {name} 👋</div>', unsafe_allow_html=True)

    properties_res = api_get("/properties/")
    leads_res = api_get("/leads/")
    followups_res = api_get("/followups/")

    properties = properties_res.json() if properties_res and properties_res.status_code == 200 else []
    leads = leads_res.json() if leads_res and leads_res.status_code == 200 else []
    followups = followups_res.json() if followups_res and followups_res.status_code == 200 else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Properties", len(properties))
    with col2:
        st.metric("My Leads", len(leads))
    with col3:
        st.metric("My Followups", len(followups))

# =========================================================
# Properties Page
# =========================================================

def properties_page():
    st.markdown('<div class="main-title">🏠 Properties</div>', unsafe_allow_html=True)

    response = api_get("/properties/")
    if not response or response.status_code != 200:
        st.error("Failed to load properties.")
        return

    properties = response.json()
    if not properties:
        st.info("No available properties.")
        return

    for prop in properties:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"### 📍 {prop.get('location', 'N/A')}")
                st.write(f"🛏 Bedrooms: {prop.get('bedrooms', 'N/A')}")
                st.write(f"📐 Area: {prop.get('area', 'N/A')} m²")
            with col2:
                st.write(f"💳 Payment Plan: {prop.get('payment_plan', 'N/A')}")
                st.write(f"📌 Status: {prop.get('status', 'N/A')}")
            with col3:
                price = prop.get("price", 0)
                st.metric("Price", f"${price:,.0f}")

# =========================================================
# Leads Page
# =========================================================

def leads_page():
    st.markdown('<div class="main-title">👤 Leads</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 My Leads", "➕ Create Lead"])

    # --- Tab 1: My Leads ---
    with tab1:
        response = api_get("/leads/")
        if response and response.status_code == 200:
            leads = response.json()
            if not leads:
                st.info("No leads available.")

            for lead in leads:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"### 👤 {lead.get('name', 'N/A')}")
                        st.markdown(f"**📞 Phone:** `{lead.get('phone', 'N/A')}`")
                    with col2:
                        st.markdown(f"**🏠 Property ID:** {lead.get('property_id', 'N/A')}")
                        st.markdown(f"**Status:** `{lead.get('status', 'NEW')}`")
                    with col3:
                        statuses = ["new", "contacted", "interested", "qualified", "converted", "lost"]
                        curr_status = lead.get("status", "new").lower()
                        idx = statuses.index(curr_status) if curr_status in statuses else 0

                        new_status = st.selectbox(
                            "Update Status",
                            statuses,
                            index=idx,
                            format_func=lambda x: x.upper(),
                            key=f"lead_status_{lead['id']}",
                        )

                        if st.button("Update", key=f"update_lead_{lead['id']}"):
                            res = api_patch(f"/leads/{lead['id']}/status", {"status": new_status})
                            if res and res.status_code == 200:
                                st.success("Updated!")
                                st.rerun()
                            else:
                                st.error("Failed to update lead.")
        else:
            st.error("Failed to load leads.")

    # --- Tab 2: Create Lead ---
    with tab2:
        name = st.text_input("Customer Name", key="c_lead_name")
        phone = st.text_input("Phone Number", key="c_lead_phone")
        prop_id = st.number_input("Property ID", min_value=1, step=1, key="c_lead_pid")

        if st.button("Create Lead", use_container_width=True):
            res = api_post("/leads/", {"name": name, "phone": phone, "property_id": int(prop_id)})
            if res and res.status_code in [200, 201]:
                st.success("Lead Created!")
                st.rerun()
            else:
                st.error("Failed to create lead.")

# =========================================================
# Followups Page
# =========================================================

def followups_page():
    st.markdown('<div class="main-title">📅 Followups</div>', unsafe_allow_html=True)

    response = api_get("/followups/")
    if not response or response.status_code != 200:
        st.error("Failed to load followups.")
        return

    followups = response.json()
    if not followups:
        st.info("No followups available.")
        return

    for followup in followups:
        with st.container(border=True):
            st.markdown(f"### 👤 {followup.get('customer_name', 'N/A')}")
            st.write(f"📞 Phone: {followup.get('phone', 'N/A')}")
            st.write(f"🏠 Property ID: {followup.get('property_id', 'N/A')}")
            st.write(f"📅 Date: {followup.get('date', 'N/A')}")
            st.write(f"⏰ Time: {followup.get('time', 'N/A')}")
            st.write(f"📌 Status: {followup.get('status', 'N/A')}")

# =========================================================
# AI Chat Page
# =========================================================

def chat_page():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="main-title">🤖 AI Sales Agent</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🗑️ Clear Chat", key="clear_chat_btn"):
            st.session_state.chat_messages = []
            st.rerun()

    # Render Previous Messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User Input
    user_message = st.chat_input("Ask something about properties...")

    if user_message:
        # Save & Display User Message
        st.session_state.chat_messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.write(user_message)

        # Stream & Save AI Response
        with st.chat_message("assistant"):
            try:
                answer = st.write_stream(stream_chat(user_message))
                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            except RuntimeError as e:
                st.error(str(e))

# =========================================================
# Sidebar & Navigation
# =========================================================

def sidebar():
    with st.sidebar:
        st.markdown("# 🏠 Real Estate AI")
        st.divider()

        if st.session_state.user:
            st.write(f"👤 **{st.session_state.user.get('name', 'User')}**")
            st.caption(st.session_state.user.get("email", ""))
            st.divider()

            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = "Dashboard"
                st.rerun()

            if st.button("🏠 Properties", use_container_width=True):
                st.session_state.page = "Properties"
                st.rerun()

            if st.button("👤 Leads", use_container_width=True):
                st.session_state.page = "Leads"
                st.rerun()

            if st.button("📅 Followups", use_container_width=True):
                st.session_state.page = "Followups"
                st.rerun()

            if st.button("🤖 AI Agent", use_container_width=True):
                st.session_state.page = "AI Agent"
                st.rerun()

            st.divider()

            if st.button("🚪 Logout", use_container_width=True):
                logout()

# =========================================================
# Main Router
# =========================================================

def main():
    if st.session_state.token is None:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        sidebar()
        pages = {
            "Dashboard": dashboard,
            "Properties": properties_page,
            "Leads": leads_page,
            "Followups": followups_page,
            "AI Agent": chat_page,
        }
        page_fn = pages.get(st.session_state.page, dashboard)
        page_fn()

# =========================================================
# Run Application
# =========================================================

if __name__ == "__main__":
    main()