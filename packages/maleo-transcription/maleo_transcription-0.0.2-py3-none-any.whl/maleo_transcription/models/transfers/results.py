from pydantic import BaseModel, Field
from typing import Optional
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_transcription.models.transfers.general import (
    AudioPropertiesTransfers,
    TranscribePropertiesTransfers,
    TranscribeTransfers
)

class ResultMetadata(BaseModel):
    audio:AudioPropertiesTransfers = Field(..., description="Audio Properties")
    transcribe:TranscribePropertiesTransfers = Field(..., description="Transcribe Properties")

class MaleoTranscriptionResultsTransfers:
    class Fail(BaseResultSchemas.Fail): pass

    class SingleData(BaseResultSchemas.SingleData):
        data:TranscribeTransfers = Field(..., description="Single transcribe data")
        metadata:Optional[ResultMetadata] = Field(None, description="Optional metadata")