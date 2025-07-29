import os
import sys
import tempfile
import whisper
import yt_dlp
import datetime
import shutil


def format_timestamp(seconds: float) -> str:
    """
    Converts a time in seconds to a formatted string HH:MM:SS.

    Args:
        seconds (float): The time in seconds.

    Returns:
        str: The formatted timestamp string.
    """
    assert seconds >= 0, "non-negative timestamp"
    td = datetime.timedelta(seconds=seconds)
    return str(td)


def download_and_transcribe(
    video_url: str,
    output_file: str,
    model: str,
    include_timestamps: bool,
    cleanup_cache: bool,
    verbose: bool = True,
):
    """
    Downloads audio from a video URL, transcribes it, and saves the transcription.

    Args:
        video_url (str): The URL of the video to process.
        output_file (str): The path to save the transcription file.
        model (str): The Whisper model to use.
        include_timestamps (bool): Whether to include timestamps in the output.
        cleanup_cache (bool): Whether to delete the temporary audio file.
        verbose (bool): Whether to print progress and status messages.
    """
    temp_dir = tempfile.mkdtemp()

    def log_message(message: str, error: bool = False):
        if verbose:
            print(message, file=sys.stderr if error else sys.stdout)

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
            "quiet": not verbose,
        }

        log_message(f"Downloading audio from: {video_url}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                downloaded_files = os.listdir(temp_dir)
                if not downloaded_files:
                    log_message("Error: Audio download failed.", error=True)
                    return
                audio_file_path = os.path.join(temp_dir, downloaded_files[0])
                log_message(f"Audio downloaded to temporary file: {audio_file_path}")

        except yt_dlp.utils.DownloadError as e:
            log_message(f"Error downloading video: {e}", error=True)
            return
        except Exception as e:
            log_message(
                f"An unexpected error occurred during download: {e}", error=True
            )
            return

        log_message("Loading Whisper model...")
        model = whisper.load_model(model)
        log_message("Transcribing audio... (This may take some time)")

        try:
            result = model.transcribe(audio_file_path, fp16=False)

            if include_timestamps:
                lines = []
                for segment in result["segments"]:
                    start_time = format_timestamp(segment["start"])
                    text = segment["text"].strip()
                    lines.append(f"[{start_time}] {text}")
                transcription = "\n".join(lines)
            else:
                transcription = result["text"]

        except Exception as e:
            log_message(f"An error occurred during transcription: {e}", error=True)
            return

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcription)
            log_message(f"Transcription successfully saved to: {output_file}")
        except IOError as e:
            log_message(f"Error writing to output file: {e}", error=True)

    finally:
        if cleanup_cache:
            log_message(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir)
        else:
            log_message(f"Temporary files kept at: {temp_dir}")
