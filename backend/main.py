from fastapi import FastAPI, Response
from common_types.AgentState import ConversationState, AgentState
from agent.graph import workflow_app

from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Help Center AI")

@app.get('/')
async def health():
    return { "status": "OK" }

@app.post('/conversations/{conversation_id}/messages')
async def create_item(conversation_id: str, message: ConversationState):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": conversation_id
        }
    }

    customer_concern = f"""
       Customer is enquiring about {message.topic} and
       here are the details: { message.concern }
    """
    sender_email = message.email

    initial_state: AgentState = {
        "conversation_id": conversation_id,
        "sender_email": sender_email,
        "message": customer_concern
    }

    result = await workflow_app.ainvoke(initial_state, config=config)

    interrupts = result.get("__interrupt__", [])

    if interrupts:
        return {
            "status": "interrupted - awaiting human review",
            "thread_id": conversation_id,
            "interrupt": interrupts[0].value
        }

    return {
        "status": "completed",
        "thread_id": conversation_id,
        "result": result,
    }
