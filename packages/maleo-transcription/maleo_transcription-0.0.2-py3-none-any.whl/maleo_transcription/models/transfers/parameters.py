from pydantic import Field
from maleo_transcription.models.schemas import MaleoTranscriptionSchemas
from maleo_transcription.models.transfers.general import OriginalAudioTransfers

class MaleoTranscriptionParametersTransfers:
    class TranscribeController(
        MaleoTranscriptionSchemas.Expand,
        MaleoTranscriptionSchemas.AudioFile,
        MaleoTranscriptionSchemas.Language
    ): pass

    class TranscribeService(MaleoTranscriptionSchemas.Language):
        audio:OriginalAudioTransfers = Field(..., description="Original audio")