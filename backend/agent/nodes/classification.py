from typing import cast
from typing_extensions import Literal
from langchain.chat_models import init_chat_model
from common_types.AgentState import EmailClassification, AgentState
from langgraph.types import Command


llm = init_chat_model('ollama:gemma4:12b-mlx')

from langsmith import traceable

@traceable
def email_classification(state: AgentState) -> Command[Literal["human_review", "search_documentation", "draft_response"]]:
    """ Use LLM to classify email intent and urgency, then route accordingly """

    llm_with_structured_output = llm.with_structured_output(EmailClassification)

    prompt = f"""
    analyse this customer email/message and classify it.
    Email: {state['message']}
    From: {state['sender_email']}

    Provide classification including intent, urgency, topic, and summary.

    """

    classification = cast(
        EmailClassification,
        llm_with_structured_output.invoke(prompt),
    )

    # if classification['intent'] == 'billing' or classification["urgency"] == 'critical':
    #     goto = 'human_review'
    if classification['intent'] in ['question', 'feature']:
        goto = "search_documentation"
    else:
        goto = 'draft_response'

    return Command(
        update={"classification": classification},
        goto=goto
    )
