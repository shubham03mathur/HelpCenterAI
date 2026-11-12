from typing import NotRequired, Dict, Any
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from typing_extensions import Literal, TypedDict

from pydantic import BaseModel

class EmailClassification(TypedDict):
    intent: Literal["question", "bug", "billing", "feature", "complex"]
    urgency: Literal["low", "medium", "high", "critical"]
    topic: str
    summary: str

class AgentRunSchema(TypedDict):
    conversation_id: str
    run_id: str
    thread_id: str
    message: str

class ConversationState(BaseModel):
    conversation_id: str
    topic: str
    email: str
    name: str
    concern: str

class ReviewState(BaseModel):
    conversation_id: str
    payload: Dict[str, Any]

class AgentState(TypedDict):
    sender_email: str
    conversation_id: str
    message: str

    email_id: NotRequired[str | None]

    # Classification result
    classification: NotRequired[EmailClassification | None]

    # Raw search/API results
    search_results: NotRequired[list[str] | None]  # List of raw document chunks
    customer_history: NotRequired[dict | None]  # Raw customer data from CRM

    # Generated content
    draft_response: NotRequired[str | None]
    messages: NotRequired[list[HumanMessage | AIMessage | SystemMessage]]
