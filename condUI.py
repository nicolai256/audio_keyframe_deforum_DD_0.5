from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import argparse
import subprocess
import logging
from math import sin, cos, asin, pi

logging.basicConfig(level=logging.INFO)

function_type_options = ['sine', 'cosine', 'abs_sin', 'abs_cos', 'modulus', 'linear', 'triangle', 'fourier']

function_type_combobox = None

def validate_input(text, text_type, min_val=None):
    try:
        value = text_type(text)
        if min_val is not None and value <= min_val:
            return False
    except ValueError:
        return False
    return True

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
    if not all([
        validate_input(file_path.get(), str),
        validate_input(fps_value.get(), int, 0),
        validate_input(intensity_value.get(), float, 0),
        validate_input(advanced_params_value.get(), str)
    ]):
        messagebox.showerror("Invalid Input", "Please check your inputs.")
        return

    python_venv_path = "venv\\Scripts\\python.exe"
    
    python_path = python_venv_path if os.path.exists(python_venv_path) else "python"
        
    cmd = [
        python_path,
        "conditional_maths_bpm_keyframes.py",
        "--file", file_path.get(),
        "--fps", fps_value.get(),
        "--intensity", intensity_value.get(),
        "--function_type", selected_function_type.get(),
        "--advanced_params", advanced_params_value.get()
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
advanced_params_value = tk.StringVar(value="A=1,P=1,D=0,B=1")
selected_function_type = tk.StringVar(value='sine')
export_all_formulas = tk.BooleanVar(value=False)

ttk.Label(root, text="Audio File:").grid(row=0, column=0, sticky="e")
ttk.Entry(root, textvariable=file_path).grid(row=0, column=1)
ttk.Button(root, text="Browse", command=lambda: file_path.set(filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")]))).grid(row=0, column=2)

ttk.Label(root, text="FPS:").grid(row=1, column=0, sticky="e")
ttk.Entry(root, textvariable=fps_value).grid(row=1, column=1)

ttk.Label(root, text="Intensity:").grid(row=2, column=0, sticky="e")
ttk.Entry(root, textvariable=intensity_value).grid(row=2, column=1)

ttk.Label(root, text="Function Type:").grid(row=3, column=0, sticky="e")
ttk.Combobox(root, textvariable=selected_function_type, values=function_type_options).grid(row=3, column=1)

ttk.Label(root, text="Advanced Params:").grid(row=4, column=0, sticky="e")
ttk.Entry(root, textvariable=advanced_params_value).grid(row=4, column=1)

tooltip = "A=Amplitude, P=Phase, D=Vertical Shift, B=Second amplitude"
ttk.Label(root, text=tooltip).grid(row=5, columnspan=3)

ttk.Checkbutton(root, text="Export All Formulas", variable=export_all_formulas).grid(row=6, columnspan=3)
ttk.Button(root, text="Run Analysis", command=execute_command).grid(row=7, columnspan=3)

root.mainloop()