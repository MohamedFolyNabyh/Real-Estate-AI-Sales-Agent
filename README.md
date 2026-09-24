# 🏠 Real Estate AI Sales Agent

An AI-powered real estate sales assistant built with **FastAPI, PostgreSQL, LangGraph, JWT Authentication, SQLAlchemy, Alembic, Streamlit, and Docker**.

The system helps real estate sales agents search for available properties, retrieve property details, create customer leads, schedule follow-ups, and update existing appointments through a conversational AI agent.

The project combines a real backend with an AI agent that can turn natural-language requests into real actions through tool calling.

---

# 🚀 Project Overview

The goal of this project is to build a practical **AI Sales Agent for real estate companies**.

Instead of forcing a sales agent to manually search through properties and enter customer information, the AI agent understands natural language and interacts with the backend through structured tools.

For example:

> "I need a 3 bedroom apartment in Cairo under 5 million."

The AI agent can extract the required parameters:

```text
location = Cairo
bedrooms = 3
max_price = 5000000
```

and call the property search tool.

The tool communicates with the FastAPI backend, which retrieves the available properties from PostgreSQL.

The agent can also handle conversations such as:

> "I am interested in property 5."

> "My name is Mohamed and my phone is 01273086886."

The agent can then create the lead automatically once all required information is available.

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

The AI uses the `search_properties` tool and retrieves real data from the backend instead of inventing property information.

Only properties with:

```text
status = available
```

are returned by the property search endpoint.

---

# 📍 Available Locations

The agent can also answer questions such as:

```text
What areas do you have?

Which locations are available?

What areas are your properties in?
```

The agent searches the available properties and extracts the locations returned by the database.

It does not invent locations.

---

# 🏡 Property Details

The agent can retrieve detailed information about a specific property.

Example:

```text
Tell me more about property 3.
```

The agent uses:

```text
get_property_details
```

to retrieve the real property information.

The returned data can include:

```text
Location
Bedrooms
Price
Area
Payment Plan
Status
```

---

# 👤 Lead Management

The system allows the AI agent to create a lead when the required information is available.

Required information:

* Customer name
* Customer phone number
* Property ID

Example:

```text
I am interested in property 4.
```

Then:

```text
My name is Mohamed and my phone number is 01273086886.
```

The agent can then call:

```text
create_lead
```

automatically.

### Duplicate Lead Protection

The backend checks whether the same customer has already registered interest in the same property for the same authenticated user.

This prevents duplicate lead records.

---

# 📞 Egyptian Phone Validation

Lead creation includes validation for Egyptian mobile numbers.

The expected format is:

```text
010xxxxxxxx
011xxxxxxxx
012xxxxxxxx
015xxxxxxxx
```

Example:

```text
01273086886
```

The backend validates the phone number before creating the lead.

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

into an actual date.

For example:

```text
tomorrow
```

can be converted into:

```text
YYYY-MM-DD
```

A follow-up can optionally be associated with a property.

Example:

```text
Schedule a follow-up for Mohamed tomorrow at 4 PM regarding property 5.
```

---

# 🔄 Update Existing Follow-ups

The agent can modify an existing follow-up instead of creating a duplicate.

Example:

```text
Change my follow-up to 5 PM.
```

The agent uses:

```text
update_followup
```

to update the existing record.

The update operation modifies:

```text
Date
Time
```

while preserving the existing property relationship.

This prevents unnecessary duplicate appointments.

---

# 🔐 JWT Authentication

The application uses **JWT authentication**.

Users can:

* Register
* Login
* Access their profile
* Access their own leads
* Access their own follow-ups
* Use protected AI operations

The authentication flow is:

```text
Login
   ↓
JWT Token
   ↓
Authorization Header
   ↓
FastAPI
   ↓
get_current_user()
   ↓
Authenticated User
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

# 🔒 Data Ownership

Leads and follow-ups are associated with the authenticated user.

For example:

```text
User 1
 │
 ├── Lead 1
 ├── Lead 2
 └── Follow-up 1

User 2
 │
 ├── Lead 3
 └── Follow-up 2
