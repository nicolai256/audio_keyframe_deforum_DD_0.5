## ![AKD](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/8752374b-6e74-46cf-b625-fbd58216f525) Audio Keyframes for Deforum (GUI) 🎵

Elevate your Deforum projects with pinpoint accuracy. This script allows you to dissect audio files into multiple stems and generate keyframes for intricate animations. Forked from: [Audio Keyframe Deforum](https://github.com/nicolai256/audio_keyframe_deforum_DD_0.5).
![image](https://github.com/FeelTheFonk/AudioKeyframeDeforum_GUI/assets/134219563/ca80efbd-5eb0-4ec7-8a66-c8236529334c)


## 🚀 Quick Start 🚀

To get started, simply run:

```
launch.bat
```

This will automatically set up a virtual environment and launch the GUI.


## 🛠 Dependencies 🛠

- numpy
- ttkthemes
- spleeter
- librosa
- pydub
- mpmath
- joblib

## 🎚 Features 🎚

### 📦 Spleeter (Built-in Audio Splitter)

Easily split audio files into multiple stems using the integrated Spleeter tool.

🔧 **Example Command**

```bash
python advanced_audio_splitter_keyframes.py -f audio.mp3 --fps 14 --spleeter 1
```

#### 🎛 Parameters

- `--spleeter 1`: Enables Spleeter for audio splitting.
- `--file audio.mp3/wav`: Specifies the audio file to process.
- `--fps 14`: Sets the frame rate to match your target animation.
- `--stems 5`: Sets the number of audio stems to create.
- `--music_cut 1`: Enables audio trimming.
- `--musicstart 1,17`: Sets the start time (1 minute 17 seconds).
- `--musicend 2,53`: Sets the end time (2 minutes 53 seconds).
- `--zoom_sound bass`: Sets the sound type for zoom effects.
- `--strength_sound bass`: Sets the sound type for strength effects.
- `--noise_sound bass`: Sets the sound type for noise effects.
- `--contrast_sound bass`: Sets the sound type for contrast effects.
  

### 🎶 Non-Spleeter Option 🎶

For even higher quality, consider using [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui).

🔧 **Example Command**

```bash
python advanced_audio_splitter_keyframes.py --fps 14 --drums_audio_path drums.wav --zoom_audio_path bass.wav
```

#### 🎛 Parameters

- `--drums_audio_path drums.wav`: Specifies the path to your drums audio file.
- `--piano_audio_path piano.wav`: Specifies the path to your piano audio file.
- `--bass_audio_path bass.wav`: Specifies the path to your bass audio file.
- `--other_audio_path other.wav`: Specifies the path to your other audio file.
- `--zoom_audio_path bass.wav`: Specifies the path to your preferred zoom audio file.


### 📈 Keyframe Values 📈

#### 🔧 Example Values

- `--drums_drop_speed 0.2`: Reactive impact of drums when the audio makes a sound.
- `--drums_begin_speed 0.0`: Starting value on keyframe 1 for drums.
- `--drums_predrop_speed -0.2`: Reactive impact right before the audio makes a sound for drums.
- `--other_drop_speed 0.4`: Reactive impact of other audio when it makes a sound.
- `--other_begin_speed 0.0`: Starting value on keyframe 1 for other audio.
- `--other_predrop_speed -0.4`: Reactive impact right before the audio makes a sound for other audio.
- `--piano_drop_speed 0.4`: Reactive impact of piano audio when it makes a sound.
- `--piano_begin_speed 0.0`: Starting value on keyframe 1 for piano audio.
- `--piano_predrop_speed -0.4`: Reactive impact right before the audio makes a sound for piano audio.


### ➕ More Features ➕

- 🔣 Conditional Maths Synced to BPM
- 🎧 Simple Audio Splitter Keyframes
- 🎤 Simple Audio Keyframes

#### 🔣 Conditional Maths Synced to BPM

Generate keyframes that are perfectly synced to the beat per minute (BPM) of your audio file.

🔧 **Example Command**

```bash
python conditional_maths_bpm_keyframes.py --file audiofile.mp3 --fps 14 --intensity 2
```

🎛 **Parameters**

- `--file`: Specifies the audio file for BPM calculations.
- `--fps`: Frame rate to match your target animation.
- `--intensity`: Amplitude/strength/intensity of your BPM-based animation.

#### 🎧 Simple Audio Splitter Keyframes

A simplified script for splitting audio and generating keyframes.

🔧 **Example Command**

```bash
python audio_splitter_keyframes.py --file audiofile.mp3 --fps 15 --stems 5 --speed 0.4 --zoomspeed 5 --music_cut 1 --musicstart 1,10 --musicend 2,50
```

🎛 **Parameters**

- `--file`: Specifies the audio file to process.
- `--fps`: Frame rate to match your target animation.
- `--stems`: The number of audio stems to create.
- `--speed, --zoomspeed`: Amplitude/strength/intensity of your animation.
- `--music_cut 1`: Enables audio trimming.
- `--musicstart`: Sets the start time for the audio.
- `--musicend`: Sets the end time for the audio.

#### 🎤 Simple Audio Keyframes

Ideal if you already have your own split audio files and want a quick and simple keyframe generation.

🔧 **Example Command**

```bash
python audio_keyframes.py --file audiofile.mp3 --fps 15 --speed 0.4 --music_cut true --musicstart 1,10 --musicend 2,50
```

🎛 **Parameters**

- `--file`: Specifies the audio file to process.
- `--fps`: Frame rate to match your target animation.
- `--speed`: Amplitude/strength/intensity of your animation.
- `--music_cut`: Enables audio trimming.
- `--musicstart`: Sets the start time for the audio.
- `--musicend`: Sets the end time for the audio.

#
