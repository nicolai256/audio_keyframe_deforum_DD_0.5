import os
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import threading
import sys
import io
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

logging.info("Starting program...")

class TextRedirector(io.StringIO):
    def __init__(self, widget):
        self.widget = widget
        
    def write(self, str):
        self.widget.after(0, self._write, str)

    def _write(self, str):
        try:
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, str)
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)
        except tk.TclError as e:
            logging.error(f"Error in TextRedirector: {e}")

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
        logging.info("Initializing UI...")
        self.master = master
        self.master.title("AKD GUI")
        self.master.geometry('512x906')        
        try:
            self.create_widgets()
        except Exception as e:
            logging.critical(f"Failed to initialize UI: {e}")
            print(f"Failed to initialize UI: {e}")
            raise
            
    def create_widgets(self):
        # Create main frame
        self.frame = ttk.Frame(self.master, padding="1")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Create sub-frames for each group of widgets
        self.audio_frame = self.create_labeled_frame("Audio Settings", row=0, col=0)
        self.spleeter_frame = self.create_labeled_frame("Spleeter Settings", row=1, col=0)
        self.script_frame = self.create_labeled_frame("Script Settings", row=2, col=0)
        self.advanced_frame = self.create_labeled_frame("Advanced Settings", row=3, col=0)
        
        # Create Widgets for Each Frame
        self.create_audio_widgets(self.audio_frame)
        self.create_spleeter_widgets(self.spleeter_frame)
        self.create_advanced_widgets(self.advanced_frame)

        # Adding a Text widget to serve as a console
        self.console = tk.Text(self.master, wrap=tk.WORD, height=6, width=50)

        self.console.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=1)  # Changé row de 4 à 1
        self.console.config(state=tk.DISABLED)
        
        # Redirect stdout and stderr
        sys.stdout = TextRedirector(self.console)
        sys.stderr = TextRedirector(self.console)   

        ToolTip(self.audio_file_entry, "Path to the audio file you want to process.")
        ToolTip(self.fps_entry, "Frames Per Second for the target animation.")
        ToolTip(self.stems_entry, "The number of audio stems to split the original audio into.")
        ToolTip(self.music_start_entry, "Start time for the audio in minute,second format.")
        ToolTip(self.music_end_entry, "End time for the audio in minute,second format.")
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
        ToolTip(self.piano_begin_speed_entry, "Starting value on keyframe 1 for piano.")
        ToolTip(self.piano_predrop_speed_entry, "Value just before a drop for piano.")
        ToolTip(self.strength_drop_speed_entry, "Reactive impact of the strength schedule when the audio makes a sound.")
        # ToolTip(self.noise_drop_speed_entry, "Reactive impact of the noise schedule when the audio makes a sound.")
        # ToolTip(self.contrast_drop_speed_entry, "Reactive impact of the contrast schedule when the audio makes a sound.")
        ToolTip(self.zoom_drop_speed_entry, "Reactive zoom drop speed for the audio.")
        ToolTip(self.music_cut_entry, "Cut in X splits")
        ToolTip(self.drums_predrop_speed_entry, "Pre-drop value for the impact of drums.")
        ToolTip(self.bass_begin_speed_entry, "Starting value on keyframe 1 for bass.")
        ToolTip(self.bass_predrop_speed_entry, "Value just before a drop for bass.")
        ToolTip(self.speed_entry, "The amplitude / strength / intensity of your animation.")
        ToolTip(self.zoom_speed_entry, "The amplitude / strength / intensity of your animation.")
        # ToolTip(self.zoom_predrop_speed_entry, "Reactive zoom impact of the audio on the animation right before the audio makes a sound.")
        ToolTip(self.zoom_drop_speed_entry, "Reactive zoom impact of the audio on the animation when the audio makes a sound.")
       
        self.fps_entry.insert(0, "30")
        self.speed_entry.insert(0, "4")
        self.zoom_speed_entry.insert(0, "4")
        self.stems_entry.insert(0, "4")
        self.zoom_drop_speed_entry.insert(0, "5")        
        self.strength_drop_speed_entry.insert(0, "0.50")
        self.drums_drop_speed_entry.insert(0, "0.2")
        self.drums_predrop_speed_entry.insert(0, "-0.2")
        self.drums_begin_speed_entry.insert(0, "0.0")
        self.piano_predrop_speed_entry.insert(0, "-0.4")
        self.piano_drop_speed_entry.insert(0, "0.25")
        self.piano_begin_speed_entry.insert(0, "0.0")
        self.bass_predrop_speed_entry.insert(0, "-0.4")
        self.bass_drop_speed_entry.insert(0, "0.4")
        self.bass_begin_speed_entry.insert(0, "0.0")

        self.execute_button = ttk.Button(self.master, text="Execute", command=self.execute_command_threaded)
        self.execute_button.grid(row=0, column=3, sticky=(tk.E), pady=1, padx=1)

    def create_labeled_frame(self, label, row, col):
        frame = ttk.LabelFrame(self.frame, text=label, padding="1")
        frame.grid(row=row, column=col, sticky=(tk.W, tk.E), pady=1, padx=1)
        return frame

    def add_file_chooser(self, frame, label, row, col):
        ttk.Label(frame, text=label).grid(row=row, column=col, sticky=(tk.W))
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=col + 1, sticky=(tk.W))
        ttk.Button(frame, text="Browse", command=lambda: self.select_file(entry)).grid(row=row, column=col + 2, sticky=(tk.W))

    def select_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
            
    def create_audio_widgets(self, frame):
        ttk.Label(frame, text="Audio File:").grid(row=0, column=0, sticky=(tk.W))
        self.audio_file_entry = ttk.Entry(frame)
        self.audio_file_entry.grid(row=0, column=1, sticky=(tk.W))
        ttk.Button(frame, text="Browse", command=lambda: self.select_audio_file(self.audio_file_entry)).grid(row=0, column=2, sticky=(tk.W))

        ttk.Label(frame, text="FPS:").grid(row=1, column=0, sticky=(tk.W))
        self.fps_entry = ttk.Entry(frame)
        self.fps_entry.grid(row=1, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Speed:").grid(row=2, column=0, sticky=(tk.W))
        self.speed_entry = ttk.Entry(frame)
        self.speed_entry.grid(row=2, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Zoom Speed:").grid(row=3, column=0, sticky=(tk.W))
        self.zoom_speed_entry = ttk.Entry(frame)
        self.zoom_speed_entry.grid(row=3, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Use Spleeter:").grid(row=4, column=0, sticky=(tk.W))
        self.spleeter_var = tk.IntVar(value=1)  # Initialize to 1 to make it checked
        ttk.Checkbutton(frame, variable=self.spleeter_var).grid(row=4, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Drums Audio Path:").grid(row=5, column=0, sticky=(tk.W))
        self.drums_audio_path_entry = ttk.Entry(frame)
        self.drums_audio_path_entry.grid(row=5, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Piano Audio Path:").grid(row=6, column=0, sticky=(tk.W))
        self.piano_audio_path_entry = ttk.Entry(frame)
        self.piano_audio_path_entry.grid(row=6, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Bass Audio Path:").grid(row=7, column=0, sticky=(tk.W))
        self.bass_audio_path_entry = ttk.Entry(frame)
        self.bass_audio_path_entry.grid(row=7, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Other Audio Path:").grid(row=8, column=0, sticky=(tk.W))
        self.other_audio_path_entry = ttk.Entry(frame)
        self.other_audio_path_entry.grid(row=8, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="BPM File:").grid(row=9, column=0, sticky=(tk.W))
        self.bpm_file_entry = ttk.Entry(frame)
        self.bpm_file_entry.grid(row=9, column=1, sticky=(tk.W))       
        
        self.add_file_chooser(frame, "Drums Audio Path:", 5, 0)
        self.add_file_chooser(frame, "Piano Audio Path:", 6, 0)
        self.add_file_chooser(frame, "Bass Audio Path:", 7, 0)
        self.add_file_chooser(frame, "Other Audio Path:", 8, 0)
        self.add_file_chooser(frame, "BPM File:", 9, 0)
        
    def create_spleeter_widgets(self, frame):

        ttk.Label(self.audio_frame, text="Music Cut:").grid(row=11, column=0, sticky=(tk.W))
        self.music_cut_entry = ttk.Entry(self.audio_frame)
        self.music_cut_entry.grid(row=11, column=1, sticky=(tk.W))

        ttk.Label(self.audio_frame, text="Music Start:").grid(row=12, column=0, sticky=(tk.W))
        self.music_start_entry = ttk.Entry(self.audio_frame)
        self.music_start_entry.grid(row=12, column=1, sticky=(tk.W))

        ttk.Label(self.audio_frame, text="Music End:").grid(row=13, column=0, sticky=(tk.W))
        self.music_end_entry = ttk.Entry(self.audio_frame)
        self.music_end_entry.grid(row=13, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Stems:").grid(row=1, column=0, sticky=(tk.W))
        self.stems_entry = ttk.Entry(frame)
        self.stems_entry.grid(row=1, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Zoom Sound:").grid(row=2, column=0, sticky=(tk.W))
        self.zoom_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.zoom_sound_combo.grid(row=2, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Strength Sound:").grid(row=3, column=0, sticky=(tk.W))
        self.strength_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.strength_sound_combo.grid(row=3, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Noise Sound:").grid(row=4, column=0, sticky=(tk.W))
        self.noise_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.noise_sound_combo.grid(row=4, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Contrast Sound:").grid(row=5, column=0, sticky=(tk.W))
        self.contrast_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.contrast_sound_combo.grid(row=5, column=1, sticky=(tk.W))

    def create_advanced_widgets(self, frame):
       
        ttk.Label(frame, text="Zoom Drop Speed:").grid(row=2, column=0, sticky=(tk.W))
        self.zoom_drop_speed_entry = ttk.Entry(frame)
        self.zoom_drop_speed_entry.grid(row=2, column=1, sticky=(tk.W))
         
        # ttk.Label(frame, text="Zoom Pre-Drop Speed:").grid(row=3, column=0, sticky=(tk.W))
        # self.zoom_drop_speed_entry = ttk.Entry(frame)
        # self.zoom_drop_speed_entry.grid(row=3, column=1, sticky=(tk.W))
  
        ttk.Label(frame, text="Strength Drop Speed:").grid(row=12, column=0, sticky=(tk.W))
        self.strength_drop_speed_entry = ttk.Entry(frame)
        self.strength_drop_speed_entry.grid(row=12, column=1, sticky=(tk.W))
            
        ttk.Label(frame, text="Drums Drop Speed:").grid(row=0, column=0, sticky=(tk.W))
        self.drums_drop_speed_entry = ttk.Entry(frame)
        self.drums_drop_speed_entry.grid(row=0, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Drums Pre-drop Speed:").grid(row=4, column=0, sticky=(tk.W))
        self.drums_predrop_speed_entry = ttk.Entry(frame)
        self.drums_predrop_speed_entry.grid(row=4, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Drums Begin Speed:").grid(row=1, column=0, sticky=(tk.W))
        self.drums_begin_speed_entry = ttk.Entry(frame)
        self.drums_begin_speed_entry.grid(row=1, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Piano Drop Speed:").grid(row=5, column=0, sticky=(tk.W))
        self.piano_drop_speed_entry = ttk.Entry(frame)
        self.piano_drop_speed_entry.grid(row=5, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Piano Begin Speed:").grid(row=7, column=0, sticky=(tk.W))
        self.piano_begin_speed_entry = ttk.Entry(frame)
        self.piano_begin_speed_entry.grid(row=7, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Piano Pre-drop Speed:").grid(row=8, column=0, sticky=(tk.W))
        self.piano_predrop_speed_entry = ttk.Entry(frame)
        self.piano_predrop_speed_entry.grid(row=8, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Bass Drop Speed:").grid(row=6, column=0, sticky=(tk.W))
        self.bass_drop_speed_entry = ttk.Entry(frame)
        self.bass_drop_speed_entry.grid(row=6, column=1, sticky=(tk.W))
            
        # ttk.Label(frame, text="Noise Drop Speed:").grid(row=13, column=0, sticky=(tk.W))
        # self.noise_drop_speed_entry = ttk.Entry(frame)
        # self.noise_drop_speed_entry.grid(row=13, column=1, sticky=(tk.W))

        # ttk.Label(frame, text="Contrast Drop Speed:").grid(row=14, column=0, sticky=(tk.W))
        # self.contrast_drop_speed_entry = ttk.Entry(frame)
        # self.contrast_drop_speed_entry.grid(row=14, column=1, sticky=(tk.W))
 
        # ttk.Label(frame, text="Other Begin Speed:").grid(row=15, column=0, sticky=(tk.W))
        # self.other_begin_speed_entry = ttk.Entry(frame)
        # self.other_begin_speed_entry.grid(row=15, column=1, sticky=(tk.W))

        # ttk.Label(frame, text="Other Pre-drop Speed:").grid(row=16, column=0, sticky=(tk.W))
        # self.other_predrop_speed_entry = ttk.Entry(frame)
        # self.other_predrop_speed_entry.grid(row=16, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Bass Begin Speed:").grid(row=17, column=0, sticky=(tk.W))
        self.bass_begin_speed_entry = ttk.Entry(frame)
        self.bass_begin_speed_entry.grid(row=17, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Bass Pre-drop Speed:").grid(row=18, column=0, sticky=(tk.W))
        self.bass_predrop_speed_entry = ttk.Entry(frame)
        self.bass_predrop_speed_entry.grid(row=18, column=1, sticky=(tk.W))
            
        # ttk.Label(frame, text="Zoom Begin Speed:").grid(row=18, column=0, sticky=(tk.W))
        # self.zoom_begin_speed_entry = ttk.Entry(frame)
        # self.zoom_begin_speed_entry.grid(row=18, column=1, sticky=(tk.W))

        # ttk.Label(frame, text="Zoom Pre-drop Speed:").grid(row=20, column=0, sticky=(tk.W))
        # self.zoom_predrop_speed_entry = ttk.Entry(frame)
        # self.zoom_predrop_speed_entry.grid(row=20, column=1, sticky=(tk.W))

        # ttk.Label(frame, text="Noise Begin Speed:").grid(row=21, column=0, sticky=(tk.W))
        # self.noise_begin_speed_entry = ttk.Entry(frame)
        # self.noise_begin_speed_entry.grid(row=21, column=1, sticky=(tk.W))
        
        # ttk.Label(frame, text="Noise Pre-drop Speed:").grid(row=22, column=0, sticky=(tk.W))
        # self.noise_predrop_speed_entry = ttk.Entry(frame)
        # self.noise_predrop_speed_entry.grid(row=22, column=1, sticky=(tk.W))
        
        # ttk.Label(frame, text="Contrast Begin Speed:").grid(row=23, column=0, sticky=(tk.W))
        # self.contrast_begin_speed_entry = ttk.Entry(frame)
        # self.contrast_begin_speed_entry.grid(row=23, column=1, sticky=(tk.W))
            
        # ttk.Label(frame, text="Contrast Pre-drop Speed:").grid(row=24, column=0, sticky=(tk.W))
        # self.contrast_predrop_speed_entry = ttk.Entry(frame)
        # self.contrast_predrop_speed_entry.grid(row=24, column=1, sticky=(tk.W))
            
        # ttk.Label(frame, text="Strength Begin Speed:").grid(row=25, column=0, sticky=(tk.W))
        # self.strength_begin_speed_entry = ttk.Entry(frame)
        # self.strength_begin_speed_entry.grid(row=25, column=1, sticky=(tk.W))
            
        # ttk.Label(frame, text="Strength Pre-drop Speed:").grid(row=26, column=0, sticky=(tk.W))
        # self.strength_predrop_speed_entry = ttk.Entry(frame)
        # self.strength_predrop_speed_entry.grid(row=26, column=1, sticky=(tk.W))

    def select_audio_file(self, audio_file_entry):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if file_path:
            if not os.path.exists(file_path):
                print("Selected file does not exist. Please select a valid file.")
                return
            audio_file_entry.delete(0, tk.END)
            audio_file_entry.insert(0, file_path)

    def validate_input(self):
        files = [self.audio_file_entry.get(), self.drums_audio_path_entry.get(), self.piano_audio_path_entry.get()]
        for f in files:
            if f and not os.path.exists(f):
                self.show_error(f"File {f} does not exist.")
                return False
        if not self.fps_entry.get().isdigit():
            self.show_error("FPS must be a number.")
            return False
        # ... more validations ...
        return True

    def execute_command_threaded(self):
        try:
            thread = threading.Thread(target=self.execute_command)
            thread.daemon = True
            thread.start()
        except Exception as e:
            logger.critical(f"Failed to start thread: {e}")
            print(f"Failed to start thread: {e}")

    def execute_command(self):
        try:
            if not self.validate_input():
                logger.warning("Invalid input. Please correct.")
                print("Invalid input. Please correct.")
                return

            # Check if venv exists and is activated
            python_venv_path = "venv\\Scripts\\python.exe"  # For Windows
            if not os.path.exists(python_venv_path):
                logging.error("Python virtual environment is not set up correctly. Please check.")
                return

            # Collect the options
            audio_file = self.audio_file_entry.get()
            # Check if the audio file path exists
            if not os.path.exists(audio_file):
                logging.error("Specified audio file does not exist. Please select a valid file.")
                return

            fps = self.fps_entry.get()
            spleeter = self.spleeter_var.get()
            music_cut = self.music_cut_entry.get()
            music_start = self.music_start_entry.get()
            music_end = self.music_end_entry.get()
            stems = self.stems_entry.get()
            zoom_sound = self.zoom_sound_combo.get()
            strength_sound = self.strength_sound_combo.get()
            noise_sound = self.noise_sound_combo.get()
            contrast_sound = self.contrast_sound_combo.get()
            # contrast_drop_speed = self.contrast_drop_speed_entry.get()
            drums_drop_speed = self.drums_drop_speed_entry.get()
            drums_predrop_speed = self.drums_predrop_speed_entry.get()
            # zoom_predrop_speed = self.zoom_predrop_speed_entry.get()
            drums_audio_path = self.drums_audio_path_entry.get()
            bass_begin_speed_entry = self.bass_begin_speed_entry.get()
            zoom_drop_speed = self.zoom_drop_speed_entry.get()
            strength_drop_speed = self.strength_drop_speed_entry.get()
            # noise_drop_speed = self.noise_drop_speed_entry.get()
            piano_drop_speed = self.piano_drop_speed_entry.get()
            
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
            if music_cut:
                cmd.extend(["--music_cut", music_cut])                
            if music_start:
                cmd.extend(["--musicstart", music_start])
            if music_end:
                cmd.extend(["--musicend", music_end])
            if self.drums_drop_speed_entry.get():
                cmd.extend(["--drums_drop_speed", self.drums_drop_speed_entry.get()])
            
            if self.zoom_sound_combo.get():
                cmd.extend(["--zoom_sound", self.zoom_sound_combo.get()])

            if self.strength_sound_combo.get():
                cmd.extend(["--strength_sound", self.strength_sound_combo.get()])

            if self.noise_sound_combo.get():
                cmd.extend(["--noise_sound", self.noise_sound_combo.get()])

            if self.contrast_sound_combo.get():
                cmd.extend(["--contrast_sound", self.contrast_sound_combo.get()])

            if self.drums_audio_path_entry.get():
                cmd.extend(["--drums_audio_path", self.drums_audio_path_entry.get()])
            
            if self.other_audio_path_entry.get():
                cmd.extend(["--other_audio_path", self.other_audio_path_entry.get()])

            if self.piano_audio_path_entry.get():
                cmd.extend(["--piano_audio_path", self.piano_audio_path_entry.get()])
            
            if self.bass_audio_path_entry.get():
                cmd.extend(["--bass_audio_path", self.bass_audio_path_entry.get()])
                
            if self.music_cut_entry.get():
                cmd.extend(["--music_cut", self.music_cut_entry.get()])
            if self.music_start_entry.get():
                cmd.extend(["--musicstart", self.music_start_entry.get()])
            if self.music_end_entry.get():
                cmd.extend(["--musicend", self.music_end_entry.get()])
            if self.zoom_drop_speed_entry.get():
                cmd.extend(["--zoom_drop_speed", self.zoom_drop_speed_entry.get()])
            if self.strength_drop_speed_entry.get():
                cmd.extend(["--strength_drop_speed", self.strength_drop_speed_entry.get()])
            if zoom_drop_speed:
                cmd.extend(["--zoom_drop_speed", zoom_drop_speed])            
            if strength_drop_speed:
                cmd.extend(["--strength_drop_speed", strength_drop_speed])               
            # if noise_drop_speed:
                # cmd.extend(["--noise_drop_speed", noise_drop_speed])           
            # if contrast_drop_speed:
                # cmd.extend(["--contrast_drop_speed", contrast_drop_speed])          
            if piano_drop_speed:
                cmd.extend(["--piano_drop_speed", piano_drop_speed])          
            if self.drums_begin_speed_entry.get():
                cmd.extend(["--drums_begin_speed", self.drums_begin_speed_entry.get()])
            if self.drums_predrop_speed_entry.get():
                cmd.extend(["--drums_predrop_speed", self.drums_predrop_speed_entry.get()])
            # if self.other_begin_speed_entry.get():
                # cmd.extend(["--other_begin_speed", self.other_begin_speed_entry.get()])
            # if self.other_predrop_speed_entry.get():
                # cmd.extend(["--other_predrop_speed", self.other_predrop_speed_entry.get()])
            if self.piano_begin_speed_entry.get():
                cmd.extend(["--piano_begin_speed", self.piano_begin_speed_entry.get()])
            if self.piano_predrop_speed_entry.get():
                cmd.extend(["--piano_predrop_speed", self.piano_predrop_speed_entry.get()])
            if self.bass_begin_speed_entry.get():
                cmd.extend(["--bass_begin_speed", self.bass_begin_speed_entry.get()])
            if self.bass_predrop_speed_entry.get():
                cmd.extend(["--bass_predrop_speed", self.bass_predrop_speed_entry.get()])
            # if self.zoom_begin_speed_entry.get():
                # cmd.extend(["--zoom_begin_speed", self.zoom_begin_speed_entry.get()])
            # if self.zoom_predrop_speed_entry.get():
                # cmd.extend(["--zoom_predrop_speed", self.zoom_predrop_speed_entry.get()])
            # if self.noise_begin_speed_entry.get():
                # cmd.extend(["--noise_begin_speed", self.noise_begin_speed_entry.get()])
            # if self.noise_predrop_speed_entry.get():
                # cmd.extend(["--noise_predrop_speed", self.noise_predrop_speed_entry.get()])
            # if self.contrast_begin_speed_entry.get():
                # cmd.extend(["--contrast_begin_speed", self.contrast_begin_speed_entry.get()])
            # if self.contrast_predrop_speed_entry.get():
                # cmd.extend(["--contrast_predrop_speed", self.contrast_predrop_speed_entry.get()])
            # if self.strength_begin_speed_entry.get():
                # cmd.extend(["--strength_begin_speed", self.strength_begin_speed_entry.get()])
            # if self.strength_predrop_speed_entry.get():
                # cmd.extend(["--strength_predrop_speed", self.strength_predrop_speed_entry.get()])            
                
            logging.info(f"Executing command: {' '.join(cmd)}")
            print(f"Executing command: {' '.join(cmd)}")

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while True:
                output = process.stdout.readline()
                error_output = process.stderr.readline()

                if output:
                    logging.info(output.strip())
                    print(output.strip())
                if error_output:
                    logging.error(f"Error: {error_output.strip()}")
                    print(f"Error: {error_output.strip()}")

                if process.poll() is not None:
                    break

            if process.returncode != 0:
                logging.error("An error occurred during command execution.")
            else:
                logging.info("Command executed successfully.")


        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            print(f"File not found: {e}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Subprocess failed: {e}")
            print(f"Subprocess failed: {e}")
        except Exception as e:
            logger.critical(f"An unhandled exception occurred: {e}")
            print(f"An unhandled exception occurred: {e}")
            
if __name__ == "__main__":
    try:
        logging.info("Inside main...")
        root = ThemedTk(theme="arc")
        root.iconbitmap('./favicon.ico')
        app = AdvancedAudioSplitterUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"An unhandled exception occurred: {e}")
        print(f"An unhandled exception occurred: {e}")