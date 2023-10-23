from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import argparse
import subprocess
import logging
from math import sin, cos, asin, pi

logging.basicConfig(level=logging.INFO)

function_type_combobox = None

def validate_inputs():
    if not file_path.get():
        return "Please select an audio file."
    try:
        fps = int(fps_value.get())
        if fps <= 0:
            return "FPS must be a positive integer."
    except ValueError:
        return "FPS must be an integer."
    try:
        intensity = float(intensity_value.get())
        if intensity <= 0:
            return "Intensity must be a positive number."
    except ValueError:
        return "Intensity must be a number."
    return None

def dict_to_str(d):
    return ','.join(f"{key}={value}" for key, value in d.items())

def validate_advanced_params(params_str):
    try:
        params = dict(map(str.strip, param.split("=")) for param in params_str.split(","))
        for k, v in params.items():
            float(v)  # Test if the value can be converted to float
    except ValueError:
        return "Advanced parameters must be in the format 'A=1,P=1,D=0,B=1' and values should be numbers."
    return None

def execute_command():
    validation_result = validate_inputs()
    if validation_result:
        messagebox.showerror("Invalid Input", validation_result)
        return

    validation_result = validate_advanced_params(advanced_params_value.get())
    if validation_result:
        messagebox.showerror("Invalid Input", validation_result)
        return

    selected_file = file_path.get()
    selected_fps = int(fps_value.get())
    selected_intensity = float(intensity_value.get())
    selected_function_type = function_type_combobox.get()
 
    advanced_params = dict(map(str.strip, param.split("=")) for param in advanced_params_value.get().split(",")) 
    advanced_params_str = dict_to_str(advanced_params)

    python_venv_path = "venv\\Scripts\\python.exe"
    
    python_path = python_venv_path if os.path.exists(python_venv_path) else "python"
        
    cmd = [
        python_path,
        "conditional_maths_bpm_keyframes.py",
        "--file", selected_file,
        "--fps", str(selected_fps),
        "--intensity", str(selected_intensity),
        "--function_type", selected_function_type,
        "--advanced_params", advanced_params_str
    ]

    if export_all_formulas.get():
        cmd.append("--export-all-formulas")   
        
    logging.info(f"Executing command: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()

    if process.returncode == 0:
        messagebox.showinfo("Success", f"Analysis completed successfully.\nOutput: {output}")
    else:
        messagebox.showerror("Error", f"An error occurred during analysis.\nError: {error}")

def browse_file():
    file = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
    file_path.set(file)

def create_widgets():
    global function_type_combobox

    ttk.Label(root, text="Audio File:").grid(row=0, column=0, sticky="e")
    ttk.Entry(root, textvariable=file_path).grid(row=0, column=1)
    ttk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2)

    ttk.Label(root, text="FPS:").grid(row=1, column=0, sticky="e")
    ttk.Entry(root, textvariable=fps_value).grid(row=1, column=1)

    ttk.Label(root, text="Intensity:").grid(row=2, column=0, sticky="e")
    ttk.Entry(root, textvariable=intensity_value).grid(row=2, column=1)  
    
    ttk.Label(root, text="Function Type:").grid(row=3, column=0, sticky="e")
    function_type_combobox = ttk.Combobox(root, textvariable=selected_function_type, values=function_type_options)
    function_type_combobox.grid(row=3, column=1)
    
    ttk.Label(root, text="Advanced Params:").grid(row=4, column=0, sticky="e")
    ttk.Entry(root, textvariable=advanced_params_value).grid(row=4, column=1)

    tooltip = "A=Amplitude, P=Phase, D=Vertical Shift, B=Second amplitude"
    advanced_params_label = ttk.Label(root, text=tooltip)
    advanced_params_label.grid(row=5, columnspan=3)
    
    ttk.Checkbutton(root, text="Export All Formulas", variable=export_all_formulas).grid(row=7, columnspan=3)
    
    ttk.Button(root, text="Run Analysis", command=execute_command).grid(row=8, columnspan=3)

root = ThemedTk(theme="arc")
root.title("AKD Conditional Maths")
root.iconbitmap('./favicon.ico')

file_path = tk.StringVar()
fps_value = tk.StringVar(value="30")
intensity_value = tk.StringVar(value="1.0")
function_type_options = ['sine', 'cosine', 'abs_sin', 'abs_cos', 'modulus', 'linear', 'triangle', 'fourier']
advanced_params_value = tk.StringVar(value="A=1,P=1,D=0,B=1")
selected_function_type = tk.StringVar()
selected_function_type.set('sine')
export_all_formulas = tk.BooleanVar(value=False)
    
create_widgets()

root.mainloop()