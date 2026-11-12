from uuid import uuid4

from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from contextlib import asynccontextmanager

from langgraph.types import Command
from db.connection import Base, engine
from db.run import create_agent_run, find_agent_run, update_agent_run
from common_types.AgentState import AgentRunSchema, AgentState, ConversationState, ReviewState
from common_types.enums import JobStatus

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from agent.graph import workflow


from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Help Center AI", lifespan=lifespan)


@app.get("/")
async def health():
    return {"status": "OK"}

async def execute_agent_run(
    run_id: str,
    thread_id: str,
    message: str,
    request: ConversationState
):
    try:
        await update_agent_run(run_id, status=JobStatus.RUNNING)
        async with AsyncSqliteSaver.from_conn_string("ava.db") as memory:
            config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
            w_app = workflow.compile(checkpointer=memory)
            initial_state: AgentState = {
                "message": message,
                "draft_response": None,
                "sender_email": request.email,
                "conversation_id": request.conversation_id
            }

            result = await w_app.ainvoke(initial_state, config=config)

            interrupts = result.get("__interrupt__", [])
            if interrupts:
                await update_agent_run(
                    run_id,
                    JobStatus.PENDING_REVIEW,
                    result={"interrupt": interrupts[0].value}
                )
                return
            agent_summary = {"output": result.get("draft_response", "Task complete")}
            await update_agent_run(run_id, status=JobStatus.COMPLETED, result=agent_summary)

    except Exception as e:
        await update_agent_run(run_id, status=JobStatus.FAILED, error=str(e))

@app.post(
    "/conversations/{conversation_id}/messages", status_code=status.HTTP_202_ACCEPTED
)
async def agent_run(
    conversation_id: str,
    cx_message: ConversationState,
    background_tasks: BackgroundTasks,
):
    thread_id = conversation_id
    run_id = str(uuid4())
    message = f"""
           Customer is enquiring about topic: {cx_message.topic}\n
           concern: { cx_message.concern }
        """
    schema: AgentRunSchema = {
        "message": message,
        "run_id": run_id,
        "conversation_id": conversation_id,
        "thread_id": thread_id,
    }
    await create_agent_run(schema)

    background_tasks.add_task(
        execute_agent_run,
        run_id,
        thread_id,
        message,
        request=cx_message
    )

    return {
        "run_id": run_id,
        "thread_id": thread_id,
        "status": "queued",
    }

@app.post('/agent-runs/{conversation_id}/resume')
async def resume(request: ReviewState):
    
    thread_id = str(request.conversation_id).strip()
    print("🚀 ~ resume ~ thread_id:", thread_id)
    draft_response = request.payload.get('draft_response','')
    print("🚀 ~ resume ~ draft_response:", draft_response)
    decision = request.payload.get('decision','')
    print("🚀 ~ resume ~ decision:", decision)

    job = await find_agent_run(thread_id)

    try:
        if not job:
            raise HTTPException(
                status_code=404, 
                detail=f"No agent run found for thread_id: {thread_id}"
            )

        draft_response = request.payload.get('draft_response', '')
        decision = request.payload.get('decision', '')

        config: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id
            }
        }
        
        resume_value = {
            "decision": decision,
            "edited_draft": draft_response,
        }

        # Always pass thread_id (your primary key), not job.run_id
        await update_agent_run(job.run_id, status=JobStatus.RUNNING)

        # Ensure "ava.db" matches the exact path used in your start endpoint
        async with AsyncSqliteSaver.from_conn_string("ava.db") as memory:
            w_app = workflow.compile(checkpointer=memory)
            
            # Verify the thread actually has a paused checkpoint before resuming
            current_state = await w_app.aget_state(config)
            if not current_state.next:
                raise HTTPException(
                    status_code=400,
                    detail=f"Thread {thread_id} is not paused at an interrupt."
                )

            result = await w_app.ainvoke(
                Command(resume=resume_value),
                config=config
            )

            interrupts = result.get("__interrupt__", [])
            if interrupts:
                await update_agent_run(
                    job.run_id,
                    status=JobStatus.PENDING_REVIEW,
                    result={"interrupt": interrupts[0].value}
                )
            else:
                await update_agent_run(
                    job.run_id,
                    status=JobStatus.COMPLETED,
                    result={
                        "final_response": result.get("draft_response"),
                        "sender_email": result.get("sender_email"),
                        "decision": decision,
                    }
                )

        return {
            "thread_id": thread_id,
            "run_id": job.run_id,
            "status": JobStatus.COMPLETED if not interrupts else JobStatus.PENDING_REVIEW,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Resume failed for {thread_id}: {e}")
        await update_agent_run(job.run_id, status=JobStatus.FAILED, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))