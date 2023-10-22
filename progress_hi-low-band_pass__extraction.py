import argparse
import csv
import os
from scipy import signal
import librosa
import numpy as np

def apply_filter(audio_data, sr, low_freq, high_freq=None, filter_type='low'):
    """Applique un filtre audio en fonction des fréquences et du type de filtre donnés."""
    b, a = signal.butter(5, low_freq / (sr / 2), filter_type)
    filtered_data = signal.filtfilt(b, a, audio_data)
    if high_freq:
        b, a = signal.butter(5, high_freq / (sr / 2), 'high')
        filtered_data = signal.filtfilt(b, a, filtered_data)
    return filtered_data

def read_bpm_from_csv(filename):
    """Lit le BPM depuis un fichier CSV."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found.")
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return float(row['tempo'])

def compute_rmse_and_save(audio_data, sr, frame_length, out_file):
    """Calcule le RMS de l'audio et sauvegarde le résultat."""
    y_rmse = librosa.feature.rms(audio_data, frame_length=int(frame_length), hop_length=int(frame_length), center=True)[0,:]
    np.save(out_file, y_rmse)

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description='Feature Extraction From MP3')
    parser.add_argument('--path', type=str, help='Path to the audio file')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        raise FileNotFoundError(f"{args.path} not found.")
        
    out_dir = "./features/"
    os.makedirs(out_dir, exist_ok=True)

    bpm = read_bpm_from_csv('names.csv')
    y, sr = librosa.load(args.path)
    
    # Calcul du cadre temporel pour le découpage de l'audio
    set_frame_track = 1 / (bpm * 16 / 60)
    frame_length = sr * set_frame_track

    # Configuration des différents filtres à appliquer
    filter_configs = [
        {'name': 'lpf', 'low_freq': 150},
        {'name': 'bpf', 'low_freq': 200, 'high_freq': 350},
        {'name': 'hpf', 'low_freq': 500, 'high_freq': 5000}
    ]

    for config in filter_configs:
        filtered_y = apply_filter(y, sr, config['low_freq'], config.get('high_freq'), 'low' if 'hpf' not in config['name'] else 'high')
        out_wav = f"{out_dir}{config['name']}_y.wav"
        out_npy = f"{out_dir}{config['name']}_y_rmse.npy"

        # Sauvegarde de l'audio filtré
        librosa.output.write_wav(out_wav, filtered_y, sr)
        
        # Recharge l'audio pour garantir que les données sont filtrées
        filtered_y, _ = librosa.load(out_wav)
        
        # Calcul et sauvegarde du RMS
        compute_rmse_and_save(filtered_y, sr, frame_length, out_npy)

if __name__ == '__main__':
    main()