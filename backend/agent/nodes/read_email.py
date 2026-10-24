from common_types.AgentState import AgentState
from langchain.messages import HumanMessage

def read_email(state: AgentState) -> dict:
    """ Parse and read email/message """
    return {
        "messages": [HumanMessage(content=f"Processing email: {state['message']}")]
    }
