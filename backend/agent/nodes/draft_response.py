from common_types.AgentState import AgentState
from langgraph.types import Command
from typing_extensions import Literal

from agent.llm import llm
from langsmith import traceable

@traceable
def draft_response(state: AgentState) -> Command[Literal['human_review', 'send_reply']]:
    """ Draft a response based on given context and route based on quality """
    classification = state.get('classification', {})

    context = []

    if state.get('search_results'):
        docs = "\n".join([ f"- {doc}" for doc in state['search_results']])
        context.append(f"Relevant documentation:\n{docs}")

    if state.get('customer_history'):
        # Format customer data for the prompt
        context.append(f"Customer tier: {state['customer_history'].get('tier', 'standard')}")

    prompt = f"""
    Draft an email for this customer:
    sender_email: {state['sender_email']}

    Intent: {classification['intent']}
    Urgency: {classification['urgency']}
    
    {chr(10).join(context)}
    
    Guidelines:
    - Be professional and helpful
    - Address their specific concern
    - Use the provided documentation when relevant
    """

    response = llm.invoke(prompt)

    need_review = (
        classification.get('intent') in ['complex', 'billing'] or
        classification.get('urgency') in ["high", "critical"]
    )

    goto = 'human_review' if need_review else 'send_reply'

    return Command(
        update={"draft_response": response.content},  # Store only the raw response
        goto=goto
    )
