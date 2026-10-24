from common_types.AgentState import AgentState, EmailClassification
from langgraph.types import Command
from typing import cast, Literal

from langsmith import traceable

@traceable
def search(state: AgentState) -> Command[Literal['draft_response']]:
    """ search the documents for answers for any queries or features """
    classification = cast(EmailClassification, state.get('classification', {}))
    query = f" topic: {classification.get('topic', '')} Intent: {classification.get('intent', '')}"

    try:
        search_results = [
            "Reset password via Settings > Security > Change Password",
            "Password must be at least 12 characters",
            "Include uppercase, lowercase, numbers, and symbols"
        ]
    except Exception as e:
        print('Could not find relvant info in store.')
        search_results = [f"Search temporarily unavailable: {str(e)}"]

    return Command(
        update={"search_results": search_results },
        goto='draft_response'
    )
