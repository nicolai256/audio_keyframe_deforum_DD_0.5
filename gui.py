import os
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import threading
import sys
import io
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

logging.info("Starting program...")

music_genre_templates = {
    "Default": {
        "speed": "4",
        "zoom_speed": "4",
        "zoom_drop_speed": "5",
        "zoom_predrop_speed": "4.5",
        "zoom_begin_speed": "4",
        "strength_predrop_speed": "0.70",
        "strength_begin_speed": "0.60",
        "strength_drop_speed": "0.50",
        "drums_drop_speed": "0.2",
        "drums_predrop_speed": "-0.2",
        "drums_begin_speed": "0.0",
        "piano_predrop_speed": "-0.4",
        "piano_drop_speed": "0.25",
        "piano_begin_speed": "0.0",
        "contrast_predrop_speed": "0.95",
        "contrast_drop_speed": "1.01",
        "contrast_begin_speed": "0.95",
        "bass_predrop_speed": "-0.4",
        "bass_drop_speed": "0.4",
        "bass_begin_speed": "0.0",
        "noise_drop_speed": "0.02",
        "noise_predrop_speed": "0.00",
        "noise_begin_speed": "0.01",
        "other_drop_speed": "0.4",
        "other_predrop_speed": "-0.4",
        "other_begin_speed": "0.0"
    },
    "Jazz": {
        "speed": "3.25",
        "zoom_speed": "3.15",
        "zoom_drop_speed": "3.65",
        "zoom_predrop_speed": "3.2",
        "zoom_begin_speed": "3",
        "strength_predrop_speed": "0.78",
        "strength_begin_speed": "0.74",
        "strength_drop_speed": "0.79",
        "drums_drop_speed": "0.17",
        "drums_predrop_speed": "0.07",
        "drums_begin_speed": "0.12",
        "piano_predrop_speed": "0.22",
        "piano_drop_speed": "0.24",
        "piano_begin_speed": "0.2",
        "contrast_predrop_speed": "0.98",
        "contrast_drop_speed": "1.03",
        "contrast_begin_speed": "0.97",
        "bass_predrop_speed": "0.22",
        "bass_drop_speed": "0.27",
        "bass_begin_speed": "0.2",
        "noise_drop_speed": "0.04",
        "noise_predrop_speed": "0.02",
        "noise_begin_speed": "0.03",
        "other_drop_speed": "0.35",
        "other_predrop_speed": "-0.25",
        "other_begin_speed": "0.15"
    },
    "Jungle": {
        "speed": "6.5",
        "zoom_speed": "6.4",
        "zoom_drop_speed": "6.8",
        "zoom_predrop_speed": "6.3",
        "zoom_begin_speed": "6.2",
        "strength_predrop_speed": "0.7",
        "strength_begin_speed": "0.68",
        "strength_drop_speed": "0.72",
        "drums_drop_speed": "0.5",
        "drums_predrop_speed": "-0.4",
        "drums_begin_speed": "0.45",
        "piano_predrop_speed": "-0.3",
        "piano_drop_speed": "0.35",
        "piano_begin_speed": "0.25",
        "contrast_predrop_speed": "0.9",
        "contrast_drop_speed": "0.92",
        "contrast_begin_speed": "0.88",
        "bass_predrop_speed": "-0.4",
        "bass_drop_speed": "0.5",
        "bass_begin_speed": "0.35",
        "noise_drop_speed": "0.06",
        "noise_predrop_speed": "0.04",
        "noise_begin_speed": "0.05",
        "other_drop_speed": "0.55",
        "other_predrop_speed": "-0.45",
        "other_begin_speed": "0.4"
    },
    "2Step": {
        "speed": "5.5",
        "zoom_speed": "5.4",
        "zoom_drop_speed": "6",
        "zoom_begin_speed": "5.3",
        "zoom_predrop_speed": "5.2",
        "strength_predrop_speed": "0.68",
        "strength_begin_speed": "0.67",
        "strength_drop_speed": "0.69",
        "drums_drop_speed": "0.35",
        "drums_predrop_speed": "-0.2",
        "drums_begin_speed": "0.15",
        "other_drop_speed": "0.45",
        "other_begin_speed": "0.2",
        "other_predrop_speed": "-0.15",
        "piano_drop_speed": "0.25",
        "piano_predrop_speed": "-0.1",
        "piano_begin_speed": "0.2",
        "bass_drop_speed": "0.4",
        "bass_predrop_speed": "-0.15",
        "bass_begin_speed": "0.2",
        "noise_drop_speed": "0.03",
        "noise_begin_speed": "0.02",
        "noise_predrop_speed": "0.01",
        "contrast_drop_speed": "1.02",
        "contrast_begin_speed": "1",
        "contrast_predrop_speed": "0.98"
    },
    "UKG": {
        "speed": "5",
        "zoom_speed": "5.1",
        "zoom_drop_speed": "5.8",
        "zoom_begin_speed": "5",
        "zoom_predrop_speed": "4.9",
        "strength_predrop_speed": "0.66",
        "strength_begin_speed": "0.65",
        "strength_drop_speed": "0.67",
        "drums_drop_speed": "0.3",
        "drums_predrop_speed": "-0.1",
        "drums_begin_speed": "0.15",
        "other_drop_speed": "0.4",
        "other_begin_speed": "0.2",
        "other_predrop_speed": "-0.1",
        "piano_drop_speed": "0.2",
        "piano_predrop_speed": "-0.05",
        "piano_begin_speed": "0.18",
        "bass_drop_speed": "0.35",
        "bass_predrop_speed": "-0.1",
        "bass_begin_speed": "0.18",
        "noise_drop_speed": "0.02",
        "noise_begin_speed": "0.01",
        "noise_predrop_speed": "0",
        "contrast_drop_speed": "1.01",
        "contrast_begin_speed": "1",
        "contrast_predrop_speed": "0.99"
    },
    "Classical": {
        "speed": "2.1",
        "zoom_speed": "2.05",
        "zoom_drop_speed": "2.6",
        "zoom_begin_speed": "2",
        "zoom_predrop_speed": "1.9",
        "strength_predrop_speed": "0.87",
        "strength_begin_speed": "0.88",
        "strength_drop_speed": "0.86",
        "drums_drop_speed": "0",
        "drums_predrop_speed": "0",
        "drums_begin_speed": "0",
        "other_drop_speed": "0.15",
        "other_begin_speed": "0.1",
        "other_predrop_speed": "0",
        "piano_predrop_speed": "0.07",
        "piano_drop_speed": "0.12",
        "piano_begin_speed": "0.1",
        "bass_predrop_speed": "0.08",
        "bass_drop_speed": "0.12",
        "bass_begin_speed": "0.1",
        "noise_drop_speed": "0.01",
        "noise_begin_speed": "0.005",
        "noise_predrop_speed": "0",
        "contrast_drop_speed": "1.01",
        "contrast_begin_speed": "0.97",
        "contrast_predrop_speed": "0.95"
    },
    "Hip-Hop": {
        "speed": "5.2",
        "zoom_speed": "5.1",
        "zoom_drop_speed": "5.6",
        "zoom_begin_speed": "5",
        "zoom_predrop_speed": "5",
        "strength_predrop_speed": "0.67",
        "strength_begin_speed": "0.66",
        "strength_drop_speed": "0.68",
        "drums_drop_speed": "0.28",
        "drums_predrop_speed": "-0.08",
        "drums_begin_speed": "0.1",
        "piano_predrop_speed": "-0.18",
        "piano_drop_speed": "0.32",
        "piano_begin_speed": "0.15",
        "contrast_predrop_speed": "0.95",
        "contrast_drop_speed": "1",
        "contrast_begin_speed": "0.94",
        "bass_predrop_speed": "-0.18",
        "bass_drop_speed": "0.32",
        "bass_begin_speed": "0.2",
        "noise_drop_speed": "0.03",
        "noise_begin_speed": "0.02",
        "noise_predrop_speed": "0.01",
        "other_drop_speed": "0.35",
        "other_begin_speed": "0.1",
        "other_predrop_speed": "-0.15"
    },
    "Minimal": {
        "speed": "4",
        "zoom_speed": "4",
        "zoom_drop_speed": "4.5",
        "zoom_begin_speed": "4",
        "zoom_predrop_speed": "3.9",
        "strength_predrop_speed": "0.6",
        "strength_begin_speed": "0.59",
        "strength_drop_speed": "0.61",
        "drums_drop_speed": "0.2",
        "drums_predrop_speed": "-0.1",
        "drums_begin_speed": "0.1",
        "piano_predrop_speed": "-0.2",
        "piano_drop_speed": "0.25",
        "piano_begin_speed": "0.1",
        "contrast_predrop_speed": "0.9",
        "contrast_drop_speed": "0.92",
        "contrast_begin_speed": "0.88",
        "bass_predrop_speed": "-0.2",
        "bass_drop_speed": "0.25",
        "bass_begin_speed": "0.1",
        "noise_drop_speed": "0.02",
        "noise_begin_speed": "0.01",
        "noise_predrop_speed": "0",
        "other_drop_speed": "0.3",
        "other_begin_speed": "0.1",
        "other_predrop_speed": "-0.1"
    },
    "Abstract": {
        "speed": "6",
        "zoom_speed": "6",
        "zoom_drop_speed": "6.5",
        "zoom_begin_speed": "6",
        "zoom_predrop_speed": "5.9",
        "strength_predrop_speed": "0.55",
        "strength_begin_speed": "0.54",
        "strength_drop_speed": "0.56",
        "drums_drop_speed": "0.4",
        "drums_predrop_speed": "-0.2",
        "drums_begin_speed": "0.2",
        "piano_predrop_speed": "-0.3",
        "piano_drop_speed": "0.35",
        "piano_begin_speed": "0.2",
        "contrast_predrop_speed": "0.9",
        "contrast_drop_speed": "0.92",
        "contrast_begin_speed": "0.88",
        "bass_predrop_speed": "-0.3",
        "bass_drop_speed": "0.35",
        "bass_begin_speed": "0.2",
        "noise_drop_speed": "0.03",
        "noise_begin_speed": "0.02",
        "noise_predrop_speed": "0.01",
        "other_drop_speed": "0.4",
        "other_begin_speed": "0.2",
        "other_predrop_speed": "-0.2"
    },
    "Violent": {
        "speed": "9",
        "zoom_speed": "9",
        "zoom_drop_speed": "9.5",
        "zoom_begin_speed": "8.9",
        "zoom_predrop_speed": "9.1",
        "noise_drop_speed": "0.04",
        "noise_begin_speed": "0.03",
        "noise_predrop_speed": "0.02",
        "other_drop_speed": "0.6",
        "other_begin_speed": "0.5",
        "other_predrop_speed": "0.55",
        "strength_predrop_speed": "0.9",
        "strength_begin_speed": "0.88",
        "strength_drop_speed": "0.92",
        "drums_drop_speed": "0.6",
        "drums_predrop_speed": "-0.5",
        "drums_begin_speed": "0.55",
        "piano_predrop_speed": "-0.4",
        "piano_drop_speed": "0.5",
        "piano_begin_speed": "0.45",
        "contrast_predrop_speed": "1.1",
        "contrast_drop_speed": "1.15",
        "contrast_begin_speed": "1.05",
        "bass_predrop_speed": "-0.6",
        "bass_drop_speed": "0.7",
        "bass_begin_speed": "0.65"
    },
    "Techno": {
        "speed": "5.2",
        "zoom_speed": "5.3",
        "zoom_drop_speed": "5.7",
        "zoom_predrop_speed": "5.1",
        "noise_drop_speed": "0.03",
        "noise_begin_speed": "0.02",
        "noise_predrop_speed": "0.01",
        "other_drop_speed": "0.5",
        "other_begin_speed": "0.45",
        "other_predrop_speed": "0.48",
        "strength_predrop_speed": "0.85",
        "strength_begin_speed": "0.83",
        "strength_drop_speed": "0.87",
        "drums_drop_speed": "0.5",
        "drums_predrop_speed": "-0.45",
        "drums_begin_speed": "0.48",
        "piano_predrop_speed": "-0.35",
        "piano_drop_speed": "0.4",
        "piano_begin_speed": "0.38",
        "contrast_predrop_speed": "1.05",
        "contrast_drop_speed": "1.08",
        "contrast_begin_speed": "1.02",
        "bass_predrop_speed": "-0.5",
        "bass_drop_speed": "0.55",
        "bass_begin_speed": "0.52"
    },
    "Reggae": {
        "speed": "4",
        "zoom_speed": "4",
        "zoom_drop_speed": "4.5",
        "zoom_begin_speed": "3.9",
        "zoom_predrop_speed": "4.1",
        "noise_drop_speed": "0.01",
        "noise_begin_speed": "0.005",
        "noise_predrop_speed": "0.007",
        "other_drop_speed": "0.3",
        "other_begin_speed": "0.28",
        "other_predrop_speed": "0.29",
        "strength_predrop_speed": "0.75",
        "strength_begin_speed": "0.73",
        "strength_drop_speed": "0.77",
        "drums_drop_speed": "0.2",
        "drums_predrop_speed": "-0.18",
        "drums_begin_speed": "0.19",
        "piano_predrop_speed": "-0.15",
        "piano_drop_speed": "0.2",
        "piano_begin_speed": "0.18",
        "contrast_predrop_speed": "0.98",
        "contrast_drop_speed": "1.01",
        "contrast_begin_speed": "0.97",
        "bass_predrop_speed": "-0.2",
        "bass_drop_speed": "0.25",
        "bass_begin_speed": "0.22"
    },
    "Lounge": {
        "speed": "3",
        "zoom_speed": "2.9",
        "zoom_drop_speed": "3.1",
        "zoom_begin_speed": "2.8",
        "zoom_predrop_speed": "2.9",
        "strength_drop_speed": "0.7",
        "strength_begin_speed": "0.69",
        "strength_predrop_speed": "0.71",
        "drums_drop_speed": "0.1",
        "drums_begin_speed": "0.09",
        "drums_predrop_speed": "0.08",
        "noise_drop_speed": "0.01",
        "noise_begin_speed": "0.009",
        "noise_predrop_speed": "0.008",
        "other_drop_speed": "0.2",
        "other_begin_speed": "0.19",
        "other_predrop_speed": "0.18",
        "piano_drop_speed": "0.25",
        "piano_begin_speed": "0.24",
        "piano_predrop_speed": "0.23",
        "contrast_drop_speed": "0.98",
        "contrast_begin_speed": "0.97",
        "contrast_predrop_speed": "0.96",
        "bass_drop_speed": "0.2",
        "bass_begin_speed": "0.19",
        "bass_predrop_speed": "0.18"
    },
    "Deep Dub": {
        "speed": "6.1",
        "zoom_speed": "6.2",
        "zoom_drop_speed": "6.7",
        "zoom_begin_speed": "6",
        "zoom_predrop_speed": "6.1",
        "strength_drop_speed": "0.58",
        "strength_begin_speed": "0.56",
        "strength_predrop_speed": "0.57",
        "drums_drop_speed": "0.42",
        "drums_begin_speed": "0.05",
        "drums_predrop_speed": "-0.38",
        "noise_drop_speed": "0.02",
        "noise_begin_speed": "0.01",
        "noise_predrop_speed": "0",
        "other_drop_speed": "0.5",
        "other_begin_speed": "0.1",
        "other_predrop_speed": "-0.48",
        "piano_drop_speed": "0.52",
        "piano_begin_speed": "0.1",
        "piano_predrop_speed": "-0.48",
        "contrast_drop_speed": "0.92",
        "contrast_begin_speed": "0.88",
        "contrast_predrop_speed": "0.9",
        "bass_drop_speed": "0.52",
        "bass_begin_speed": "0.1",
        "bass_predrop_speed": "-0.48"
    },
    "Funk": {
        "speed": "3.1",
        "zoom_speed": "3.05",
        "zoom_drop_speed": "4.2",
        "zoom_begin_speed": "3",
        "zoom_predrop_speed": "3.1",
        "strength_drop_speed": "0.73",
        "strength_begin_speed": "0.71",
        "strength_predrop_speed": "0.72",
        "drums_drop_speed": "0.17",
        "drums_begin_speed": "0.1",
        "drums_predrop_speed": "-0.13",
        "noise_drop_speed": "0.015",
        "noise_begin_speed": "0.01",
        "noise_predrop_speed": "0",
        "other_drop_speed": "0.22",
        "other_begin_speed": "0.1",
        "other_predrop_speed": "-0.08",
        "piano_drop_speed": "0.22",
        "piano_begin_speed": "0.1",
        "piano_predrop_speed": "-0.08",
        "contrast_drop_speed": "0.97",
        "contrast_begin_speed": "0.94",
        "contrast_predrop_speed": "0.95",
        "bass_drop_speed": "0.27",
        "bass_begin_speed": "0.1",
        "bass_predrop_speed": "-0.08"
    },
    "Psychedelic": {
        "speed": "7.2",
        "zoom_speed": "7.1",
        "zoom_drop_speed": "8.2",
        "zoom_predrop_speed": "7",
        "zoom_begin_speed": "7",
        "strength_predrop_speed": "0.52",
        "strength_begin_speed": "0.51",
        "strength_drop_speed": "0.53",
        "drums_drop_speed": "0.42",
        "drums_predrop_speed": "-0.28",
        "drums_begin_speed": "0.05",
        "piano_predrop_speed": "-0.38",
        "piano_drop_speed": "0.47",
        "piano_begin_speed": "0.1",
        "contrast_predrop_speed": "0.9",
        "contrast_drop_speed": "0.92",
        "contrast_begin_speed": "0.88",
        "bass_predrop_speed": "-0.38",
        "bass_drop_speed": "0.47",
        "bass_begin_speed": "0.1",
        "noise_drop_speed": "0.02",
        "noise_begin_speed": "0.01",
        "noise_predrop_speed": "0",
        "other_drop_speed": "0.4",
        "other_begin_speed": "0",
        "other_predrop_speed": "-0.4"
    },
    "Ambient": {
        "speed": "2",
        "zoom_speed": "2",
        "zoom_drop_speed": "2.5",
        "zoom_predrop_speed": "1.8",
        "zoom_begin_speed": "2",
        "strength_predrop_speed": "0.8",
        "strength_begin_speed": "0.8",
        "strength_drop_speed": "0.8",
        "drums_drop_speed": "0",
        "drums_predrop_speed": "0",
        "drums_begin_speed": "0",
        "piano_predrop_speed": "0.1",
        "piano_drop_speed": "0.15",
        "piano_begin_speed": "0.1",
        "contrast_predrop_speed": "0.95",
        "contrast_drop_speed": "0.95",
        "contrast_begin_speed": "0.95",
        "bass_predrop_speed": "0.05",
        "bass_drop_speed": "0.1",
        "bass_begin_speed": "0.05",
        "noise_drop_speed": "0.01",
        "noise_begin_speed": "0.01",
        "noise_predrop_speed": "0",
        "other_drop_speed": "0.2",
        "other_begin_speed": "0",
        "other_predrop_speed": "-0.2"
    },
    "Cinematic": {
        "speed": "4",
        "zoom_speed": "4",
        "zoom_drop_speed": "4.5",
        "zoom_predrop_speed": "3.8",
        "zoom_begin_speed": "4",
        "strength_predrop_speed": "0.75",
        "strength_begin_speed": "0.76",
        "strength_drop_speed": "0.77",
        "drums_drop_speed": "0.2",
        "drums_predrop_speed": "-0.1",
        "drums_begin_speed": "0.15",
        "piano_predrop_speed": "0.3",
        "piano_drop_speed": "0.35",
        "piano_begin_speed": "0.25",
        "contrast_predrop_speed": "1",
        "contrast_drop_speed": "1.02",
        "contrast_begin_speed": "0.98",
        "bass_predrop_speed": "0.2",
        "bass_drop_speed": "0.25",
        "bass_begin_speed": "0.15",
        "noise_drop_speed": "0.02",
        "noise_begin_speed": "0.02",
        "noise_predrop_speed": "0.01",
        "other_drop_speed": "0.4",
        "other_begin_speed": "0.1",
        "other_predrop_speed": "-0.3"
    },
    "Vaporwave": {
        "speed": "2.5",
        "zoom_speed": "2.5",
        "zoom_drop_speed": "3",
        "zoom_predrop_speed": "2.4",
        "zoom_begin_speed": "2.5",
        "strength_predrop_speed": "0.65",
        "strength_begin_speed": "0.67",
        "strength_drop_speed": "0.63",
        "drums_drop_speed": "0.1",
        "drums_predrop_speed": "-0.1",
        "drums_begin_speed": "0.05",
        "piano_predrop_speed": "-0.3",
        "piano_drop_speed": "0.2",
        "piano_begin_speed": "0.1",
        "contrast_predrop_speed": "0.9",
        "contrast_drop_speed": "0.92",
        "contrast_begin_speed": "0.91",
        "bass_predrop_speed": "-0.3",
        "bass_drop_speed": "0.3",
        "bass_begin_speed": "0.1",
        "noise_drop_speed": "0.01",
        "noise_predrop_speed": "0.00",
        "noise_begin_speed": "0.01",
        "other_drop_speed": "0.3",
        "other_predrop_speed": "-0.3",
        "other_begin_speed": "0.1"
    },
    "Chillstep": {
        "speed": "3.5",
        "zoom_speed": "3.5",
        "zoom_drop_speed": "4",
        "zoom_predrop_speed": "3.4",
        "zoom_begin_speed": "3.5",
        "strength_predrop_speed": "0.60",
        "strength_begin_speed": "0.62",
        "strength_drop_speed": "0.58",
        "drums_drop_speed": "0.2",
        "drums_predrop_speed": "-0.15",
        "drums_begin_speed": "0.1",
        "piano_predrop_speed": "-0.2",
        "piano_drop_speed": "0.2",
        "piano_begin_speed": "0.15",
        "contrast_predrop_speed": "0.93",
        "contrast_drop_speed": "0.95",
        "contrast_begin_speed": "0.92",
        "bass_predrop_speed": "-0.2",
        "bass_drop_speed": "0.3",
        "bass_begin_speed": "0.15",
        "noise_drop_speed": "0.02",
        "noise_predrop_speed": "0.01",
        "noise_begin_speed": "0.02",
        "other_drop_speed": "0.25",
        "other_predrop_speed": "-0.25",
        "other_begin_speed": "0.15"
    },
    "FeelTheFonk#1": {
        "speed": "4.8",
        "zoom_speed": "4.8",
        "zoom_drop_speed": "5.5",
        "zoom_predrop_speed": "4.7",
        "zoom_begin_speed": "4.8",
        "strength_predrop_speed": "0.76",
        "strength_begin_speed": "0.78",
        "strength_drop_speed": "0.77",
        "drums_drop_speed": "0.25",
        "drums_predrop_speed": "-0.15",
        "drums_begin_speed": "0.2",
        "piano_predrop_speed": "-0.1",
        "piano_drop_speed": "0.3",
        "piano_begin_speed": "0.25",
        "contrast_predrop_speed": "0.99",
        "contrast_drop_speed": "1.03",
        "contrast_begin_speed": "0.98",
        "bass_predrop_speed": "-0.1",
        "bass_drop_speed": "0.35",
        "bass_begin_speed": "0.3",
        "noise_drop_speed": "0.03",
        "noise_predrop_speed": "0.02",
        "noise_begin_speed": "0.025",
        "other_drop_speed": "0.35",
        "other_predrop_speed": "-0.3",
        "other_begin_speed": "0.25"
    },
    "FeelTheFonk#2": {
        "speed": "5.1",
        "zoom_speed": "5.2",
        "zoom_drop_speed": "5.8",
        "zoom_predrop_speed": "5.1",
        "zoom_begin_speed": "5.2",
        "strength_predrop_speed": "0.81",
        "strength_begin_speed": "0.83",
        "strength_drop_speed": "0.82",
        "drums_drop_speed": "0.3",
        "drums_predrop_speed": "-0.1",
        "drums_begin_speed": "0.25",
        "piano_predrop_speed": "0.0",
        "piano_drop_speed": "0.35",
        "piano_begin_speed": "0.3",
        "contrast_predrop_speed": "1.0",
        "contrast_drop_speed": "1.04",
        "contrast_begin_speed": "0.99",
        "bass_predrop_speed": "0.0",
        "bass_drop_speed": "0.4",
        "bass_begin_speed": "0.35",
        "noise_drop_speed": "0.04",
        "noise_predrop_speed": "0.03",
        "noise_begin_speed": "0.035",
        "other_drop_speed": "0.4",
        "other_predrop_speed": "-0.2",
        "other_begin_speed": "0.3"
    },   
}

