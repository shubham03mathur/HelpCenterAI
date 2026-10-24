from langgraph.graph import END
from langgraph.types import Command, interrupt
from typing_extensions import Literal

from common_types.AgentState import AgentState, EmailClassification
from langsmith import traceable
from typing import cast

@traceable
def human_review(state: AgentState) -> Command[Literal['send_reply', END]]:
    """ Pause for human review with interrupt (and route based on desicion """
    classification = cast(EmailClassification, state.get('classification', {}))

    human_decision = interrupt({
        "question": "Do you want to proceed with this action?",
        "details": {
            "email_id": state.get('email_id',''),
            "original_email": state.get('message',''),
            "draft_response": state.get('draft_response',''),
            "urgency": classification.get('urgency'),
            "intent": classification.get('intent'),
            "action": "Please review and approve/edit this response"
        }
    })

    if human_decision.get("approved"):
        return Command(
            update={"draft_response": human_decision.get("edited_response", state.get('draft_response',''))},
            goto="send_reply"
        )
    else:
        # rejection means it will be handled manually
        return Command(update={}, goto=END)
    