```

Users cannot access another user's leads or follow-ups.

This is enforced at the database query level.

For example:

```python
.filter(Lead.user_id == current_user.id)
```

and:

```python
.filter(Followup.user_id == current_user.id)
```

The same ownership check is also applied when updating follow-ups.

---

# 🤖 AI Agent Architecture

The AI agent is implemented using **LangGraph** and **Gemini**.

The overall system architecture is:

```text
                     ┌──────────────────┐
                     │    Streamlit     │
                     │    Frontend      │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │     FastAPI      │
                     │    /chat/        │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │    LangGraph     │
                     │      Agent       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │      Gemini      │
                     │       LLM        │
                     └────────┬─────────┘
                              │
                     Tool Calling
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
   search_properties   get_property_details   create_lead
          │                                        │
          └───────────────────┬────────────────────┘
                              │
                    schedule_followup
                              │
                    update_followup
                              │
                              ▼
                     ┌──────────────────┐
                     │     FastAPI      │
                     │      APIs       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   PostgreSQL     │
                     └──────────────────┘
```

---

# 🧠 LangGraph Flow

The current graph follows the basic agent loop:

```text
LLM
 │
 ▼
Tools
 │
 ▼
LLM
 │
 ▼
Final Answer
```

If the LLM determines that a tool is required, LangGraph executes it.

Example:

```text
User:
"I need a 3 bedroom apartment in Cairo."
```

The LLM decides to call:

```text
search_properties
```

The tool retrieves the data from the backend.

The result is returned to the LLM.

The LLM then generates the final response.

---

# 🛠️ AI Tools

The agent currently uses five tools.

## `search_properties`

Searches available properties.

Parameters:

```text
location
bedrooms
max_price
```

---

## `get_property_details`

Retrieves detailed information about a property.

Parameter:

```text
property_id
```

---

## `create_lead`

Creates a customer lead.

Parameters:

```text
name
phone
property_id
```

The authenticated JWT token is injected automatically.

---

## `schedule_followup`

Creates a new follow-up.

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

## `update_followup`

Updates an existing follow-up.

Parameters:

```text
followup_id
date
time
```

The authenticated JWT token is injected automatically.

---

# 🌊 Response Streaming

The `/chat/` endpoint uses **streaming responses**.

Instead of waiting for the complete AI response and returning one large JSON response, FastAPI streams the generated text progressively.

The flow is:

```text
Gemini
  ↓
LangGraph
  ↓
FastAPI StreamingResponse
  ↓
Streamlit
  ↓
Text appears progressively
```

This provides a more natural conversational experience.

The endpoint returns:

```text
text/plain
```

instead of the previous JSON `ChatResponse` format.

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
                /     \
               /       \
              ▼         ▼
           leads     followups
              │          │
              └────┬─────┘
                   │
                   ▼
               properties
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

Property status values:

```text
available
reserved
sold
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

Lead status values include:

```text
new
contacted
interested
qualified
converted
lost
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

Follow-up status values:

```text
scheduled
completed
cancelled
```

`property_id` is optional for follow-ups, allowing general customer follow-ups that are not associated with a specific property.

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
* Argon2
* python-jose

## AI

* LangGraph
* LangChain
* Google Gemini
* LLM Tool Calling
* Structured Tools
* Pydantic

## Frontend

* Streamlit

## Infrastructure

* Docker
* Docker Compose
* Docker Hub

---

# 📁 Project Structure

```text
Real-Estate-AI-Sales-Agent/
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
├── .env.example
├── .dockerignore
├── .gitignore
└── README.md
```

---

# 🐳 Docker Architecture

The project uses a single application image for both the backend and frontend.

Docker Compose runs three services:

```text
┌─────────────────────────┐
│       PostgreSQL        │
│      postgres:16        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│        Backend          │
│        FastAPI          │
│        Port 8000        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│        Frontend         │
│        Streamlit        │
│        Port 8501        │
└─────────────────────────┘
```

The same Docker image:

```text
mohamedfoly12/real-estate-ai-sales-agent:latest
```

is used by both:

```text
backend
frontend
```

The containers run different commands:

```text
Backend
→ uvicorn api.main:app --host 0.0.0.0 --port 8000
```

```text
Frontend
→ streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501
```

---

# 🐳 Docker Hub

The application image is published to Docker Hub as:

```text
mohamedfoly12/real-estate-ai-sales-agent:latest
```

Docker Hub repository:

https://hub.docker.com/r/mohamedfoly12/real-estate-ai-sales-agent

The Docker Compose configuration uses this image directly, so another machine does not need to build the application image locally.

---

# ⚙️ Run with Docker

## 1. Clone the repository

```bash
git clone https://github.com/MohamedFolyNabyh/Real-Estate-AI-Sales-Agent.git
```

Move into the project:

```bash
cd Real-Estate-AI-Sales-Agent
```

---

## 2. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Example for Docker:

```env
DATABASE_URL=postgresql+psycopg://real_estate_user:real_estate_password@postgres:5432/real_estate

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

