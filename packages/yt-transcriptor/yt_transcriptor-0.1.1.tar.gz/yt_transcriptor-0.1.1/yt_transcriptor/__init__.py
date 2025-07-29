"""
yt-transcriptor

A CLI and library to download audio from a video, transcribe it using Whisper,
and save the transcription to a file.
"""

__version__ = "0.1.1"

from .core import download_and_transcribe, format_timestamp

__all__ = ["download_and_transcribe", "format_timestamp"]
