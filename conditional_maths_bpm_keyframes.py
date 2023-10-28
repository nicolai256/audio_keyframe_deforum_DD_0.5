import argparse
import json
import librosa
import numpy as np
from scipy import fftpack
import os
import logging
import hashlib
from os import path
from joblib import Memory

# Initialize joblib memory cache
memory = Memory("cache_directory", verbose=0)

# Standard PI for performance-sensitive operations
PI = np.pi

def parse_arguments():
    parser = argparse.ArgumentParser(description='Feature Extraction From Audio Files')
    parser.add_argument('--file', type=str, required=True, help='Your audio file')
    parser.add_argument('--fps', type=int, required=True, help='Frames per second')
    parser.add_argument('--intensity', type=float, required=True, help='Intensity of the keyframe')
    parser.add_argument('--function_type', type=str, choices=['sine', 'cosine', 'abs_sin', 'abs_cos', 'modulus', 'linear', 'triangle', 'fourier'], default='sine', help='Type of function to generate')
    parser.add_argument('--advanced_params', type=str, default="", help='Advanced parameters as a string')
    parser.add_argument('--export-all-formulas', action='store_true', help='Export all formulas to JSON')
    
    args = parser.parse_args()
    
    args.advanced_params = {k: float(v) for k, v in (param.split("=") for param in args.advanced_params.split(","))} if args.advanced_params else {}

    if not path.exists(args.file) or args.fps <= 0 or args.intensity <= 0:
        logging.error(f"Invalid arguments.")
        exit(1)
    
    return args

@memory.cache
def fft_analysis(y):
    N = len(y)
    T = 1.0 / 800.0
    yf = fftpack.fft(y)
    return np.abs(yf[0:N//2])

def load_audio_file(filename):
    try:
        y, sr = librosa.load(filename, sr=None)
        
        # FFT for more precise frequency analysis
        fft_result = fft_analysis(y)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        
        if tempo <= 0:
            logging.error(f"Error: BPM detected as zero or negative.")
            exit(1)

        return float(tempo)  # Standard float for performance
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)

def calculate_expression(fps, tempo, intensity):
    x = float(fps) * 60 / tempo  # Standard float for performance
    return f'0:({intensity}*sin(2*{PI}*t/{x}))'

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as fp:
            json.dump(data, fp)
    except Exception as e:
        logging.error(f"An error occurred while saving to JSON: {e}")
        exit(1)

def generate_unique_filename(base_name, file_content, audio_filename):
    m = hashlib.sha256()
    m.update(file_content.encode('utf-8'))
    hash_value = m.hexdigest()[:10]
    audio_filename_without_extension = os.path.splitext(os.path.basename(audio_filename))[0]
    return f"{base_name}_{audio_filename_without_extension}_{hash_value}.json"

def generate_complex_expression(fps, tempo, intensity, function_type="sine", params={}):
    x = float(fps) * 60 / tempo
    A = params.get('A', 1)
    P = params.get('P', 1)
    D = params.get('D', 0)
    B = params.get('B', 1)
        
    if function_type == "sine":
        return f'0:(D+A*sin(23.14*t/P))'.replace('D', str(D)).replace('A', str(A)).replace('P', str(P))
    elif function_type == "cosine":
        return f'0:(D+A*cos(23.14*t/P))'.replace('D', str(D)).replace('A', str(A)).replace('P', str(P))
    elif function_type == "abs_sin":
        return f'0:(A-(abs(sin(10*t/P))*B))'.replace('A', str(A)).replace('P', str(P)).replace('B', str(B))
    elif function_type == "abs_cos":
        return f'0:(A-(abs(cos(10*t/P))*B))'.replace('A', str(A)).replace('P', str(P)).replace('B', str(B))
    elif function_type == "modulus":
        return f'0:(A*(t%P)+D)'.replace('A', str(A)).replace('P', str(P)).replace('D', str(D))
    elif function_type == "linear":
        return f'0:(A*t+D)'.replace('A', str(A)).replace('D', str(D))
    elif function_type == "triangle":
        return f'0:((2 + 2*A)/3.14*arcsin(sin((2*3.14)/P*t)))'.replace('A', str(A)).replace('P', str(P))
    elif function_type == "fourier":
        return f'0:(D + (A*(sin*t/P)+sin(A*t/P) + sin(A*t/P)))'.replace('D', str(D)).replace('A', str(A)).replace('P', str(P))
    else:
        return None
  
def generate_all_formulas(fps, tempo, intensity, params={}):
    all_formulas = {}
    for function_type in ['sine', 'cosine', 'abs_sin', 'abs_cos', 'modulus', 'linear', 'triangle', 'fourier']:
        formula = generate_complex_expression(fps, tempo, intensity, function_type, params)
        all_formulas[function_type] = formula
    return all_formulas
  
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    args = parse_arguments()
    
    tempo = load_audio_file(args.file)
    logging.info(f'BPM: {tempo:.5f}')
    
    expression = calculate_expression(args.fps, tempo, args.intensity)
    
    complex_params = {'A': 2, 'P': 3, 'D': 4}
    
    all_formulas = None
    if args.export_all_formulas:
        all_formulas = generate_all_formulas(args.fps, tempo, args.intensity, params=complex_params)

    complex_expression = generate_complex_expression(args.fps, tempo, args.intensity, function_type=args.function_type, params=complex_params)
    
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)
    json_filename = os.path.join(output_folder, generate_unique_filename("conditional_maths_bpm", expression, args.file))
    
    data = {
        "expression": expression,
        "complex_expression": complex_expression,
        "all_formulas": all_formulas     
    }
    
    save_to_json(data, json_filename)
    logging.info(f"Le traitement des images clés a réussi et a été exporté dans {json_filename}")