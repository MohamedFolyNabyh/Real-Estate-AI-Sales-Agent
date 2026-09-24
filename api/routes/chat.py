from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer

from langchain_core.messages import HumanMessage

from api.dependencies.auth import get_current_user
from api.models import User
from api.schemas import ChatRequest
from app.graph import graph


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post("/")
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
):

    config = {
        "configurable": {
            "thread_id": f"user_{current_user.id}"
        }
    }

    def generate():

        for message_chunk, metadata in graph.stream(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ],
                "token": token
            },
            config=config,
            stream_mode="messages"
        ):

            if metadata.get("langgraph_node") != "llm":
                continue

            content = message_chunk.content

            # -----------------------------------------
            # String content
            # -----------------------------------------

            if isinstance(content, str):

                if content:
                    yield content

            # -----------------------------------------
            # List content
            # -----------------------------------------

            elif isinstance(content, list):

                for item in content:

                    if isinstance(item, dict):

                        if item.get("type") == "text":

                            text = item.get("text", "")

                            if text:
                                yield text

    return StreamingResponse(
        generate(),
        media_type="text/plain; charset=utf-8"
    )