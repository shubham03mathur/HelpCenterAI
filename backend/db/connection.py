from typing import Any, Dict

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import JSON, String, Float, Enum

from common_types.enums import JobStatus


DB_URL = "sqlite+aiosqlite:///ava.db"
engine = create_async_engine(DB_URL, connect_args={"check_same_thread": False})
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class JobTracking(Base):
    __tablename__ = "job_tracking"
    
    thread_id: Mapped[str] = mapped_column(String, primary_key=True)
    run_id: Mapped[str] = mapped_column(String)
    conversation_id: Mapped[str] = mapped_column(String)
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus),
        default=JobStatus.PENDING,
        nullable=False
    )
    interrupt_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    result: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[float] = mapped_column(Float)
    error: Mapped[str] = mapped_column(String, nullable=True)

async def get_db():
    async with async_session() as session:
        yield session