class TextRedirector(io.StringIO):
    def __init__(self, app_object, message_type="info"):
        """
        :param app_object: The main application object that contains the add_message method.
        :param message_type: The default type of the message. Can be "info", "error", etc.
        """
        self.app_object = app_object
        self.message_type = message_type

    def write(self, str):
        # Schedule _write to run as soon as possible
        self.app_object.after(0, self._write, str)

    def _write(self, str):
        try:
            # Detect message type if possible (this part can be customized as needed)
            detected_type = self.message_type
            if "error" in str.lower():
                detected_type = "error"
            elif "warning" in str.lower():
                detected_type = "warning"
            # ...

            # Add message to the console
            self.app_object.add_message(str.strip(), detected_type)
        except tk.TclError as e:
            # Log the error if the Tkinter operation fails
            logging.error(f"Error in TextRedirector: {e}")

    def flush(self):
        """
        Implement flush method to prevent "io.UnsupportedOperation: fileno" errors.
        """
        pass
            
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
        self.master.geometry('690x890')        
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
        self.spleeter_frame = self.create_labeled_frame("Sounds Settings", row=1, col=0)
        self.script_frame = self.create_labeled_frame("Script Settings", row=2, col=0)
        self.advanced_frame = self.create_labeled_frame("Advanced Settings", row=3, col=0)
        
        # Create Widgets for Each Frame
        self.create_audio_widgets(self.audio_frame)
        self.create_spleeter_widgets(self.spleeter_frame)
        self.create_advanced_widgets(self.advanced_frame)

        # Create a frame to hold the console and its scrollbar
        console_frame = tk.Frame(self.master)
        console_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=1)

        # Adding a Text widget to serve as a console
        self.console = tk.Text(console_frame, wrap=tk.WORD, height=11, width=66,
                               bg="black", fg="white", font=("Courier New", 12))
        self.console.pack(side=tk.LEFT, fill=tk.BOTH)

        # Adding a Scrollbar
        scrollbar = ttk.Scrollbar(console_frame, orient="vertical", command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=scrollbar.set)

        # Configure tags
        self.console.tag_configure("error", foreground="red")
        self.console.tag_configure("warning", foreground="orange")
        self.console.tag_configure("info", foreground="lightgreen")
        self.console.tag_configure("highlight", background="yellow")
        self.console.tag_configure("timestamp", foreground="green")

        # Redirect stdout and stderr
        sys.stdout = TextRedirector(self, message_type="info")  # Note : Passez 'self' ici
        sys.stderr = TextRedirector(self, message_type="error") 

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
        ToolTip(self.contrast_drop_speed_entry, "Reactive contrast impact of the audio on the animation when the audio makes a sound.")
        ToolTip(self.contrast_predrop_speed_entry, "Reactive contrast impact of the audio on the animation right before the audio makes a sound.")
        ToolTip(self.contrast_begin_speed_entry, "Reactive contrast impact of the audio on the animation (starting value on keyframe 1.")
        ToolTip(self.other_drop_speed_entry, "Reactive other impact of the audio on the animation when the audio makes a sound.")
        ToolTip(self.other_predrop_speed_entry, "Reactive other impact of the audio on the animation right before the audio makes a sound.")
        ToolTip(self.other_begin_speed_entry, "Reactive other impact of the audio on the animation (starting value on keyframe 1.")
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
        ToolTip(self.strength_drop_speed_entry, "Reactive image strength impact of the audio on the animation when the audio makes a sound.")        
        ToolTip(self.strength_predrop_speed_entry, "Reactive image strength impact of the audio on the animation right before the audio makes a sound.")        
        ToolTip(self.strength_begin_speed_entry, "Reactive image strength impact of the audio on the animation (starting value on keyframe 1.")        
        ToolTip(self.zoom_drop_speed_entry, "Reactive zoom drop speed for the audio.")
        ToolTip(self.music_cut_entry, "Cut in X splits")
        ToolTip(self.drums_predrop_speed_entry, "Pre-drop value for the impact of drums.")
        ToolTip(self.bass_begin_speed_entry, "Starting value on keyframe 1 for bass.")
        ToolTip(self.bass_predrop_speed_entry, "Value just before a drop for bass.")
        ToolTip(self.speed_entry, "The amplitude / strength / intensity of your animation.")
        ToolTip(self.zoom_speed_entry, "The amplitude / strength / intensity of your animation.")
        ToolTip(self.zoom_drop_speed_entry, "Reactive zoom impact of the audio on the animation when the audio makes a sound.")
        ToolTip(self.noise_drop_speed_entry, "Reactive impact of the noise schedule when the audio makes a sound.")
        ToolTip(self.contrast_drop_speed_entry, "Reactive impact of the contrast schedule when the audio makes a sound.")
        ToolTip(self.zoom_predrop_speed_entry, "Reactive zoom impact of the audio on the animation right before the audio makes a sound.")
        ToolTip(self.zoom_begin_speed_entry, "Reactive zoom impact of the audio on the animation (starting value on keyframe 1.")
       
        self.fps_entry.insert(0, "30")
        self.speed_entry.insert(0, "4")
        self.zoom_speed_entry.insert(0, "4")
        self.stems_entry.insert(0, "4")
        self.zoom_drop_speed_entry.insert(0, "5")        
        self.zoom_predrop_speed_entry.insert(0, "0.5")        
        self.zoom_begin_speed_entry.insert(0, "0")        
        self.strength_drop_speed_entry.insert(0, "0.50")
        self.strength_predrop_speed_entry.insert(0, "0.60")
        self.strength_begin_speed_entry.insert(0, "0.70")
        self.contrast_drop_speed_entry.insert(0, "1.01")
        self.contrast_predrop_speed_entry.insert(0, "0.95")
        self.contrast_begin_speed_entry.insert(0, "0.95")
        self.noise_drop_speed_entry.insert(0, "0.02")
        self.noise_predrop_speed_entry.insert(0, "0.00")
        self.noise_begin_speed_entry.insert(0, "0.01")
        self.other_drop_speed_entry.insert(0, "0.4")
        self.other_predrop_speed_entry.insert(0, "-0.4")
        self.other_begin_speed_entry.insert(0, "0.0")
        self.drums_drop_speed_entry.insert(0, "0.2")
        self.drums_predrop_speed_entry.insert(0, "-0.2")
        self.drums_begin_speed_entry.insert(0, "0.0")
        self.piano_predrop_speed_entry.insert(0, "-0.4")
        self.piano_drop_speed_entry.insert(0, "0.25")
        self.piano_begin_speed_entry.insert(0, "0.0")
        self.bass_predrop_speed_entry.insert(0, "-0.4")
        self.bass_drop_speed_entry.insert(0, "0.4")
        self.bass_begin_speed_entry.insert(0, "0.0")

        self.maths_cond_button = ttk.Button(self.master, text="Maths Cond.", command=self.open_cond_ui)
        self.maths_cond_button.grid(row=0, column=2, sticky=(tk.E), pady=0, padx=0)

        self.execute_button = ttk.Button(self.master, text="Execute", command=self.execute_command_threaded)
        self.execute_button.grid(row=0, column=2, sticky=(tk.E, tk.S), pady=0, padx=0)

    def load_genre_template(self):
        selected_genre = self.music_genre_combo.get()
        if selected_genre in music_genre_templates:
            template = music_genre_templates[selected_genre]
            
            widget_mapping = {
                'speed': self.speed_entry,
                'zoom_speed': self.zoom_speed_entry,
                'zoom_drop_speed': self.zoom_drop_speed_entry,
                'zoom_predrop_speed': self.zoom_predrop_speed_entry,
                'zoom_begin_speed': self.zoom_begin_speed_entry,
                'strength_drop_speed': self.strength_drop_speed_entry,
                'strength_predrop_speed': self.strength_predrop_speed_entry,
                'strength_begin_speed': self.strength_begin_speed_entry,
                'drums_drop_speed': self.drums_drop_speed_entry,
                'drums_predrop_speed': self.drums_predrop_speed_entry,
                'drums_begin_speed': self.drums_begin_speed_entry,
                'piano_predrop_speed': self.piano_predrop_speed_entry,
                'piano_drop_speed': self.piano_drop_speed_entry,
                'piano_begin_speed': self.piano_begin_speed_entry,
                'bass_predrop_speed': self.bass_predrop_speed_entry,
                'bass_drop_speed': self.bass_drop_speed_entry,
                'bass_begin_speed': self.bass_begin_speed_entry,
                'noise_begin_speed': self.noise_begin_speed_entry,
                'noise_drop_speed': self.noise_drop_speed_entry,
                'noise_predrop_speed': self.noise_predrop_speed_entry,
                'other_predrop_speed': self.other_predrop_speed_entry,
                'other_drop_speed': self.other_drop_speed_entry,
                'other_begin_speed': self.other_begin_speed_entry,
                'contrast_drop_speed': self.contrast_drop_speed_entry,
                'contrast_predrop_speed': self.contrast_predrop_speed_entry,
                'contrast_begin_speed': self.contrast_begin_speed_entry
            }
            
            for key, widget in widget_mapping.items():
                widget.delete(0, tk.END)
                if key in template:
                    widget.insert(0, template[key])
                else:
                    print(f"Warning: Key {key} not found in the selected genre template.")
        else:
            print(f"Warning: Selected genre {selected_genre} not found in templates.")

    def add_message(self, message, tag):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.console.insert(tk.END, f"{message}\n", tag)
        self.console.config(state=tk.DISABLED)
        self.console.see(tk.END)  # Auto-scroll to the end

    def open_cond_ui(self):
        subprocess.Popen([sys.executable, "condUI.py"])
        
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
        self.spleeter_var = tk.IntVar(value=1)
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

        ttk.Label(self.audio_frame, text="Music Cut:").grid(row=1, column=3, sticky=(tk.W))
        self.music_cut_entry = ttk.Entry(self.audio_frame)
        self.music_cut_entry.grid(row=1, column=4, sticky=(tk.W))

        ttk.Label(self.audio_frame, text="Music Start:").grid(row=2, column=3, sticky=(tk.W))
        self.music_start_entry = ttk.Entry(self.audio_frame)
        self.music_start_entry.grid(row=2, column=4, sticky=(tk.W))

        ttk.Label(self.audio_frame, text="Music End:").grid(row=3, column=3, sticky=(tk.W))
        self.music_end_entry = ttk.Entry(self.audio_frame)
        self.music_end_entry.grid(row=3, column=4, sticky=(tk.W))

        ttk.Label(frame, text="Stems:").grid(row=4, column=3, sticky=(tk.W))
        self.stems_entry = ttk.Entry(frame)
        self.stems_entry.grid(row=4, column=4, sticky=(tk.W))
        
    def create_spleeter_widgets(self, frame):
        
        ttk.Label(frame, text="Zoom Sound:").grid(row=2, column=0, sticky=(tk.W))
        self.zoom_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.zoom_sound_combo.grid(row=2, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Strength Sound:").grid(row=3, column=0, sticky=(tk.W))
        self.strength_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.strength_sound_combo.grid(row=3, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Noise Sound:").grid(row=2, column=2, sticky=(tk.W))
        self.noise_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.noise_sound_combo.grid(row=2, column=3, sticky=(tk.W))

        ttk.Label(frame, text="Contrast Sound:").grid(row=3, column=2, sticky=(tk.W))
        self.contrast_sound_combo = ttk.Combobox(frame, values=("drums", "other", "piano", "bass"))
        self.contrast_sound_combo.grid(row=3, column=3, sticky=(tk.W))

    def create_advanced_widgets(self, frame):
       
        ttk.Label(frame, text="Zoom Drop Speed:").grid(row=1, column=2, sticky=(tk.W))
        self.zoom_drop_speed_entry = ttk.Entry(frame)
        self.zoom_drop_speed_entry.grid(row=1, column=3, sticky=(tk.W))
            
        ttk.Label(frame, text="Zoom Begin Speed:").grid(row=2, column=2, sticky=(tk.W))
        self.zoom_begin_speed_entry = ttk.Entry(frame)
        self.zoom_begin_speed_entry.grid(row=2, column=3, sticky=(tk.W))

        ttk.Label(frame, text="Zoom Pre-drop Speed:").grid(row=3, column=2, sticky=(tk.W))
        self.zoom_predrop_speed_entry = ttk.Entry(frame)
        self.zoom_predrop_speed_entry.grid(row=3, column=3, sticky=(tk.W))

        ttk.Label(frame, text="Noise Begin Speed:").grid(row=4, column=2, sticky=(tk.W))
        self.noise_begin_speed_entry = ttk.Entry(frame)
        self.noise_begin_speed_entry.grid(row=4, column=3, sticky=(tk.W))
            
        ttk.Label(frame, text="Noise Drop Speed:").grid(row=6, column=2, sticky=(tk.W))
        self.noise_drop_speed_entry = ttk.Entry(frame)
        self.noise_drop_speed_entry.grid(row=6, column=3, sticky=(tk.W))
        
        ttk.Label(frame, text="Noise Pre-drop Speed:").grid(row=5, column=2, sticky=(tk.W))
        self.noise_predrop_speed_entry = ttk.Entry(frame)
        self.noise_predrop_speed_entry.grid(row=5, column=3, sticky=(tk.W))
        
        ttk.Label(frame, text="Contrast Begin Speed:").grid(row=6, column=2, sticky=(tk.W))
        self.contrast_begin_speed_entry = ttk.Entry(frame)
        self.contrast_begin_speed_entry.grid(row=6, column=3, sticky=(tk.W))

        ttk.Label(frame, text="Contrast Drop Speed:").grid(row=7, column=2, sticky=(tk.W))
        self.contrast_drop_speed_entry = ttk.Entry(frame)
        self.contrast_drop_speed_entry.grid(row=7, column=3, sticky=(tk.W))
             
        ttk.Label(frame, text="Contrast Pre-drop Speed:").grid(row=8, column=2, sticky=(tk.W))
        self.contrast_predrop_speed_entry = ttk.Entry(frame)
        self.contrast_predrop_speed_entry.grid(row=8, column=3, sticky=(tk.W))
            
        ttk.Label(frame, text="Strength Begin Speed:").grid(row=9, column=2, sticky=(tk.W))
        self.strength_begin_speed_entry = ttk.Entry(frame)
        self.strength_begin_speed_entry.grid(row=9, column=3, sticky=(tk.W))
  
        ttk.Label(frame, text="Strength Drop Speed:").grid(row=10, column=2, sticky=(tk.W))
        self.strength_drop_speed_entry = ttk.Entry(frame)
        self.strength_drop_speed_entry.grid(row=10, column=3, sticky=(tk.W))
        
        ttk.Label(frame, text="Strength Pre-drop Speed:").grid(row=11, column=2, sticky=(tk.W))
        self.strength_predrop_speed_entry = ttk.Entry(frame)
        self.strength_predrop_speed_entry.grid(row=11, column=3, sticky=(tk.W))

        ttk.Label(frame, text="Other Begin Speed:").grid(row=10, column=0, sticky=(tk.W))
        self.other_begin_speed_entry = ttk.Entry(frame)
        self.other_begin_speed_entry.grid(row=10, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Other Pre-drop Speed:").grid(row=11, column=0, sticky=(tk.W))
        self.other_predrop_speed_entry = ttk.Entry(frame)
        self.other_predrop_speed_entry.grid(row=11, column=1, sticky=(tk.W))
      
        ttk.Label(frame, text="Other Drop Speed:").grid(row=9, column=0, sticky=(tk.W))
        self.other_drop_speed_entry = ttk.Entry(frame)
        self.other_drop_speed_entry.grid(row=9, column=1, sticky=(tk.W))
      
        self.music_genre_label = ttk.Label(frame, text="Genre:")
        self.music_genre_label.grid(row=0, column=0, sticky=(tk.W))

        self.music_genre_combo = ttk.Combobox(frame, values=list(music_genre_templates.keys()))
        self.music_genre_combo.grid(row=0, column=1, sticky=(tk.W))
        self.music_genre_combo.bind("<<ComboboxSelected>>", lambda event: self.load_genre_template())

        ttk.Label(frame, text="Drums Drop Speed:").grid(row=0, column=2, sticky=(tk.W))
        self.drums_drop_speed_entry = ttk.Entry(frame)
        self.drums_drop_speed_entry.grid(row=0, column=3, sticky=(tk.W))

        ttk.Label(frame, text="Drums Pre-drop Speed:").grid(row=1, column=0, sticky=(tk.W))
        self.drums_predrop_speed_entry = ttk.Entry(frame)
        self.drums_predrop_speed_entry.grid(row=1, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Drums Begin Speed:").grid(row=2, column=0, sticky=(tk.W))
        self.drums_begin_speed_entry = ttk.Entry(frame)
        self.drums_begin_speed_entry.grid(row=2, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Piano Drop Speed:").grid(row=3, column=0, sticky=(tk.W))
        self.piano_drop_speed_entry = ttk.Entry(frame)
        self.piano_drop_speed_entry.grid(row=3, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Piano Begin Speed:").grid(row=4, column=0, sticky=(tk.W))
        self.piano_begin_speed_entry = ttk.Entry(frame)
        self.piano_begin_speed_entry.grid(row=4, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Piano Pre-drop Speed:").grid(row=5, column=0, sticky=(tk.W))
        self.piano_predrop_speed_entry = ttk.Entry(frame)
        self.piano_predrop_speed_entry.grid(row=5, column=1, sticky=(tk.W))
        
        ttk.Label(frame, text="Bass Drop Speed:").grid(row=6, column=0, sticky=(tk.W))
        self.bass_drop_speed_entry = ttk.Entry(frame)
        self.bass_drop_speed_entry.grid(row=6, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Bass Begin Speed:").grid(row=7, column=0, sticky=(tk.W))
        self.bass_begin_speed_entry = ttk.Entry(frame)
        self.bass_begin_speed_entry.grid(row=7, column=1, sticky=(tk.W))

        ttk.Label(frame, text="Bass Pre-drop Speed:").grid(row=8, column=0, sticky=(tk.W))
        self.bass_predrop_speed_entry = ttk.Entry(frame)
        self.bass_predrop_speed_entry.grid(row=8, column=1, sticky=(tk.W))
            
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
                logging.error("Invalid input. Please correct.")
                self.add_message("Invalid input. Please correct.", "error")
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
            drums_begin_speed = self.drums_begin_speed_entry.get()
            drums_drop_speed = self.drums_drop_speed_entry.get()
            drums_predrop_speed = self.drums_predrop_speed_entry.get()
            drums_audio_path = self.drums_audio_path_entry.get()
            bass_begin_speed_entry = self.bass_begin_speed_entry.get()
            bass_drop_speed_entry = self.bass_drop_speed_entry.get()
            bass_predrop_speed_entry = self.bass_predrop_speed_entry.get()
            strength_drop_speed = self.strength_drop_speed_entry.get()
            strength_predrop_speed = self.strength_predrop_speed_entry.get()
            strength_begin_speed = self.strength_begin_speed_entry.get()
            piano_drop_speed = self.piano_drop_speed_entry.get()
            piano_predrop_speed = self.piano_predrop_speed_entry.get()
            piano_begin_speed = self.piano_begin_speed_entry.get()
            contrast_drop_speed = self.contrast_drop_speed_entry.get()
            contrast_predrop_speed = self.contrast_predrop_speed_entry.get()
            contrast_begin_speed = self.contrast_begin_speed_entry.get()
            zoom_drop_speed = self.zoom_drop_speed_entry.get()            
            zoom_predrop_speed = self.zoom_predrop_speed_entry.get()       
            zoom_begin_speed = self.zoom_begin_speed_entry.get()       
            noise_drop_speed = self.noise_drop_speed_entry.get()
            noise_predrop_speed = self.noise_predrop_speed_entry.get()
            noise_begin_speed = self.noise_begin_speed_entry.get()
            other_drop_speed = self.other_drop_speed_entry.get()
            other_predrop_speed = self.other_predrop_speed_entry.get()
            other_begin_speed = self.other_begin_speed_entry.get()
            
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
            if piano_drop_speed:
                cmd.extend(["--piano_drop_speed", piano_drop_speed])          
            if self.drums_begin_speed_entry.get():
                cmd.extend(["--drums_begin_speed", self.drums_begin_speed_entry.get()])
            if self.drums_predrop_speed_entry.get():
                cmd.extend(["--drums_predrop_speed", self.drums_predrop_speed_entry.get()])
            if self.piano_begin_speed_entry.get():
                cmd.extend(["--piano_begin_speed", self.piano_begin_speed_entry.get()])
            if self.piano_predrop_speed_entry.get():
                cmd.extend(["--piano_predrop_speed", self.piano_predrop_speed_entry.get()])
            if self.bass_begin_speed_entry.get():
                cmd.extend(["--bass_begin_speed", self.bass_begin_speed_entry.get()])
            if self.bass_predrop_speed_entry.get():
                cmd.extend(["--bass_predrop_speed", self.bass_predrop_speed_entry.get()])
            if self.zoom_begin_speed_entry.get():
                cmd.extend(["--zoom_begin_speed", self.zoom_begin_speed_entry.get()])
            if self.zoom_predrop_speed_entry.get():
                cmd.extend(["--zoom_predrop_speed", self.zoom_predrop_speed_entry.get()])
            if self.noise_begin_speed_entry.get():
                cmd.extend(["--noise_begin_speed", self.noise_begin_speed_entry.get()])
            if self.noise_predrop_speed_entry.get():
                cmd.extend(["--noise_predrop_speed", self.noise_predrop_speed_entry.get()])
            if self.contrast_begin_speed_entry.get():
                cmd.extend(["--contrast_begin_speed", self.contrast_begin_speed_entry.get()])
            if self.contrast_predrop_speed_entry.get():
                cmd.extend(["--contrast_predrop_speed", self.contrast_predrop_speed_entry.get()])
            if self.strength_begin_speed_entry.get():
                cmd.extend(["--strength_begin_speed", self.strength_begin_speed_entry.get()])
            if self.strength_predrop_speed_entry.get():
                cmd.extend(["--strength_predrop_speed", self.strength_predrop_speed_entry.get()])   						
            if self.other_begin_speed_entry.get():
                cmd.extend(["--other_begin_speed", self.other_begin_speed_entry.get()])
            if self.other_predrop_speed_entry.get():
                cmd.extend(["--other_predrop_speed", self.other_predrop_speed_entry.get()])				
            if noise_drop_speed:
                cmd.extend(["--noise_drop_speed", noise_drop_speed])           
            if contrast_drop_speed:
                cmd.extend(["--contrast_drop_speed", contrast_drop_speed])
                
            self.add_message(f"Executing command: {' '.join(cmd)}", "info")
            logging.info(f"Executing command: {' '.join(cmd)}")

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while True:
                output = process.stdout.readline()
                error_output = process.stderr.readline()

                if output:
                    logging.info(output.strip())
                    self.add_message(output.strip(), "info")
                if error_output:
                    logging.error(f"{error_output.strip()}")
                    self.add_message(error_output.strip(), "error")

                if process.poll() is not None:
                    break

            if process.returncode != 0:
                self.add_message("An error occurred during command execution.", "error")
                logging.error("An error occurred during command execution.")
            else:
                self.add_message("Command executed successfully.", "info")
                logging.info("Command executed successfully.")


        except FileNotFoundError as e:
            self.add_message(f"File not found: {e}", "error")
            logging.error(f"File not found: {e}")
        except subprocess.CalledProcessError as e:
            self.add_message(f"Subprocess failed: {e}", "error")
            logging.error(f"Subprocess failed: {e}")
        except Exception as e:
            self.add_message(f"An unhandled exception occurred: {e}", "error")
            logging.critical(f"An unhandled exception occurred: {e}")

if __name__ == "__main__":
    try:
        logging.info("Inside main...")
        root = ThemedTk(theme="arc")
        root.iconbitmap('./favicon.ico')
        app = AdvancedAudioSplitterUI(root)
        root.mainloop()
    except Exception as e:
        app.add_message(f"An unhandled exception occurred: {e}", "error")
        logging.critical(f"An unhandled exception occurred: {e}")