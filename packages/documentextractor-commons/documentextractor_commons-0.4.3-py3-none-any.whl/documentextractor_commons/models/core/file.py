from enum import Enum

class FileType(str, Enum):
    PDF = "application/pdf"
    HTML = "text/html"
    RTF = "application/rtf"
    DOC = "application/msword"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    PPT = "application/vnd.ms-powerpoint"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

    # Currently supported: PDF, HTML, DOCX, PPTX
    # All others have storage not implemented!