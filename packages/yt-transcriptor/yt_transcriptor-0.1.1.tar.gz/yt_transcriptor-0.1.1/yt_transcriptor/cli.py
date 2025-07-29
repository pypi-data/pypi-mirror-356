import click
from .core import download_and_transcribe as core_download_and_transcribe


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
    core_download_and_transcribe(
        video_url=video_url,
        output_file=output_path,
        model=model,
        include_timestamps=timestamps,
        cleanup_cache=delete_cache,
        verbose=logging_flag,
    )
