# 🏠 Real Estate AI Sales Agent

An AI-powered real estate sales assistant built with **FastAPI, PostgreSQL, LangGraph, JWT Authentication, SQLAlchemy, Alembic, and Streamlit**.

The system helps real estate sales agents search for available properties, collect customer leads, schedule follow-ups, and modify existing appointments through a conversational AI agent.

---

## 🚀 Project Overview

The goal of this project is to build a practical AI sales agent for a real estate company.

Instead of forcing the sales agent to manually search through properties and enter customer information, the AI agent can understand natural language requests and interact with the backend through tools.

For example:

> "I need a 3 bedroom apartment in Cairo under 5 million."

The AI agent can understand the request and call the property search tool with:

```text
location = Cairo
bedrooms = 3
max_price = 5000000
```

The system then retrieves the available properties from PostgreSQL and returns the results to the user.

The agent can also handle conversations such as:

> "I am interested in property 5."

> "My name is Mohamed and my phone is 01273086886."

The agent can then create a lead automatically.

---

# ✨ Main Features

## 🏠 Property Search

Users can search available properties using:

* Location
* Number of bedrooms
* Maximum price

Examples:

```text
Show me available properties.

Show me properties in Cairo.

I need a 3 bedroom apartment.

Show me properties under 5 million.

Show me 3 bedroom apartments in Cairo under 5 million.
```

The AI uses the `search_properties` tool instead of inventing property information.

---

## 📍 Available Locations

The AI can also answer questions such as:

```text
What areas do you have?

Which locations are available?

What areas are your properties in?
```

The agent retrieves the properties from the database and extracts the available locations.

It does not invent locations.

---

## 🏡 Property Details

The agent can retrieve details for a specific property.

Example:

```text
Tell me more about property 3.
```

The system retrieves the property using:

```text
get_property_details
```

---

# 👤 Lead Management

The system allows the AI agent to create a lead when the required information is available.

Required information:

* Customer name
* Phone number
* Property ID

Example:

```text
I am interested in property 4.

My name is Mohamed and my phone number is 01273086886.
```

The AI can create the lead automatically.

Each lead is connected to the authenticated user.

This means one sales agent cannot access another sales agent's leads.

---

# 📅 Follow-up Management

The AI agent can schedule customer follow-ups.

Example:

```text
Schedule a follow-up tomorrow at 4 PM.
```

The agent converts relative dates such as:

```text
today
tomorrow
بكرة
النهارده
```

into actual dates.

A follow-up can optionally be associated with a property.

For example:

```text
Schedule a follow-up for Mohamed tomorrow at 4 PM regarding property 5.
```

---

# 🔄 Update Existing Follow-ups

The AI can also modify an existing follow-up.

Example:

```text
Change my follow-up to 5 PM.
```

The agent uses:

```text
update_followup
```

instead of creating a new follow-up.

This prevents duplicate appointments.

The update operation can modify:

* Date
* Time

while keeping the existing property relationship.

---

# 🔐 JWT Authentication

The application uses JWT authentication.

Users can:

* Register
* Login
* Access their profile
* Access their own leads
* Access their own follow-ups

The JWT contains the authenticated user's ID.

The backend uses the token to identify the current user.

---

# 🔒 Data Ownership

Leads and follow-ups are associated with a user.

For example:

```text
User
  │
  ├── Lead 1
  ├── Lead 2
  └── Lead 3
```

Another user will not be able to access these records.

This is implemented using queries such as:

```python
.filter(Lead.user_id == current_user.id)
```

and:

```python
.filter(Followup.user_id == current_user.id)
```

---

# 🤖 AI Agent Architecture

The AI agent is implemented using **LangGraph**.

The basic flow is:

```text
User
 │
 ▼
Streamlit
 │
 ▼
FastAPI /chat/
 │
 ▼
LangGraph
 │
 ▼
LLM
 │
 ├───────────────┐
 │               │
 ▼               ▼
Tools          Final Answer
 │
 ├── search_properties
 │
 ├── get_property_details
 │
 ├── create_lead
 │
 ├── schedule_followup
 │
 └── update_followup
 │
 ▼
FastAPI APIs
 │
 ▼
PostgreSQL
```

