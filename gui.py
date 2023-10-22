import os
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, justify=tk.LEFT, background="#ffffff", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

class AdvancedAudioSplitterUI:
    def __init__(self, master):
        self.master = master
        self.master.title("AKD GUI")
        self.create_widgets()

    def create_widgets(self):
        # Create and place widgets similarly as before, but now they are encapsulated within this class method
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.audio_file_label = ttk.Label(self.frame, text="Audio File:")
        self.audio_file_label.grid(row=0, column=0, sticky=tk.W)

        self.audio_file_entry = ttk.Entry(self.frame, width=40)
        self.audio_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        self.audio_file_button = ttk.Button(self.frame, text="Browse", command=lambda: self.select_audio_file(self.audio_file_entry))
        self.audio_file_button.grid(row=0, column=2)

        ttk.Label(self.master, text="FPS:").grid(row=1, column=0)
        self.fps_entry = ttk.Entry(root)
        self.fps_entry.grid(row=1, column=1)

        # Widgets for Spleeter settings
        ttk.Label(root, text="Use Spleeter:").grid(row=2, column=0)
        self.spleeter_var = tk.IntVar()
        ttk.Checkbutton(root, variable=self.spleeter_var).grid(row=2, column=1)

        ttk.Label(root, text="Stems:").grid(row=3, column=0)
        self.stems_entry = ttk.Entry(root)
        self.stems_entry.grid(row=3, column=1)

        # Widgets for music start and end in minute, second format
        ttk.Label(root, text="Music Start (m,s):").grid(row=5, column=0)
        self.music_start_entry = ttk.Entry(root)
        self.music_start_entry.grid(row=5, column=1)

        ttk.Label(root, text="Music End (m,s):").grid(row=6, column=0)
        self.music_end_entry = ttk.Entry(root)
        self.music_end_entry.grid(row=6, column=1)

        # Widgets for speed and zoomspeed in simple scripts
        ttk.Label(root, text="Speed:").grid(row=24, column=0)
        self.speed_entry = ttk.Entry(root)
        self.speed_entry.grid(row=24, column=1)

        ttk.Label(root, text="Zoom Speed:").grid(row=25, column=0)
        self.zoom_speed_entry = ttk.Entry(root)
        self.zoom_speed_entry.grid(row=25, column=1)

        # Widget for use_vocals
        ttk.Label(root, text="Use Vocals:").grid(row=26, column=0)
        use_vocals_var = tk.IntVar()
        ttk.Checkbutton(root, variable=use_vocals_var).grid(row=26, column=1)

        ttk.Label(root, text="Zoom Sound:").grid(row=7, column=0)
        self.zoom_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
        self.zoom_sound_combo.grid(row=7, column=1)

        ttk.Label(root, text="Strength Sound:").grid(row=8, column=0)
        self.strength_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
        self.strength_sound_combo.grid(row=8, column=1)

        ttk.Label(root, text="Noise Sound:").grid(row=9, column=0)
        self.noise_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
        self.noise_sound_combo.grid(row=9, column=1)

        ttk.Label(root, text="Contrast Sound:").grid(row=10, column=0)
        self.contrast_sound_combo = ttk.Combobox(root, values=["drums", "other", "piano", "bass"])
        self.contrast_sound_combo.grid(row=10, column=1)

        # Widgets for keyframe impact settings
        ttk.Label(root, text="Drums Drop Speed:").grid(row=11, column=0)
        self.drums_drop_speed_entry = ttk.Entry(root)
        self.drums_drop_speed_entry.grid(row=11, column=1)

        ttk.Label(root, text="Drums Begin Speed:").grid(row=27, column=0)
        self.drums_begin_speed_entry = ttk.Entry(root)
        self.drums_begin_speed_entry.grid(row=27, column=1)

        # Widgets for non-Spleeter audio path settings
        ttk.Label(root, text="Drums Audio Path:").grid(row=15, column=0)
        self.drums_audio_path_entry = ttk.Entry(root)
        self.drums_audio_path_entry.grid(row=15, column=1)

        ttk.Label(root, text="Piano Audio Path:").grid(row=16, column=0)
        self.piano_audio_path_entry = ttk.Entry(root)
        self.piano_audio_path_entry.grid(row=16, column=1)

        ttk.Label(root, text="Bass Audio Path:").grid(row=17, column=0)
        self.bass_audio_path_entry = ttk.Entry(root)
        self.bass_audio_path_entry.grid(row=17, column=1)

        ttk.Label(root, text="Other Audio Path:").grid(row=18, column=0)
        self.other_audio_path_entry = ttk.Entry(root)
        self.other_audio_path_entry.grid(row=18, column=1)

        # Widgets for additional keyframe impact settings
        ttk.Label(root, text="Piano Drop Speed:").grid(row=19, column=0)
        self.piano_drop_speed_entry = ttk.Entry(root)
        self.piano_drop_speed_entry.grid(row=19, column=1)

        ttk.Label(root, text="Bass Drop Speed:").grid(row=20, column=0)
        self.bass_drop_speed_entry = ttk.Entry(root)
        self.bass_drop_speed_entry.grid(row=20, column=1)

        # Widgets for Conditional Maths BPM
        ttk.Label(root, text="BPM File:").grid(row=21, column=0)
        self.bpm_file_entry = ttk.Entry(root)
        self.bpm_file_entry.grid(row=21, column=1)

        ttk.Label(root, text="Intensity:").grid(row=22, column=0)
        self.intensity_entry = ttk.Entry(root)
        self.intensity_entry.grid(row=22, column=1)

        ToolTip(self.audio_file_entry, "Path to the audio file you want to process.")
        ToolTip(self.fps_entry, "Frames Per Second for the target animation.")
        ToolTip(self.stems_entry, "The number of audio stems to split the original audio into.")
        ToolTip(self.music_start_entry, "Start time for the audio in minute,second format.")
        ToolTip(self.music_end_entry, "End time for the audio in minute,second format.")
        ToolTip(self.speed_entry, "The amplitude/strength/intensity of your animation.")
        ToolTip(self.zoom_speed_entry, "Reactive zoom impact speed for the audio.")
        ToolTip(self.zoom_sound_combo, "Sound for zoom effect. Choose from 'drums', 'other', 'piano', 'bass'.")
        ToolTip(self.strength_sound_combo, "Sound for strength schedule. Recommended to be the same as zoom sound.")
        ToolTip(self.noise_sound_combo, "Sound for noise schedule. Recommended to be the same as zoom sound.")
        ToolTip(self.contrast_sound_combo, "Sound for contrast schedule. Recommended to be the same as zoom sound.")
        ToolTip(self.drums_drop_speed_entry, "Reactive impact of the drums audio on the animation when the audio makes a sound.")
        ToolTip(self.drums_begin_speed_entry, "Starting value on keyframe 1 for drums.")
        ToolTip(self.drums_audio_path_entry, "Path to your drums .wav file if not using Spleeter.")
        ToolTip(self.piano_audio_path_entry, "Path to your piano .wav file if not using Spleeter.")
        ToolTip(self.bass_audio_path_entry, "Path to your bass .wav file if not using Spleeter.")
        ToolTip(self.other_audio_path_entry, "Path to your other .wav file if not using Spleeter.")
        ToolTip(self.piano_drop_speed_entry, "Reactive impact of the piano audio on the animation when the audio makes a sound.")
        ToolTip(self.bass_drop_speed_entry, "Reactive impact of the bass audio on the animation when the audio makes a sound.")
        ToolTip(self.bpm_file_entry, "Path to the audio file for BPM calculations.")
        ToolTip(self.intensity_entry, "The amplitude/strength/intensity of your BPM-based animation.")

        self.fps_entry.insert(0, "30")
        self.stems_entry.insert(0, "5")
        self.music_start_entry.insert(0, "1,30")
        self.music_end_entry.insert(0, "3,20")
        self.speed_entry.insert(0, "1.5")
        self.zoom_speed_entry.insert(0, "0.8")
        self.drums_drop_speed_entry.insert(0, "0.3")
        self.drums_begin_speed_entry.insert(0, "0.1")
        self.piano_drop_speed_entry.insert(0, "0.25")
        self.bass_drop_speed_entry.insert(0, "0.4")
        self.intensity_entry.insert(0, "1.0")

        # Add Execute Button
        ttk.Button(self.master, text="Execute", command=self.execute_command).grid(row=23, columnspan=2)

    def select_audio_file(self, audio_file_entry):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if file_path:
            if not os.path.exists(file_path):
                print("Selected file does not exist. Please select a valid file.")
                return
            audio_file_entry.delete(0, tk.END)
            audio_file_entry.insert(0, file_path)

    def validate_input(self):
        # Validate user input here
        # Return True if validation succeeds, otherwise return False
        return True

    def execute_command(self):
        if not self.validate_input():
            print("Invalid input. Please correct.")
            return
        # Check if venv exists and is activated
        python_venv_path = "venv\\Scripts\\python.exe"  # For Windows
        if not os.path.exists(python_venv_path):
            print("Python virtual environment is not set up correctly. Please check.")
            return
            
        # Collect the options
        audio_file = self.audio_file_entry.get()
        # Check if the audio file path exists
        if not os.path.exists(audio_file):
            print("Specified audio file does not exist. Please select a valid file.")
            return

        fps = self.fps_entry.get()
        spleeter = self.spleeter_var.get()
        stems = self.stems_entry.get()
        music_start = self.music_start_entry.get()
        music_end = self.music_end_entry.get()
        zoom_sound = self.zoom_sound_combo.get()
        strength_sound = self.strength_sound_combo.get()
        noise_sound = self.noise_sound_combo.get()
        contrast_sound = self.contrast_sound_combo.get()
        drums_drop_speed = self.drums_drop_speed_entry.get()
        drums_audio_path = self.drums_audio_path_entry.get()

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

if __name__ == "__main__":
    root = ThemedTk()
    root.set_theme("arc")
    root.iconbitmap('./favicon.ico')     
    app = AdvancedAudioSplitterUI(root)
    root.mainloop()