from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, root_validator
from uuid import UUID

from ..core.schema import AttributeSource, AttributeType

class AttributeTypeCreate(str, Enum):
    TEXT = "Text"
    NUMBER = "Number"
    DATE = "Date"
    TIME = "Time"
    DATETIME = "DateTime"

class SchemaCreate(BaseModel):
    key: str | None = Field(None, pattern=r"^[A-Za-z_]*$")
    name: str | None = None
    description: str | None
    source: AttributeSource = AttributeSource.DOC_DATA
    type: AttributeTypeCreate | None = None
    is_array: bool = False
    children: list["SchemaCreate"] | None = None # top-level schema needs to contain at least one child

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "key": "main_actor",  # key should be snake_case
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
                }
            ]
        }
    
    @root_validator(pre=True)
    def validate_key_present(cls, values):
        if not values.get('name') and not values.get('key'):
            raise ValueError("Either 'name' or 'key' must be provided.")
        return values
    
    @root_validator(pre=True)
    def validate_attribute_type_exists(cls, values):
        if values.get('type') is None and (values.get('children') is None or len(values.get('children')) == 0):
            raise ValueError("Attributes (childless schemas) require 'type' to be set.")
        return values

class SchemaResponse(BaseModel):
    id: UUID
    key: str
    name: str
    description: str | None
    source: AttributeSource
    type: AttributeType | None
    is_array: bool
    children: list["SchemaResponse"] | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": "925e106a-9b57-4a8a-baae-c35042ea275c",
                    "key": "letter",
                    "name": "Simple Letter",
                    "description": "A simple letter with recipient details, title, and body.",
                    "source": "data",
                    "type": None, # can remove?
                    "is_array": False,
                    "children": [
                        {
                        "id": "aebf8f71-1cd8-48f9-8b67-2b0472b88826",
                        "key": "recipient_address",
                        "name": "Recipient Address",
                        "description": "The address the letter is sent to.",
                        "source": "data",
                        "type": "ADDRESS",
                        "is_array": False,
                        "children": [
                             {
                                "id": "df015a23-5827-4983-8d0a-d8345ac466c",
                                "key": "recipient_name",
                                "name": "Recipient Name",
                                "description": "The name of the letter's recipient.",
                                "source": "data",
                                "type": "TEXT",
                                "is_array": False,
                                "children": None,
                                "created_at": "2024-10-24T12:00:00",
                                "updated_at": None
                            },
                            {
                                "id": "8deceae5-9aac-454f-b32b-f7302302fe36",
                                "key": "recipient_address",
                                "name": "Recipient Address",
                                "description": "The address of the letter's recipient.",
                                "source": "data",
                                "type": "TEXT",
                                "is_array": False,
                                "children": None,
                                "created_at": "2024-10-24T12:00:00",
                                "updated_at": None
                            },
                        ],
                        "created_at": "2024-10-24T12:00:00",
                        "updated_at": None
                        },
                        {
                        "id": "1b7482c8-bfef-4184-b162-1589248481ae",
                        "key": "subject",
                        "name": "Subject",
                        "description": "The subject of the letter.",
                        "source": "data",
                        "type": "TEXT",
                        "is_array": False,
                        "children": None,
                        "created_at": "2024-10-24T12:00:00",
                        "updated_at": None
                        },
                        {
                        "id": "9eecef2c-121c-4ed2-a93a-255b84dc750c",
                        "key": "body",
                        "name": "Body",
                        "description": "The body of the letter.",
                        "source": "user_defined",
                        "type": "TEXT",
                        "is_array": False,
                        "children": None,
                        "created_at": "2024-10-24T12:00:00",
                        "updated_at": None
                        }
                    ],
                    "created_at": "2024-10-24T12:00:00",
                    "updated_at": None
                }
            ]
        }