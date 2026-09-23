from datetime import datetime
import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import StructuredTool

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import InjectedState, ToolNode, tools_condition

from app.schemas import (
    CreateLeadInput,
    GetPropertyDetailsInput,
    ScheduleFollowupInput,
    SearchPropertiesInput,
    UpdateFollowupInput,
)

from app.tools import (
    create_lead,
    get_property_details,
    schedule_followup,
    search_properties,
    update_followup,
)

from app.prompts import SALES_AGENT_PROMPT


# =========================================
# Environment
# =========================================

load_dotenv()


# =========================================
# Checkpointer
# =========================================

checkpointer = InMemorySaver()


# =========================================
# Agent State
# =========================================

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    token: str


# =========================================
# LLM Initialization
# =========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)


# =========================================
# Structured Tools Definition
# =========================================

search_properties_tool = StructuredTool.from_function(
    func=search_properties,
    name="search_properties",
    description=(
        "Search for AVAILABLE properties. Location, bedrooms, and max price are optional filters. "
        "Call without filters if asked generally about availability or available areas."
    ),
    args_schema=SearchPropertiesInput,
)

get_property_details_tool = StructuredTool.from_function(
    func=get_property_details,
    name="get_property_details",
    description="Get detailed information about a specific property using its property ID.",
    args_schema=GetPropertyDetailsInput,
)


def create_lead_with_token(
    name: str,
    phone: str,
    property_id: int,
    token: Annotated[str, InjectedState("token")],
):
    return create_lead(
        name=name,
        phone=phone,
        property_id=property_id,
        token=token,
    )


create_lead_tool = StructuredTool.from_function(
    func=create_lead_with_token,
    name="create_lead",
    description="Create a sales lead when name, phone, and property_id are provided.",
    args_schema=CreateLeadInput,
)


def schedule_followup_with_token(
    customer_name: str,
    phone: str,
    date: str,
    time: str,
    property_id: int | None = None,
    token: Annotated[str, InjectedState("token")] = None,
):
    return schedule_followup(
        customer_name=customer_name,
        phone=phone,
        date=date,
        time=time,
        property_id=property_id,
        token=token,
    )


schedule_followup_tool = StructuredTool.from_function(
    func=schedule_followup_with_token,
    name="schedule_followup",
    description=(
        "Schedule a new follow-up appointment when explicitly requested by the customer. "
        "Do not use to change existing appointments."
    ),
    args_schema=ScheduleFollowupInput,
)


def update_followup_with_token(
    followup_id: int,
    date: str,
    time: str,
    token: Annotated[str, InjectedState("token")],
):
    print("\n========== UPDATE FOLLOWUP DEBUG ==========")
    print("FOLLOWUP ID:", followup_id)
    print("NEW DATE:", date)
    print("NEW TIME:", time)
    print("TOKEN:", token[:15] + "..." if token else None)
    print("===========================================\n")

    return update_followup(
        followup_id=followup_id,
        date=date,
        time=time,
        token=token,
    )


update_followup_tool = StructuredTool.from_function(
    func=update_followup_with_token,
    name="update_followup",
    description=(
        "Update or reschedule an existing follow-up appointment when the customer asks to change "
        "the time or date of a scheduled follow-up. Do not create a new follow-up."
    ),
    args_schema=UpdateFollowupInput,
)


# =========================================
# Tools Setup & Binding
# =========================================

tools = [
    search_properties_tool,
    get_property_details_tool,
    create_lead_tool,
    schedule_followup_tool,
    update_followup_tool,
]

llm_with_tools = llm.bind_tools(tools)


# =========================================
# Model Execution Node
# =========================================

def call_model(state: AgentState):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")

    system_prompt = SALES_AGENT_PROMPT.format(
        current_date=current_date,
        current_time=current_time,
    )

    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    # Debug Log
    print("\n========== MESSAGE HISTORY ==========")
    for i, message in enumerate(messages):
        print(f"--- MESSAGE {i} ({type(message).__name__}) ---")
        print("CONTENT:", message.content)
        if getattr(message, "tool_calls", None):
            print("TOOL CALLS:", message.tool_calls)
    print("====================================\n")

    response = llm_with_tools.invoke(messages)

    # Debug Model Output
    print("\n========== MODEL RESPONSE ==========")
    print("CONTENT:", response.content)
    print("TOOL CALLS:", response.tool_calls)
    print("====================================\n")

    return {"messages": [response]}


# =========================================
# Build StateGraph
# =========================================

tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("llm", call_model)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges(
    "llm",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)
graph_builder.add_edge("tools", "llm")

graph = graph_builder.compile(checkpointer=checkpointer)