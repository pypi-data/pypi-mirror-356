from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from .schema import SchemaCreate, SchemaResponse

class WorkflowCreate(BaseModel):
    name: str
    extraction_schema: SchemaCreate

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "name": "Main actor identifier",
                    "extraction_schema": {
                        "key": "main_actor",  # key should be snake case
                        "name": "Main Actor",  # this can be optional if `key` is provided
                        "description": "The person playing the main role in the script",
                        "source": "data",  # must match one of the AttributeSource enum values
                        "type": "Text",  # must match one of the AttributeType enum values
                        "is_array": False,  # boolean field
                        "children": [
                            {
                                "key": "last_name",
                                "name": "Last Name",
                                "description": "Last name of the main actor",
                                "source": "data",
                                "type": "Text",
                                "is_array": False,
                                "children": None
                            },
                            {
                                "name": "Age",
                                "description": "Age of the main actor",
                                "source": "data",
                                "type": "Number",
                                "is_array": False,
                                "children": None
                            }
                        ]
                    },
                }
            ]
        }

class WorkflowUpdate(BaseModel):
    name: str | None = None
    extraction_schema: SchemaCreate | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "name": "New name for workflow",
                }
            ]
        }


class WorkflowResponse(BaseModel):
    id: UUID
    name: str
    extraction_schema: SchemaResponse
    runs: list[int]
    created_at: datetime
    updated_at: datetime | None
    created_by: UUID

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": "d83862c1-4e10-4bef-8c40-26b774c3cd38",
                    "name": "Total spend extraction",
                    "extraction_schema": {
                        "id": "439-7f425-4618-481d-9dc9-0eccb1b90aa4",
                        "key": "total_amount",
                        "name": "Total Amount",
                        "description": "The total amount logged on the invoice",
                        "source": "data",
                        "type": "NUMBER",
                        "is_array": True,
                        "children": None,
                        "created_at": "2024-10-24T12:00:00",
                        "updated_at": None
                    },
                    "runs": [1,2,3,4],
                    "created_at": "2024-10-24T12:00:00",
                    "updated_at": None,
                    "created_by": "e4ecd95c-8b4c-41b8-8b00-6acae02e868a",
                }
            ]
        }