GOOGLE_API_KEY=your-google-api-key
```

### Important

Inside Docker, PostgreSQL is accessed using:

```text
postgres:5432
```

not:

```text
localhost:5432
```

because `postgres` is the Docker Compose service name.

Do not upload `.env` to GitHub.

---

## 3. Start the Application

Run:

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

Expected services:

```text
real_estate_postgres
real_estate_backend
real_estate_frontend
```

---

## 4. Run Database Migrations

Run Alembic inside the backend container:

```bash
docker compose exec backend alembic upgrade head
```

Check the current migration:

```bash
docker compose exec backend alembic current
```

Check available heads:

```bash
docker compose exec backend alembic heads
```

---

# 🌐 Application URLs

After the containers start:

### FastAPI

```text
http://localhost:8000
```

### Swagger

```text
http://localhost:8000/docs
```

### OpenAPI

```text
http://localhost:8000/openapi.json
```

### Streamlit

```text
http://localhost:8501
```

### Important Docker Note

Uvicorn displays:

```text
http://0.0.0.0:8000
```

inside the container.

`0.0.0.0` is the address the server listens on; it is not the browser address.

Use:

```text
http://localhost:8000/docs
```

or:

```text
http://127.0.0.1:8000/docs
```

---

# 🔗 Docker Networking

The frontend container communicates with the backend using:

```text
http://backend:8000
```

This is configured in Docker Compose:

```yaml
environment:
  API_URL: http://backend:8000
```

The browser accesses Streamlit through:

```text
http://localhost:8501
```

while containers communicate using their Docker service names.

---

# 🧪 Run from Docker Hub Without Building

The Docker Compose configuration uses:

```text
mohamedfoly12/real-estate-ai-sales-agent:latest
```

To test the published image on a clean machine:

```bash
docker compose up -d
```

Docker will pull the image from Docker Hub when it is not already available locally.

To simulate a clean local environment:

```bash
docker compose down
```

Then remove the local image:

```bash
docker rmi mohamedfoly12/real-estate-ai-sales-agent:latest
```

Then start again:

```bash
docker compose up -d
```

Docker will download the application image from Docker Hub.

The PostgreSQL volume is preserved by:

```text
postgres_data
```

Do not use:

```bash
docker compose down -v
```

when you want to keep the database data.

---

# 🐍 Run Locally Without Docker

The application can also be run using a local Python environment.

Create a Conda environment:

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

For local PostgreSQL, the database URL should point to `localhost` instead of the Docker service name.

Example:

```env
DATABASE_URL=postgresql+psycopg://real_estate_user:real_estate_password@localhost:5432/real_estate
```

---

# 🐘 PostgreSQL

PostgreSQL can be started through Docker Compose:

```bash
docker compose up -d postgres
```

Check the database container:

```bash
docker compose ps postgres
```

The database is stored in the Docker volume:

```text
postgres_data
```

---

# ▶️ Run FastAPI Locally

Start the backend with:

```bash
uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🖥️ Run Streamlit Locally

In another terminal:

```bash
streamlit run streamlit_app.py
```

For local execution, the frontend uses:

```text
http://127.0.0.1:8000
```

as the FastAPI backend URL.

---

# 🔑 Authentication Flow

