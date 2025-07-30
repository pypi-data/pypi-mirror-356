from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import Optional, List
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_transcription.enums import MaleoTranscriptionEnums

class MaleoTranscriptionSchemas:
    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoTranscriptionEnums.ExpandableFields]] = Field(None, description="Expanded Fields")

    class Language(BaseModel):
        language:MaleoTranscriptionEnums.Languange = Field(MaleoTranscriptionEnums.Languange.ID, description="Audio language")

    class AudioFile(BaseModel):
        audio:UploadFile = Field(..., description="Audio File")

    class Name(BaseModel):
        name:str = Field(..., description="Audio file name")

    class Size(BaseModel):
        size:int = Field(..., ge=0, description="Audio file size")

    class MimeType(BaseModel):
        mime_type:str = Field(..., description="Audio file mime type")

    class Format(BaseModel):
        format:str = Field(..., description="Audio file format")

    class AudioData(BaseModel):
        data:bytes = Field(..., description="Audio data")

    class Duration(BaseModel):
        duration:float = Field(0, description="Audio Duration")

    class Channels(BaseModel):
        channels:int = Field(..., description="WAV Audio Number of Channels")

    class SampleWidth(BaseModel):
        sample_width:int = Field(..., description="WAV Audio Sample Width")

    class FrameRate(BaseModel):
        frame_rate:int = Field(..., description="WAV Audio Frame Rate")

    class NumberOfFrames(BaseModel):
        number_of_frames:int = Field(..., description="WAV Audio Number of Frames")