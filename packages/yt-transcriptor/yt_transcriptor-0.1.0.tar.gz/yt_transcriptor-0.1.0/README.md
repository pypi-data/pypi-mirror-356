# yt-transcribe

A CLI tool to download audio from a video, transcribe it using [Whisper](https://github.com/openai/whisper), and save the transcription to a file.

## Usage

```
Usage: yt-transcribe [OPTIONS] VIDEO_URL OUTPUT_PATH

  Downloads audio from a video URL, transcribes it, and saves the result.

Options:
  --version                       Show the version and exit.
  --model [tiny|base|small|medium|large]
                                  Select the Whisper model to use.
  --timestamps                    Include timestamps in the output file (e.g.,
                                  [0:00:00] Text).
  --cleanup / --no-cleanup        Delete the temporary audio file after
                                  transcription. Use --no-cleanup to keep it.
  --logging / --no-logging        Enable or disable logging to stdout.
  --help                          Show this message and exit.
```