```text
Register
   ↓
Login
   ↓
JWT Token
   ↓
Authorization: Bearer <token>
   ↓
FastAPI
   ↓
get_current_user()
   ↓
Database User
```

Protected operations require the JWT token.

---

# 💬 Example AI Conversations

## Property Search

```text
User:
ايه الشقق المتاحة؟
```

The agent calls:

```text
search_properties
```

---

## Search with Filters

```text
User:
عايز شقة 3 غرف في القاهرة بسعر لحد 5 مليون
```

The agent extracts:

```text
location = Cairo
bedrooms = 3
max_price = 5000000
```

and searches the backend.

---

## Property Details

```text
User:
عايز تفاصيل الشقة رقم 3
```

The agent calls:

```text
get_property_details
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

The agent can call:

```text
create_lead
```

when all required information is available.

---

## Schedule Follow-up

```text
User:
كلمني بكرة الساعة 4
```

The agent converts the relative date and calls:

```text
schedule_followup
```

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

# 🔄 Conversation Memory

The LangGraph agent maintains conversation history using a thread associated with the authenticated user.

The current thread ID follows the pattern:

```text
user_<user_id>
```

This allows the agent to understand references from previous messages such as:

```text
it
this property
the apartment
المتابعة
العقار ده
```

within the conversation.

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

Optional filters include:

```text
location
bedrooms
max_price
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

The response is streamed progressively as:

```text
text/plain
```

---

# 🔐 Security

The project uses JWT authentication for protected endpoints.

Protected resources include:

```text
/leads/
/followups/
/chat/
```

Users can only access their own:

```text
Leads
Follow-ups
```

The backend validates the authenticated user before performing protected operations.

Property search remains public because property availability is not user-specific.

---

# 🧪 Testing

The application can be tested through:

### Swagger

```text
http://localhost:8000/docs
```

### Streamlit

```text
http://localhost:8501
```

The main flows to test are:

```text
Register
↓
Login
↓
Property Search
↓
Property Details
↓
Lead Creation
↓
Phone Validation
↓
Follow-up Scheduling
↓
Follow-up Update
↓
Streaming AI Response
```

---

# 📦 Requirements

Main dependencies include:

```text
fastapi
uvicorn
SQLAlchemy
psycopg
alembic

langchain_core
langchain_google_genai
langgraph

pydantic
email-validator
python-multipart
python-dotenv

python-jose
argon2-cffi
requests

streamlit
```

The exact pinned versions are available in:

```text
requirements.txt
```

---

# 🎯 Project Goals

This project demonstrates practical implementation of:

* REST APIs
* JWT Authentication
* OAuth2 Bearer Authentication
* PostgreSQL
* SQLAlchemy
* Alembic migrations
* User data ownership
* Pydantic validation
* LangGraph
* LLM Tool Calling
* Structured Tools
* Conversational AI
* AI-powered CRM operations
* Response Streaming
* Streamlit
* Docker
* Docker Compose
* Docker Hub

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
* AI agent evaluation
* RAG over property/project documents

---

# 📌 Project Status

Current implementation includes:

* ✅ FastAPI backend
* ✅ PostgreSQL database
* ✅ SQLAlchemy models
* ✅ Alembic migrations
* ✅ JWT authentication
* ✅ OAuth2 Bearer authentication
* ✅ User ownership
* ✅ Property search
* ✅ Property details
* ✅ Lead management
* ✅ Egyptian phone validation
* ✅ Duplicate lead protection
* ✅ Follow-up scheduling
* ✅ Follow-up updates
* ✅ LangGraph agent
* ✅ Gemini integration
* ✅ Tool calling
* ✅ Conversation history
* ✅ Streaming AI responses
* ✅ Streamlit frontend
* ✅ Docker support
* ✅ Docker Compose
* ✅ Docker Hub image

---

# 👨‍💻 Author

**Mohamed Foly**

AI / ML Engineer

GitHub:

https://github.com/MohamedFolyNabyh

Docker Hub:

https://hub.docker.com/u/mohamedfoly12

---

# ⭐ If you find this project useful

Feel free to explore the repository, test the application, and give feedback.
