from typing import Union
from maleo_transcription.models.transfers.results import MaleoTranscriptionResultsTransfers

class MaleoTranscriptionResultsTypes:
    Transcribe = Union[
        MaleoTranscriptionResultsTransfers.Fail,
        MaleoTranscriptionResultsTransfers.SingleData
    ]