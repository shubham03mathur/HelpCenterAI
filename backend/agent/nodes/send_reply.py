from common_types.AgentState import AgentState

from langsmith import traceable

@traceable
def send_reply(state: AgentState) -> dict:
    """Send the email response"""
    # Integrate with email service
    print(f"Sending reply: {state['draft_response'][:100]}...")
    return {}
