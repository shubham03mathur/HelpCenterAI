import time

from sqlalchemy import select
from common_types.enums import JobStatus
from common_types.AgentState import AgentRunSchema
from agent.graph import workflow
from .connection import JobTracking, async_session

from langchain_core.runnables import RunnableConfig

async def create_agent_run(schema: AgentRunSchema):
    run_id = schema['run_id']
    thread_id = schema['thread_id']
    conversation_id = schema['conversation_id']
    message = schema['message']

    async with async_session() as session:
        job = JobTracking(
            run_id=run_id,
            thread_id=thread_id,
            conversation_id=conversation_id,
            status=JobStatus.PENDING,
            created_at=time.time(),
            updated_at=time.time()
        )
        session.add(job)
        await session.commit()

async def update_agent_run(
    run_id: str,
    status: JobStatus,
    result: dict | None = None,
    error: str | None = None
):
    """Utility helper to cleanly update task metrics globally"""
    async with async_session() as session:
        from sqlalchemy import select
        db_result = await session.execute(select(JobTracking).where(JobTracking.run_id == run_id))
        job = db_result.scalar_one()

        job.status = status
        job.updated_at = time.time()
        if result:
            job.result = result
        if error:
            job.error = error

        await session.commit()

async def find_agent_run(
    thread_id: str
):
    async with async_session() as session:
        from sqlalchemy import select
        clean_thread_id = str(thread_id).strip()
        db_result = await session.execute(select(JobTracking).where(JobTracking.thread_id == clean_thread_id))
        return db_result.scalar_one()