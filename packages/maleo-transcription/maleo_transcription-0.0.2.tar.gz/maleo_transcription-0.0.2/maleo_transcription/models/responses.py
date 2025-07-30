from pydantic import Field
from typing import Optional
from maleo_foundation.models.responses import BaseResponses
from maleo_transcription.models.transfers.general import TranscribeTransfers
from maleo_transcription.models.transfers.results import ResultMetadata

class MaleoTranscriptionResponses:
    class TranscribeFailed(BaseResponses.BadRequest):
        code:str = "TRN-SCB-002"
        message:str = "Failed transcribing audio"

    class TranscribeSuccess(BaseResponses.SingleData):
        code:str = "TRN-SCB-003"
        message:str = "Successfully transcribed audio"
        description:str = "The given audio has been successfully transcribed"
        data:TranscribeTransfers = Field(..., description="Single transcribe data")
        metadata:Optional[ResultMetadata] = Field(None, description="Optional metadata")