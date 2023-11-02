# ![AKD Logo](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/8752374b-6e74-46cf-b625-fbd58216f525) Audio Keyframes for Deforum (GUI) 🎵
![Version](https://img.shields.io/badge/version-1.0.5-lightgreen.svg)
![Last Commit](https://img.shields.io/github/last-commit/FeelTheFonk/AudioKeyframeDeforum_GUI.svg)
![Open Issues](https://img.shields.io/github/issues-raw/FeelTheFonk/AudioKeyframeDeforum_GUI.svg)
![Closed Issues](https://img.shields.io/github/issues-closed-raw/FeelTheFonk/AudioKeyframeDeforum_GUI.svg)
![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)
![Star](https://img.shields.io/github/stars/FeelTheFonk/AudioKeyframeDeforum_GUI.svg?style=social)
![Fork](https://img.shields.io/github/forks/FeelTheFonk/AudioKeyframeDeforum_GUI.svg?style=social)
![Watch](https://img.shields.io/github/watchers/FeelTheFonk/AudioKeyframeDeforum_GUI.svg?style=social)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Elevate Your Deforum Projects to Unprecedented Heights

Achieve unparalleled precision in your Deforum projects with Audio Keyframes for Deforum (GUI). This tool enables you to dissect audio files into multiple stems and construct highly intricate keyframes for your animations.

Original project forked from [Audio Keyframe Deforum](https://github.com/nicolai256/audio_keyframe_deforum_DD_0.5).

![image](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/d073730c-5761-4ba1-8484-85239ec62b5c)


## 🚀 Quick Start 🚀

To initiate your journey toward unparalleled project excellence, execute the following command:

```bash
launch.bat
```

This single command sets up a virtual environment and kickstarts the GUI for a seamless experience.

---

## 🛠 Dependencies 🛠

```
- numpy
- ttkthemes
- spleeter
- librosa
- pydub
- mpmath
- joblib
```
---

### ➕ Conditional Maths Synced to BPM ➕

![image](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/01e4a289-2f01-4c66-8617-fc22d3532aec)

#### 🌐 Overview

Unearth the zenith of animation synchronization by leveraging our sophisticated mathematical algorithms. These algorithms are precisely tailored to sync with the beat per minute (BPM) of your audio file, offering a seamless and dynamic animation experience.

#### 🧠 What's Under the Hood?

The feature uses Fast Fourier Transform (FFT) for frequency analysis and utilizes diverse mathematical functions such as sine, cosine, and Fourier transformations. Thanks to these, your keyframes will not just be in sync with the audio but will embody the rhythm and mood of it.

#### 📐 **Available Functions for Keyframe Generation**

Here's a comprehensive guide to each mathematical function available for keyframe generation, complete with their respective visual representations and impacts on motion or camera dynamics.

- **Sine Function (`sine`)**
  
  - **Expression**: `D + A*sin(2*PI*t/x/P)`
  
  - **Motion Impact**: Generates smooth, oscillating movements that rise and fall in a sinusoidal pattern. Ideal for creating natural, flowing motions like waves.
![Sine_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/ffabf053-f03c-417e-8dde-ce800b8ead18)
---

- **Cosine Function (`cosine`)**

  - **Expression**: `D + A*cos(2*PI*t/x/P)`
  
  - **Motion Impact**: Similar to the sine function but starts at its peak, providing a phase-shifted oscillation. Useful for motions that need to start at a peak or valley.
![Cosine_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/3be028e1-f78a-4105-baa8-e53480c9b0ea)
---

- **Absolute Sine Function (`abs_sin`)**

  - **Expression**: `A - (abs(sin(10*t/P))*B)`

  - **Motion Impact**: Produces oscillations that are always positive, giving a 'bouncing' effect. Great for motions that should not cross a certain threshold.
![Absolute_Sine_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/4e731090-51dc-4179-a5d6-3fcef66e9841)
---

- **Absolute Cosine Function (`abs_cos`)**

  - **Expression**: `A - (abs(cos(10*t/P))*B)`
  
  - **Motion Impact**: Similar to Absolute Sine but starts at its lowest point. Useful for motions like heartbeats that start slow and then rise quickly.
![Absolute_Cosine_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/f8a5ffc3-1726-43ed-8052-19875a469ba1)
---

- **Modulus Function (`modulus`)**

  - **Expression**: `A*(t%P)+D`
  
  - **Motion Impact**: Produces a sawtooth wave, ideal for creating abrupt, repetitive motions like a ticking clock.
![Modulus_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/6dcf8c91-a395-4cbd-8b66-7cf3b700ba4c)
---

- **Linear Function (`linear`)**

  - **Expression**: `A*t+D`
  
  - **Motion Impact**: Generates a straight line, which is useful for constant-speed motion in one direction.
![Linear_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/26930f16-a3cb-494c-b0f4-5478e5c4df38)
---

- **Triangle Function (`triangle`)**

  - **Expression**: `(2 + 2*A)/3.14*arcsin(sin((2*3.14)/P*t))`
  
  - **Motion Impact**: Creates a triangular wave for motions that have sharp peaks and valleys, such as a bouncing ball hitting the ground and rising sharply.
![Triangle_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/8e09e32a-c68f-42b1-aa5d-b2ae6b81a08f)
---

- **Fourier Function (`fourier`)**

  - **Expression**: `D + (A*(sin*t/P)+sin(A*t/P) + sin(A*t/P))`
  
  - **Motion Impact**: Generates complex, layered oscillations by summing multiple sine waves. Ideal for intricate, multi-layered motions like spirals.
![Fourier_Function](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/1d8aa29c-28d8-4d0d-9520-2be873ce1384)
---


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

#### 🎛 Parameters

For those who demand the highest quality Audio Split, consider using [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui).

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
- `--drums_audio_path drums.wav`: Specify the drums audio file.
- `--piano_audio_path piano.wav`: Specify the piano audio file.
- `--bass_audio_path bass.wav`: Specify the bass audio file.
- `--other_audio_path other.wav`: Specify other types of audio files.
- `--zoom_audio_path bass.wav`: Specify the zoom audio file.
- `--drums_drop_speed 0.2`: Set the reactive impact of drums.
- `--drums_begin_speed 0.0`: Set the starting keyframe value for drums.
- `--drums_predrop_speed -0.2`: Set the pre-impact value for drums.
- `--other_drop_speed 0.4`: Set the reactive impact of other audio.
- `--other_begin_speed 0.0`: Set the starting keyframe value for other audio.
- `--other_predrop_speed -0.4`: Set the pre-impact value for other audio.
- `--piano_drop_speed 0.4`: Set the reactive impact of piano audio.
- `--piano_begin_speed 0.0`: Set the starting keyframe value for piano audio.
- `--piano_predrop_speed -0.4`: Set the pre-impact value for piano audio.
- `--contrast_drop_speed 0.4`: Set the reactive impact of constrat.
- `--constrast_begin_speed 0.0`: Set the starting keyframe value for constrast
- `--constrast_predrop_speed -0.4`: Set the pre-impact value for constrast.
---