---

# 🧠 LangGraph Flow

The graph contains two main nodes:

```text
LLM
 │
 ▼
Tools
 │
 ▼
LLM
```

If the LLM decides that a tool is required, LangGraph executes the tool.

For example:

```text
User:
"I need a 3 bedroom apartment in Cairo."
```

The LLM decides to call:

```text
search_properties
```

The tool queries the backend.

The result is returned to the LLM.

The LLM then generates the final response.

---

# 🛠️ AI Tools

The current agent contains the following tools.

## search_properties

Searches available properties.

Parameters:

```text
location
bedrooms
max_price
```

---

## get_property_details

Returns detailed information about a property.

Parameter:

```text
property_id
```

---

## create_lead

Creates a new lead.

Parameters:

```text
name
phone
property_id
```

The authenticated JWT token is injected automatically.

---

## schedule_followup

Schedules a new follow-up.

Parameters:

```text
customer_name
phone
date
time
property_id
```

`property_id` is optional.

---

## update_followup

Updates an existing follow-up.

Parameters:

```text
followup_id
date
time
```

The authenticated JWT token is injected automatically.

---

# 🗄️ Database

The project uses:

```text
PostgreSQL
```

Main tables:

```text
users
properties
leads
followups
```

Relationship:

```text
users
 │
 ├──────────────┐
 │              │
 ▼              ▼
leads        followups
```

Properties are referenced by:

```text
leads.property_id
followups.property_id
```

---

# 📊 Database Models

## User

```text
id
name
email
password_hash
created_at
```

---

## Property

```text
id
location
bedrooms
price
area
payment_plan
status
```

---

## Lead

```text
id
name
phone
property_id
status
user_id
```

---

## Followup

```text
id
customer_name
phone
date
time
property_id
status
user_id
```

---

# 🧰 Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic

## Authentication

* JWT
* OAuth2 Bearer Authentication
* argon2
* python-jose

## AI

* LangGraph
* LangChain
* Google Gemini
* Tool Calling
* Structured Tools
* Pydantic

## Frontend

* Streamlit

## Infrastructure

* Docker
* Docker Compose

---

# 📁 Project Structure

```text
langgraph-agent-project/
│
├── api/
│   ├── database/
│   ├── dependencies/
│   │   └── auth.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── ...
│
├── app/
│   ├── graph.py
│   ├── prompts.py
│   ├── schemas.py
│   └── tools.py
│
├── alembic/
│   └── versions/
│
├── streamlit_app.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
<<<<<<< HEAD
git clone github.com/MohamedFolyNabyh/Real-Estate-AI-Sales-Agent.git
=======
git clone YOUR_GITHUB_REPOSITORY_URL
>>>>>>> bf21f7e (Dockerize application and update README)
```

Move into the project:

```bash
<<<<<<< HEAD
cd Real-Estate-AI-Sales-Agent
=======
cd langgraph-agent-project
>>>>>>> bf21f7e (Dockerize application and update README)
```

---

# 🐍 Create Virtual Environment

Using Conda:

```bash
conda create -n agent python=3.11
```

Activate it:

```bash
conda activate agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://real_estate_user:password@localhost:5432/real_estate

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

GOOGLE_API_KEY=your-google-api-key
```

Do not upload `.env` to GitHub.

Add it to `.gitignore`:

```text
.env
__pycache__/
*.pyc
.venv/
```

---

# 🐘 PostgreSQL

The project can run PostgreSQL using Docker.

Start the services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

---

# 🗃️ Database Migrations

Run:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

Check available heads:

```bash
alembic heads
```

---

# ▶️ Run FastAPI

Start the backend:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🖥️ Run Streamlit

In another terminal:

```bash
streamlit run streamlit_app.py
```

