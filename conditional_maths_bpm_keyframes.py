import argparse
import json
import librosa
import numpy as np
import os
import logging
import hashlib
from os import path
import mpmath

# Use mpmath for high-precision PI constant
PI = mpmath.pi

def parse_arguments():
    parser = argparse.ArgumentParser(description='Feature Extraction From Audio Files')
    parser.add_argument('--file', type=str, required=True, help='Your audio file')
    parser.add_argument('--fps', type=int, required=True, help='Frames per second')
    parser.add_argument('--intensity', type=float, required=True, help='Intensity of the keyframe')
    args = parser.parse_args()
    
    if not path.exists(args.file) or args.fps <= 0 or args.intensity <= 0:
        logging.error(f"Invalid arguments.")
        exit(1)
    
    return args

def load_audio_file(filename):
    try:
        y, sr = librosa.load(filename, sr=None)
        
        # Advanced tempo detection with Harmonic Resonance Analysis
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        
        if tempo <= 0:
            logging.error(f"Error: BPM detected as zero or negative.")
            exit(1)
        
        # Use mpmath for high-precision calculations
        return mpmath.mpf(tempo)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)

def calculate_expression(fps, tempo, intensity):
    # Use mpmath for high-precision calculations
    x = mpmath.mpf(fps) * 60 / tempo
    return f'0:({intensity}*sin(2*{PI}*t/{x}))'

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as fp:
            json.dump(data, fp)
    except Exception as e:
        logging.error(f"An error occurred while saving to JSON: {e}")
        exit(1)

def generate_unique_filename(base_name, file_content):
    m = hashlib.sha256()
    m.update(file_content.encode('utf-8'))
    hash_value = m.hexdigest()[:10]
    return f"{base_name}_{hash_value}.json"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    args = parse_arguments()
    
    tempo = load_audio_file(args.file)
    logging.info(f'BPM: {mpmath.nstr(tempo, 50)}')  # Display tempo with 50 decimal places
    
    expression = calculate_expression(args.fps, tempo, args.intensity)
    
    json_filename = generate_unique_filename("conditional_maths_bpm", expression)
    
    save_to_json(expression, json_filename)
    logging.info(f"Processing of the keyframes succeeded and exported to {json_filename}")