import click
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


logging_enabled = True


def echo(
    message: str,
    file=None,
):
    if logging_enabled:
        click.echo(message, file)


def download_and_transcribe(
    video_url: str,
    output_file: str,
    model: str,
    include_timestamps: bool,
    delete_cache: bool,
):
    """
    Downloads audio from a video URL, transcribes it, and saves the transcription.

    Args:
        video_url (str): The URL of the video to process.
        output_file (str): The path to save the transcription file.
        model (str): The Whisper model to use.
        include_timestamps (bool): Whether to include timestamps in the output.
        delete_cache (bool): Whether to delete the temporary audio file.
    """
    temp_dir = tempfile.mkdtemp()

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
            "quiet": True,
        }

        echo(f"Downloading audio from: {video_url}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                downloaded_files = os.listdir(temp_dir)
                if not downloaded_files:
                    echo("Error: Audio download failed.", file=sys.stderr)
                    return
                audio_file_path = os.path.join(temp_dir, downloaded_files[0])
                echo(f"Audio downloaded to temporary file: {audio_file_path}")

        except yt_dlp.utils.DownloadError as e:
            echo(f"Error downloading video: {e}", file=sys.stderr)
            return
        except Exception as e:
            echo(f"An unexpected error occurred during download: {e}", file=sys.stderr)
            return

        echo("Loading Whisper model...")
        model = whisper.load_model(model)
        echo("Transcribing audio... (This may take some time)")

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
            echo(f"An error occurred during transcription: {e}", file=sys.stderr)
            return

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcription)
            echo(f"Transcription successfully saved to: {output_file}")
        except IOError as e:
            echo(f"Error writing to output file: {e}", file=sys.stderr)

    finally:
        if delete_cache:
            echo(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir)
        else:
            echo(f"Temporary files kept at: {temp_dir}")


@click.command(
    help="Downloads audio from a video URL, transcribes it, and saves the result."
)
@click.version_option()
@click.argument("video_url", type=str)
@click.argument("output_path", type=click.Path())
@click.option(
    "--model",
    type=click.Choice(["tiny", "base", "small", "medium", "large"]),
    default="base",
    help="Select the Whisper model to use.",
)
@click.option(
    "--timestamps",
    is_flag=True,
    default=False,
    help="Include timestamps in the output file (e.g., [0:00:00] Text).",
)
@click.option(
    "--cleanup/--no-cleanup",
    "delete_cache",
    default=True,
    help="Delete the temporary audio file after transcription. Use --no-cleanup to keep it.",
)
@click.option(
    "--logging/--no-logging",
    "logging_flag",
    default=True,
    help="Enable or disable logging to stdout.",
)
def cli(
    video_url: str,
    output_path: str,
    model: str,
    timestamps: bool,
    delete_cache: bool,
    logging_flag: bool,
):
    """
    A CLI tool to download audio from a video, transcribe it using Whisper,
    and save the transcription to a specified file.

    VIDEO_URL: The URL of the video to transcribe (e.g., from YouTube).
    OUTPUT_PATH: The file path to save the transcription text.
    """

    global logging_enabled
    logging_enabled = logging_flag

    download_and_transcribe(
        video_url=video_url,
        output_file=output_path,
        include_timestamps=timestamps,
        delete_cache=delete_cache,
        model=model,
    )
