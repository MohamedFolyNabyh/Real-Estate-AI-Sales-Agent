from fastapi import FastAPI

from api.database import Base, engine
from api import models

from api.routes.properties import router as properties_router
from api.routes.leads import router as leads_router
from api.routes.followups import router as followups_router
from api.routes.chat import router as chat_router
from api.routes.auth import router as auth_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يتيح الاتصال من أي مصدر أثناء التطوير
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Real Estate AI Sales Agent"
)


app.include_router(
    properties_router
)

app.include_router(
    leads_router
)

app.include_router(
    followups_router
)

app.include_router(
    chat_router
)


app.include_router(auth_router)