import os
import wave
import json
import shutil
import argparse
import numpy as np
import librosa
from pydub import AudioSegment
from pathlib import Path
from os import path

def parse_args():
    parser = argparse.ArgumentParser(description="Audio processing and keyframe generation.")
    parser.add_argument("-f", "--file", type=str, required=True, help="Input audio file.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second.")
    parser.add_argument("--music_cut", action="store_true", help="Option to cut the music.")
    parser.add_argument("--musicstart", type=str, help="Start time of the music (in minutes,seconds).")
    parser.add_argument("--musicend", type=str, help="End time of the music (in minutes,seconds).")
    parser.add_argument("--speed", type=float, default=0.4, help="Reactive impact of the audio on the animation.")
    return parser.parse_args()

def convert_time_to_seconds(time_str):
    if "," in time_str:
        minutes, seconds = map(int, time_str.split(","))
        return minutes * 60 + seconds
    else:
        return int(time_str)

def crop_audio(args):
    print("Cropping audio...")
    
    src = args.file
    file_stem, _ = os.path.splitext(src)
    i = 0
    cropped_file = f"{file_stem}{i}_cut.wav"

    while path.exists(cropped_file):
        i += 1
        cropped_file = f"{file_stem}{i}.wav"

    shutil.copyfile(src, cropped_file)
    
    start_time = convert_time_to_seconds(args.musicstart) if args.musicstart else 0
    end_time = convert_time_to_seconds(args.musicend) if args.musicend else librosa.get_duration(filename=cropped_file)

    with wave.open(cropped_file, "rb") as infile:
        nchannels = infile.getnchannels()
        sampwidth = infile.getsampwidth()
        framerate = infile.getframerate()
        infile.setpos(int(start_time * framerate))
        data = infile.readframes(int((end_time - start_time) * framerate))

    with wave.open(cropped_file, 'w') as outfile:
        outfile.setnchannels(nchannels)
        outfile.setsampwidth(sampwidth)
        outfile.setframerate(framerate)
        outfile.writeframes(data)
    
    print(f"Your new cropped file is {int(end_time - start_time)} seconds long.")
    print(f"The name of your new cropped file is {cropped_file} and your original non-cropped file is {args.file}")
    
    return cropped_file

def generate_keyframes(args, cropped_file):
    print("Generating keyframes...")
    
    x, sr = librosa.load(cropped_file)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_times = librosa.frames_to_time(onset_frames)

    fps = args.fps
    duration = librosa.get_duration(filename=cropped_file)
    total_frames = int(duration * fps)
    vals, _ = np.histogram(onset_times, bins=total_frames, range=(0, duration))

    key_frame_value = []
    for i, val in enumerate(vals):
        if val > 0:
            key_frame_value.append(f"{i}:({args.speed}),")

    key_frame_string = "".join(key_frame_value)

    with open("audio_keyframes.json", "w") as fp:
        json.dump(key_frame_string, fp)

    print("Keyframes exported to audio_keyframes.json")

if __name__ == "__main__":
    args = parse_args()

    if args.music_cut:
        cropped_file = crop_audio(args)
    else:
        print("Audio not cropped.")
        cropped_file = args.file

    generate_keyframes(args, cropped_file)