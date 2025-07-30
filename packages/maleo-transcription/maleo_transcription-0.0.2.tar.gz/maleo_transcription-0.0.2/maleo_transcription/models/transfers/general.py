from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Self, Tuple
from maleo_transcription.models.schemas import MaleoTranscriptionSchemas

class OriginalAudioPropertiesTransfers(
    MaleoTranscriptionSchemas.Format,
    MaleoTranscriptionSchemas.MimeType,
    MaleoTranscriptionSchemas.Size,
    MaleoTranscriptionSchemas.Name
): pass

class OriginalAudioTransfers(
    MaleoTranscriptionSchemas.AudioData,
    OriginalAudioPropertiesTransfers
): pass

class ConvertedAudioPropertiesTransfers(
    MaleoTranscriptionSchemas.Size,
    MaleoTranscriptionSchemas.Duration,
    MaleoTranscriptionSchemas.NumberOfFrames,
    MaleoTranscriptionSchemas.FrameRate,
    MaleoTranscriptionSchemas.SampleWidth,
    MaleoTranscriptionSchemas.Channels
):
    @model_validator(mode="after")
    def calculate_duration(self) -> Self:
        if self.frame_rate == 0:
            self.duration = 0
        else:
            self.duration = self.number_of_frames/self.frame_rate

        return self

class AudioPropertiesTransfers(BaseModel):
    original:OriginalAudioPropertiesTransfers = Field(..., description="Original audio properties")
    converted:Optional[ConvertedAudioPropertiesTransfers] = Field(None, description="Converted audio properties")

class TranscribePropertiesTransfers(BaseModel):
    duration:float = Field(..., description="Transcribe duration")

class TranscribeChunk(BaseModel):
    timestamp:Tuple[float, float] = Field(..., description="Timestamp")
    text:str = Field(..., description="Text")

class TranscribeTransfers(BaseModel):
    text:str = Field(..., description="Transcribe text")
    chunks:List[TranscribeChunk] = Field(..., description="List of transcribe chunk")