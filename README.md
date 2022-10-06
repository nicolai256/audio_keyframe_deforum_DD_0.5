# audio to animation keyframes deforum DD [BETA]
a script that can convert audio to animation keyframes for Deforum Stable Diffusion and Disco Diffusion

**this is still in BETA phase so give all the feedback you want to improve this**

the script splits up the audio into different files and makes keyframes from all those files

u can import these generated keyframes into [this blender DSD keyframe plugin](https://www.youtube.com/watch?v=rzGINC9m4FM&ab_channel=Purz) if you want for changing the curves or editing the values visually

**dependencies**

```
pip install numpy
pip install loguru
pip install spleeter
pip install librosa
pip install pydub
```

# advanced audio splitter keyframes

can split, cut or just use files from external splitters

### if using spleeter (built in audio splitter)

basic command example

```python advanced_audio_splitter_keyframes.py -f audio.mp3 --fps 14 --spleeter 1 ```
#

```--spleeter 1``` = use spleeter

```--file audio.mp3/wav``` = the audio file
 
```--fps 14``` = the fps has to match the fps of the animation you will make

```--stems 5``` = the amount of splitting to the audio file (--stems 5 = splits your audio file into 5 audio files)

```--music_cut 1``` = enable music cutting

```--musicstart 1,17``` = the start of the audio (use 1,17 for 1 minute 17 seconds)

```--musicend 2,53``` = the end of the audio (use 2,53 for 2 minutes 53 seconds)

```--zoom_sound bass``` = the sound u want to use for your zoom, choices=['drums', 'other', 'piano','bass']

```--strength_sound bass``` = the sound for your strength schedule, recommended to be the same as zoom sound, choices=['drums', 'other', 'piano','bass']

```--noise_sound bass``` = the sound for your noise schedule, recommended to be the same as zoom sound, choices=['drums', 'other', 'piano','bass']

```--contrast_sound bass``` = the sound for your contrast schedule, recommended to be the same as zoom sound, choices=['drums', 'other', 'piano','bass']

#

### if not using spleeter

spleeter is the best available one that i can easily put in the script 

but if you want higher quality split files i reccomend this program (easy install and free)
https://github.com/Anjok07/ultimatevocalremovergui([https://github.com/Anjok07/ultimatevocalremovergui])

command example

```python advanced_audio_splitter_keyframes.py --fps 14 --drums_audio_path drums.wav --zoom_audio_path bass.wav```

#

```--drums_audio_path drums.wav``` = path to your drums .wav file 

```--piano_audio_path piano.wav``` = path to your piano .wav file 

```--bass_audio_path bass.wav``` = path to your bass .wav file 

```--other_audio_path other.wav``` = path to your other .wav file 

```--zoom_audio_path bass.wav``` = path to your preferred .wav file 

```--strength_audio_path bass.wav``` = path to your preferred .wav file (recommended to be the same as zoom_audio_path

```--noise_audio_path bass.wav``` = path to your preferred .wav file (recommended to be the same as zoom_audio_path

```--contrast_audio_path bass.wav``` = path to your preferred .wav file (recommended to be the same as zoom_audio_path
#

### keyframe values commands, they work in both spleeter and non spleeter

(these values are default in the script, change them if u want to)

#

```--drums_drop_speed 0.2``` = reactive impact of the drums audio on the animation when the audio makes a sound

```--drums_begin_speed 0.0``` = reactive impact of the drums audio on the animation (starting value on keyframe 1)

```--drums_predrop_speed -0.2``` = reactive impact of the drums audio on the animation right before the audio makes a sound
#

```--other_drop_speed 0.4``` = reactive impact of the other audio on the animation when the audio makes a sound

```--other_begin_speed 0.0``` = reactive impact of the other audio on the animation (starting value on keyframe 1)

```--other_predrop_speed -0.4``` = reactive impact of the other audio on the animation right before the audio makes a sound
#

```--piano_drop_speed 0.4``` = reactive impact of the piano audio on the animation when the audio makes a sound

```--piano_begin_speed 0.0``` = reactive impact of the piano audio on the animation (starting value on keyframe 1)

```--piano_predrop_speed -0.4``` = reactive impact of the piano audio on the animation right before the audio makes a sound
#

```--bass_drop_speed 0.4``` = reactive impact of the bass audio on the animation when the audio makes a sound

```--bass_begin_speed 0.0``` = reactive impact of the bass audio on the animation (starting value on keyframe 1)

```--bass_predrop_speed -0.4``` = reactive impact of the bass audio on the animation right before the audio makes a sound
#

```--zoom_drop_speed 5``` = reactive zoom impact of the audio on the animation when the audio makes a sound

```--zoom_begin_speed 0``` = reactive zoom impact of the audio on the animation (starting value on keyframe 1)

```--zoom_predrop_speed 0.5``` = reactive zoom impact of the audio on the animation right before the audio makes a sound
#

```--noise_drop_speed 0.02``` = reactive noise impact of the audio on the animation when the audio makes a sound

```--noise_begin_speed 0.01``` = reactive noise impact of the audio on the animation (starting value on keyframe 1)

```--noise_predrop_speed 0.00``` = reactive noise impact of the audio on the animation right before the audio makes a sound
#

```--contrast_drop_speed 1.01``` = reactive contrast impact of the audio on the animation when the audio makes a sound

```--contrast_begin_speed 0.95``` = reactive contrast impact of the audio on the animation (starting value on keyframe 1)

```--contrast_predrop_speed 0.95``` = reactive contrast impact of the audio on the animation right before the audio makes a sound
#

```--strength_drop_speed 0.50``` = reactive strength impact of the audio on the animation when the audio makes a sound

```--strength_begin_speed 0.60``` = reactive strength impact of the audio on the animation (starting value on keyframe 1)

```--strength_predrop_speed 0.70``` = reactive strength impact of the audio on the animation right before the audio makes a sound

###
#


#

# conditional math synced to BPM

```
python conditional_maths_bpm_keyframes.py --file audiofile.mp3 --fps 14 --intensity 2
```

**keyframes will be exported to conditional_maths_bpm_0.json**

it will look something like this ```0:(2*sin(2*3.14*t/7.17948717948718))```

```--file``` = the audio file
 
```--fps``` = the fps has to match the fps of the animation you will make

```--intensity``` = the amplitude / strength / intensity of your animation

#

# simple audio splitter keyframes

**splits the audio and makes keyframes of the splitted files**

```
python audio_splitter_keyframes.py --file audiofile.mp3 --fps 15 --stems 5 --speed 0.4 --zoomspeed 5 --music_cut 1 --musicstart 1,10 --musicend 2,50
```
**keyframes will be exported to audio_splitter_keyframes.json**

```--file``` = the audio file
 
```--fps``` = the fps has to match the fps of the animation you will make

```--stems``` = the amount of splitting to the audio file (--stems 5 = splits your audio file into 5 audio files)

```--speed , --zoomspeed``` = the amplitude / strength / intensity of your animation

```--music_cut 1``` = enable music cutting

```--musicstart``` = the start of the audio (use 1,17 for 1 minute 17 seconds)

```--musicend``` = the end of the audio (use 2,53 for 2 minutes 53 seconds)

```--use_vocals``` = only use this if you want to keyframe the vocals too (not recommended)

#

# simple audio keyframes

**makes keyframes of the audio fast, good if have your own splitted sounds and don't want to use the advanced version**

```
python audio_keyframes.py --file audiofile.mp3 --fps 15 --speed 0.4 --music_cut true --musicstart 1,10 --musicend 2,50
```
**keyframes will be exported to audio_keyframes.json**

```--file``` = the audio file
 
```--fps``` = the fps has to match the fps of the animation you will make

```--speed``` = the amplitude / strength / intensity of your animation

```--music_cut``` = enable music cutting

```--musicstart``` = the start of the audio (use 1,17 for 1 minute 17 seconds)

```--musicend``` = the end of the audio (use 2,53 for 2 minutes 53 seconds)

#

support this and other projects 

[PayPal](https://paypal.me/nicolaivernieuwe?country.x=BE&locale.x=en_US)<br/>

#

special thanks to [Zippy](https://github.com/aredden) for cleaning up this script 
