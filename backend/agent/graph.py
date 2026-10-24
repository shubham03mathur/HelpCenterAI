from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph import START, END

from common_types.AgentState import AgentState
from agent import read_email, email_classification, human_review, draft_response, search, send_reply

workflow = StateGraph(AgentState)

workflow.add_node("read_email", read_email)
workflow.add_node('email_classification', email_classification)
workflow.add_node('search_documentation', search)
workflow.add_node('human_review', human_review)
workflow.add_node('draft_response', draft_response)
workflow.add_node('send_reply', send_reply)

workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "email_classification")
workflow.add_edge('send_reply', END)

memory = MemorySaver()
workflow_app = workflow.compile(checkpointer=memory)
