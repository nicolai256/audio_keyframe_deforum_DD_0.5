# ![AKD Logo](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/8752374b-6e74-46cf-b625-fbd58216f525) Audio Keyframes for Deforum (GUI) 🎵
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/FeelTheFonk/AudioKeyframeDeforum_GUI.svg)
![Open Issues](https://img.shields.io/github/issues-raw/FeelTheFonk/AudioKeyframeDeforum_GUI.svg)
![Closed Issues](https://img.shields.io/github/issues-closed-raw/FeelTheFonk/AudioKeyframeDeforum_GUI.svg)
![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)
![Star](https://img.shields.io/github/stars/FeelTheFonk/AudioKeyframeDeforum_GUI.svg?style=social)
![Fork](https://img.shields.io/github/forks/FeelTheFonk/AudioKeyframeDeforum_GUI.svg?style=social)
![Watch](https://img.shields.io/github/watchers/FeelTheFonk/AudioKeyframeDeforum_GUI.svg?style=social)

## Elevate Your Deforum Projects to Unprecedented Heights

Achieve unparalleled precision in your Deforum projects with Audio Keyframes for Deforum (GUI). This powerful tool enables you to dissect audio files into multiple stems and construct highly intricate keyframes for your animations.

Original project forked from [Audio Keyframe Deforum](https://github.com/nicolai256/audio_keyframe_deforum_DD_0.5).

![Screenshot](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/9dbb6b57-c30d-4bdf-b2a0-f4c7cdda7e2b)


## 🚀 Quick Start 🚀

To initiate your journey toward unparalleled project excellence, execute the following command:

```bash
launch.bat
```

This single command sets up a virtual environment and kickstarts the GUI for a seamless experience.

---

## 🛠 Dependencies 🛠

Ensure you have the following Python packages installed or simply run `pip install -r requirements.txt`:

- numpy
- ttkthemes
- spleeter
- librosa
- pydub
- mpmath
- joblib

---

## 🎚 Features 🎚

### 📦 Spleeter (Built-in Audio Splitter)

Unveil the layers of your audio files by leveraging the power of the integrated Spleeter tool.

**🔧 Example Command**

```bash
python advanced_audio_splitter_keyframes.py -f audio.mp3 --fps 14 --spleeter 1
```

#### 🎛 Parameters

- `--spleeter 1`: Activate Spleeter for audio dissection.
- `--file audio.mp3/wav`: Choose the audio file to dissect.
- `--fps 14`: Align the frame rate with your target animation.
- `--stems 5`: Determine the number of audio stems to generate.
- `--music_cut 1`: Enable audio trimming.
- `--musicstart 1,17`: Specify the start time (1 minute 17 seconds).
- `--musicend 2,53`: Specify the end time (2 minutes 53 seconds).
- `--zoom_sound bass`: Choose the sound type for zoom effects.
- `--strength_sound bass`: Choose the sound type for strength effects.
- `--noise_sound bass`: Choose the sound type for noise effects.
- `--contrast_sound bass`: Choose the sound type for contrast effects.

---

### 🎶 Non-Spleeter Option 🎶

For those who demand the highest quality, consider using [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui).

**🔧 Example Command**

```bash
python advanced_audio_splitter_keyframes.py --fps 14 --drums_audio_path drums.wav --zoom_audio_path bass.wav
```

#### 🎛 Parameters

- `--drums_audio_path drums.wav`: Specify the drums audio file.
- `--piano_audio_path piano.wav`: Specify the piano audio file.
- `--bass_audio_path bass.wav`: Specify the bass audio file.
- `--other_audio_path other.wav`: Specify other types of audio files.
- `--zoom_audio_path bass.wav`: Specify the zoom audio file.

---

### 📈 Keyframe Values 📈

#### 🔧 Example Values

- `--drums_drop_speed 0.2`: Set the reactive impact of drums.
- `--drums_begin_speed 0.0`: Set the starting keyframe value for drums.
- `--drums_predrop_speed -0.2`: Set the pre-impact value for drums.
- `--other_drop_speed 0.4`: Set the reactive impact of other audio.
- `--other_begin_speed 0.0`: Set the starting keyframe value for other audio.
- `--other_predrop_speed -0.4`: Set the pre-impact value for other audio.
- `--piano_drop_speed 0.4`: Set the reactive impact of piano audio.
- `--piano_begin_speed 0.0`: Set the starting keyframe value for piano audio.
- `--piano_predrop_speed -0.4`: Set the pre-impact value for piano audio.

---

### ➕ Conditional Maths Synced to BPM ➕

![image](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/01e4a289-2f01-4c66-8617-fc22d3532aec)

#### 🌐 Overview

Unearth the zenith of animation synchronization by leveraging our sophisticated mathematical algorithms. These algorithms are precisely tailored to sync with the beat per minute (BPM) of your audio file, offering a seamless and dynamic animation experience.

#### 🧠 What's Under the Hood?

The feature uses Fast Fourier Transform (FFT) for frequency analysis and utilizes diverse mathematical functions such as sine, cosine, and Fourier transformations. Thanks to these, your keyframes will not just be in sync with the audio but will embody the rhythm and mood of it.

#### 🔧 **Example Command**

```bash
python conditional_maths_bpm_keyframes.py --file audiofile.mp3 --fps 14 --intensity 2 --function_type sine --advanced_params "A=2,P=3,D=4"
```

#### 🎛 **Parameters**

- `--file`: The audio file whose BPM will serve as the synchronization baseline.
- `--fps`: Frame rate to synchronize with your targeted animation speed.
- `--intensity`: The amplitude, strength, or intensity of your BPM-tailored keyframes.
- `--function_type`: The type of mathematical function to be used for keyframe generation. Options are 'sine', 'cosine', 'abs_sin', 'abs_cos', 'modulus', 'linear', 'triangle', and 'fourier'.
- `--advanced_params`: A comma-separated list of advanced parameters for the chosen function, formatted as "A=2,P=3,D=4".
- `--export-all-formulas`: An optional flag to export all possible formulas based on the provided parameters to a JSON file.

#### 📊 **Advanced Parameters**

These are parameters for fine-tuning the mathematical functions:

- `A`: Amplitude of the function.
- `P`: Period of the function.
- `D`: Vertical shift of the function.
- `B`: Magnitude for absolute value functions.

#### 📜 **Exported JSON Structure**

The exported JSON will contain the following keys:

- `expression`: The generated mathematical expression for keyframes.
- `complex_expression`: The complex mathematical expression if any advanced parameters are used.
- `all_formulas`: A dictionary of all possible formulas if `--export-all-formulas` is used.

---