The frontend will be available through the Streamlit URL shown in the terminal.

---

# 🔑 Authentication Flow

The authentication flow is:

```text
Register
   ↓
Login
   ↓
JWT Token
   ↓
Authorization Header
   ↓
FastAPI
   ↓
get_current_user()
```

The frontend sends:

```http
Authorization: Bearer <JWT_TOKEN>
```

The backend extracts the user ID from:

```text
JWT.sub
```

and loads the corresponding user from PostgreSQL.

---

# 💬 Example AI Conversations

## Property Search

```text
User:
ايه الشقق المتاحة؟
```

The agent calls:

```text
search_properties()
```

---

## Search by filters

```text
User:
عايز شقة 3 غرف في القاهرة بسعر لحد 5 مليون
```

The agent uses:

```text
location = Cairo
bedrooms = 3
max_price = 5000000
```

---

## Lead Creation

```text
User:
أنا مهتم بالعقار رقم 3
```

Then:

```text
User:
اسمي محمد فولي ورقمي 01273086886
```

The agent can create the lead.

---

## Schedule Follow-up

```text
User:
كلمني بكرة الساعة 4
```

The agent schedules the follow-up.

---

## Update Follow-up

```text
User:
غير ميعاد المتابعة وخليها الساعة 5
```

The agent uses:

```text
update_followup
```

instead of creating another follow-up.

---

# 🔄 API Endpoints

## Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

---

## Properties

```text
GET /properties/
GET /properties/{property_id}
```

Example:

```text
GET /properties/?location=Cairo
```

---

## Leads

```text
POST  /leads/
GET   /leads/
PATCH /leads/{lead_id}/status
```

---

## Followups

```text
POST  /followups/
GET   /followups/
PATCH /followups/{followup_id}
PATCH /followups/{followup_id}/status
```

---

## AI Agent

```text
POST /chat/
```

Example request:

```json
{
    "message": "Show me available properties"
}
```

---

# 🧪 Testing

The project can be tested through:

### Swagger

```text
http://127.0.0.1:8000/docs
```

### Streamlit

Use the Streamlit frontend to test:

* Login
* Property search
* Lead creation
* Follow-up creation
* Follow-up updates
* AI conversations

---

# 🔐 Security

The project uses JWT authentication for protected endpoints.

Protected resources include:

```text
/leads/
/followups/
/chat/
```

Users can only access their own leads and follow-ups.

Property search is public because property availability is not user-specific.

---

# 🎯 Project Goals

This project demonstrates practical implementation of:

* REST APIs
* Authentication
* JWT
* PostgreSQL
* SQLAlchemy
* Database migrations
* LangGraph
* LLM Tool Calling
* Structured Tools
* Pydantic validation
* Conversational AI
* AI-powered CRM operations
* Streamlit
* Docker

---

# 🚧 Future Improvements

Possible future improvements include:

* Arabic location normalization
* More advanced property recommendations
* Conversation persistence in PostgreSQL
* Redis-based conversation memory
* CRM dashboard analytics
* Property recommendation ranking
* Automated follow-up reminders
* WhatsApp integration
* Email integration
* Calendar integration
* Human handoff to sales agents
* Evaluation of the AI agent
* RAG over property/project documents

---

# 📌 Project Status

Current implementation includes:

* ✅ FastAPI backend
* ✅ PostgreSQL database
* ✅ SQLAlchemy models
* ✅ Alembic migrations
* ✅ JWT authentication
* ✅ User ownership
* ✅ Property search
* ✅ Lead management
* ✅ Follow-up management
* ✅ Follow-up updates
* ✅ LangGraph agent
* ✅ Tool calling
* ✅ Gemini integration
* ✅ Streamlit frontend
* ✅ Docker support

---

# 👨‍💻 Author

**Mohamed Foly**

AI / ML Engineer

GitHub:

```text
https://github.com/MohamedFolyNabyh
```

---

# ⭐ If you find this project useful

Feel free to explore the repository, test the application, and give feedback.
