import os
import wave
import json
import shutil
import logging
import argparse
from typing import Union, Optional, List, Tuple
import numpy as np
import librosa
from pydub import AudioSegment
from pathlib import Path

# Constants
AUDIO_KEYFRAMES_FILENAME = "audio_keyframes.json"

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Audio processing and keyframe generation.")
    parser.add_argument("-f", "--file", type=str, required=True, help="Input audio file.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second.")
    parser.add_argument("--music_cut", action="store_true", help="Option to cut the music.")
    parser.add_argument("--musicstart", type=str, help="Start time of the music (in minutes,seconds).")
    parser.add_argument("--musicend", type=str, help="End time of the music (in minutes,seconds).")
    parser.add_argument("--speed", type=float, default=0.4, help="Reactive impact of the audio on the animation.")
    return parser.parse_args()

def convert_time_to_seconds(time_str: str) -> Union[int, float]:
    """Convert time string to seconds."""
    try:
        minutes, seconds = map(int, time_str.split(","))
        return minutes * 60 + seconds
    except ValueError:
        logging.error(f"Invalid time format: {time_str}")
        exit(1)

def validate_file(file_path: str) -> None:
    """Validate if the file exists and is a wave file."""
    if not Path(file_path).exists() or not file_path.endswith(".wav"):
        logging.error(f"The file {file_path} does not exist or is not a wave file.")
        exit(1)

def copy_and_get_new_file_name(src: str, suffix: str) -> str:
    """Copy the source file and generate a new name for the copied file."""
    file_stem = Path(src).stem
    i = 0
    new_file = f"{file_stem}_{suffix}_{i}.wav"

    while Path(new_file).exists():
        i += 1
        new_file = f"{file_stem}_{suffix}_{i}.wav"

    shutil.copyfile(src, new_file)
    return new_file

def crop_audio(args: argparse.Namespace) -> str:
    """Crop the audio file based on the given arguments."""
    logging.info("Cropping audio...")
    src = args.file
    validate_file(src)
    cropped_file = copy_and_get_new_file_name(src, "cut")

    start_time = convert_time_to_seconds(args.musicstart) if args.musicstart else 0
    end_time = convert_time_to_seconds(args.musicend) if args.musicend else librosa.get_duration(filename=cropped_file)

    with wave.open(cropped_file, "rb") as infile, wave.open(cropped_file, 'w') as outfile:
        nchannels, sampwidth, framerate, _ = infile.getparams()
        infile.setpos(int(start_time * framerate))
        data = infile.readframes(int((end_time - start_time) * framerate))
        
        outfile.setparams((nchannels, sampwidth, framerate, 0, 'NONE', 'not compressed'))
        outfile.writeframes(data)

    logging.info(f"Your new cropped file is {int(end_time - start_time)} seconds long.")
    logging.info(f"The name of your new cropped file is {cropped_file} and your original non-cropped file is {args.file}")
    return cropped_file

def generate_keyframes(args: argparse.Namespace, cropped_file: str) -> None:
    """Generate keyframes based on the audio."""
    logging.info("Generating keyframes...")
    x, sr = librosa.load(cropped_file)
    onset_frames = librosa.onset.onset_detect(x, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    fps = args.fps
    duration = librosa.get_duration(filename=cropped_file)
    total_frames = int(duration * fps)
    vals, _ = np.histogram(onset_times, bins=total_frames, range=(0, duration))

    key_frame_value = [f"{i}:({args.speed})," for i, val in enumerate(vals) if val > 0]
    key_frame_string = "".join(key_frame_value)

    with open(AUDIO_KEYFRAMES_FILENAME, "w") as fp:
        json.dump(key_frame_string, fp)

    logging.info(f"Keyframes exported to {AUDIO_KEYFRAMES_FILENAME}")

if __name__ == "__main__":
    args = parse_args()

    if args.music_cut:
        cropped_file = crop_audio(args)
    else:
        logging.info("Audio not cropped.")
        cropped_file = args.file

    generate_keyframes(args, cropped_file)