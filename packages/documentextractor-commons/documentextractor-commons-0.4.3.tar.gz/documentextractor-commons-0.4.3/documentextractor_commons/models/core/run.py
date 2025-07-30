from enum import Enum

class RunStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class RunResultResponseFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"