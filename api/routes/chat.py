from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from langchain_core.messages import HumanMessage

from api.dependencies.auth import get_current_user
from api.models import User
from api.schemas import ChatRequest, ChatResponse
from app.graph import graph

router = APIRouter(prefix="/chat", tags=["Chat"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):
    config = {"configurable": {"thread_id": f"user_{current_user.id}"}}

    result = graph.invoke(
        {"messages": [HumanMessage(content=request.message)], "token": token},
        config=config,
    )

    final_message = result["messages"][-1]
    content = final_message.content

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
        content = "\n".join(text_parts)

    return ChatResponse(
        message=content, thread_id=f"user_{current_user.id}"
    )