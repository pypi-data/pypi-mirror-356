from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from ..core.file import FileType

class UploadRequest(BaseModel):
    filename: str
    content_type: str
class UploadResponse(BaseModel):
    upload_token: str
    upload_url: str
    object_key: str

class CreateFileRequest(BaseModel):
    upload_token: str

class FileResponse(BaseModel):
    id: UUID
    filename: str
    filetype: FileType
    size: int
    num_pages: int
    upload_time: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": "f73d464e-b8fd-40b0-9f13-44d476af4c91",
                    "filename": "Invoice 2024-10-24.pdf",
                    "filetype": "application/pdf",
                    "size": 43627,
                    "upload_time": "2024-10-24T18:37:41.354093",
                }
            ]
        }