from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any
from uuid import UUID

from ..core.run import RunStatus

class FileExtractionResult(BaseModel):
    file_id: UUID
    file_name: str
    data: Dict[str, Any] | None

class RunResult(BaseModel):
    results: list[FileExtractionResult]
    errors: list[str]

class RunCreate(BaseModel):
    file_ids: list[UUID]
    status: RunStatus = RunStatus.READY

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "file_ids": [
                        "f73d464e-b8fd-40b0-9f13-44d476af4c91",
                        "e996b436-96df-4867-90f5-fe5d6f2916c1",
                    ],
                }
            ]
        }

class RunUpdate(BaseModel):
    file_ids: list[UUID] | None = None
    status: RunStatus | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "status": "ready",
                }
            ]
        }

class RunResponse(BaseModel):
    run_num: int
    workflow_id: UUID
    file_ids: list[UUID]
    status: RunStatus
    results: RunResult | None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "run_num": 1,
                    "workflow_id": "36060877-5005-4fcd-9d96-5a729d9f5292",
                    "file_ids": [
                        "f73d464e-b8fd-40b0-9f13-44d476af4c91"
                    ],
                    "status": RunStatus.DRAFT,
                    "results": None,
                    "created_at": "2024-10-24T18:37:41.354093",
                    "updated_at": None
                }
            ]
        }