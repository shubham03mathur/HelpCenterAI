from enum import Enum

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PENDING_REVIEW = "PENDING_REVIEW"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"