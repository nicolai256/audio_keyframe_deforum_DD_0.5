import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess

def select_audio_file(audio_file_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
    if file_path:
        if not os.path.exists(file_path):
            print("Selected file does not exist. Please select a valid file.")
            return
        audio_file_entry.delete(0, tk.END)
        audio_file_entry.insert(0, file_path)

def execute_command():
    # Check if venv exists and is activated
    python_venv_path = "venv\\Scripts\\python.exe"  # For Windows
    if not os.path.exists(python_venv_path):
        print("Python virtual environment is not set up correctly. Please check.")
        return
        
    # Collect the options
    audio_file = audio_file_entry.get()
    # Check if the audio file path exists
    if not os.path.exists(audio_file):
        print("Specified audio file does not exist. Please select a valid file.")
        return

    fps = fps_entry.get()
    spleeter = spleeter_var.get()
    stems = stems_entry.get()
    music_start = music_start_entry.get()
    music_end = music_end_entry.get()
    zoom_sound = zoom_sound_combo.get()
    strength_sound = strength_sound_combo.get()
    noise_sound = noise_sound_combo.get()
    contrast_sound = contrast_sound_combo.get()
    drums_drop_speed = drums_drop_speed_entry.get()
    drums_audio_path = drums_audio_path_entry.get()

    # Initialize the command list with the python path and script name
    cmd = [python_venv_path if os.path.exists(python_venv_path) else "python", "advanced_audio_splitter_keyframes.py"]

    # Append arguments conditionally
    if audio_file:
        cmd.extend(["-f", audio_file])
    if fps:
        cmd.extend(["--fps", fps])
    if spleeter is not None:
        cmd.extend(["--spleeter", str(spleeter)])
    if stems:
        cmd.extend(["--stems", stems])
    if music_start:
        cmd.extend(["--musicstart", music_start])
    if music_end:
        cmd.extend(["--musicend", music_end])
    if zoom_sound:
        cmd.extend(["--zoom_sound", zoom_sound])
    if strength_sound:
        cmd.extend(["--strength_sound", strength_sound])
    if noise_sound:
        cmd.extend(["--noise_sound", noise_sound])
    if contrast_sound:
        cmd.extend(["--contrast_sound", contrast_sound])
    if drums_drop_speed:
        cmd.extend(["--drums_drop_speed", drums_drop_speed])
    if drums_audio_path:
        cmd.extend(["--drums_audio_path", drums_audio_path])

    # Execute the command and capture output
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if the process has completed successfully
    if process.returncode != 0:
        print(f"An error occurred: {process.stderr.decode('utf-8', errors='replace')}")
    else:
        print(f"Success: {process.stdout.decode('utf-8')}")

# Initialize Tkinter window
root = tk.Tk()
root.title("AKD GUI")

# Widgets for general settings
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

audio_file_label = ttk.Label(frame, text="Audio File:")
audio_file_label.grid(row=0, column=0, sticky=tk.W)

audio_file_entry = ttk.Entry(frame, width=40)
audio_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

audio_file_button = ttk.Button(frame, text="Browse", command=lambda: select_audio_file(audio_file_entry))
audio_file_button.grid(row=0, column=2)

ttk.Label(root, text="FPS:").grid(row=1, column=0)
fps_entry = ttk.Entry(root)
fps_entry.grid(row=1, column=1)

# Widgets for Spleeter settings
ttk.Label(root, text="Use Spleeter:").grid(row=2, column=0)
spleeter_var = tk.IntVar()
ttk.Checkbutton(root, variable=spleeter_var).grid(row=2, column=1)

ttk.Label(root, text="Stems:").grid(row=3, column=0)
stems_entry = ttk.Entry(root)
stems_entry.grid(row=3, column=1)

# Widgets for music start and end in minute, second format
ttk.Label(root, text="Music Start (m,s):").grid(row=5, column=0)
music_start_entry = ttk.Entry(root)
music_start_entry.grid(row=5, column=1)

ttk.Label(root, text="Music End (m,s):").grid(row=6, column=0)
music_end_entry = ttk.Entry(root)
music_end_entry.grid(row=6, column=1)

# Widgets for speed and zoomspeed in simple scripts
ttk.Label(root, text="Speed:").grid(row=24, column=0)
speed_entry = ttk.Entry(root)
speed_entry.grid(row=24, column=1)

ttk.Label(root, text="Zoom Speed:").grid(row=25, column=0)
zoom_speed_entry = ttk.Entry(root)
zoom_speed_entry.grid(row=25, column=1)

# Widget for use_vocals
ttk.Label(root, text="Use Vocals:").grid(row=26, column=0)
use_vocals_var = tk.IntVar()
ttk.Checkbutton(root, variable=use_vocals_var).grid(row=26, column=1)

ttk.Label(root, text="Zoom Sound:").grid(row=7, column=0)
zoom_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
zoom_sound_combo.grid(row=7, column=1)

ttk.Label(root, text="Strength Sound:").grid(row=8, column=0)
strength_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
strength_sound_combo.grid(row=8, column=1)

ttk.Label(root, text="Noise Sound:").grid(row=9, column=0)
noise_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
noise_sound_combo.grid(row=9, column=1)

ttk.Label(root, text="Contrast Sound:").grid(row=10, column=0)
contrast_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
contrast_sound_combo.grid(row=10, column=1)

# Widgets for keyframe impact settings
ttk.Label(root, text="Drums Drop Speed:").grid(row=11, column=0)
drums_drop_speed_entry = ttk.Entry(root)
drums_drop_speed_entry.grid(row=11, column=1)

ttk.Label(root, text="Drums Begin Speed:").grid(row=27, column=0)
drums_begin_speed_entry = ttk.Entry(root)
drums_begin_speed_entry.grid(row=27, column=1)

# Widgets for non-Spleeter audio path settings
ttk.Label(root, text="Drums Audio Path:").grid(row=15, column=0)
drums_audio_path_entry = ttk.Entry(root)
drums_audio_path_entry.grid(row=15, column=1)

ttk.Label(root, text="Piano Audio Path:").grid(row=16, column=0)
piano_audio_path_entry = ttk.Entry(root)
piano_audio_path_entry.grid(row=16, column=1)

ttk.Label(root, text="Bass Audio Path:").grid(row=17, column=0)
bass_audio_path_entry = ttk.Entry(root)
bass_audio_path_entry.grid(row=17, column=1)

ttk.Label(root, text="Other Audio Path:").grid(row=18, column=0)
other_audio_path_entry = ttk.Entry(root)
other_audio_path_entry.grid(row=18, column=1)

# Widgets for additional keyframe impact settings
ttk.Label(root, text="Piano Drop Speed:").grid(row=19, column=0)
piano_drop_speed_entry = ttk.Entry(root)
piano_drop_speed_entry.grid(row=19, column=1)

ttk.Label(root, text="Bass Drop Speed:").grid(row=20, column=0)
bass_drop_speed_entry = ttk.Entry(root)
bass_drop_speed_entry.grid(row=20, column=1)

# Widgets for Conditional Maths BPM
ttk.Label(root, text="BPM File:").grid(row=21, column=0)
bpm_file_entry = ttk.Entry(root)
bpm_file_entry.grid(row=21, column=1)

ttk.Label(root, text="Intensity:").grid(row=22, column=0)
intensity_entry = ttk.Entry(root)
intensity_entry.grid(row=22, column=1)

# Add Execute Button
ttk.Button(root, text="Execute", command=execute_command).grid(row=23, columnspan=2)

# Run the Tkinter event loop
root.mainloop()
