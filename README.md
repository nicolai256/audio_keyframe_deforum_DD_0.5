# audio to animation keyframes deforum DD
a script that can convert audio to animation keyframes for Deforum Stable Diffusion and Disco Diffusion

the script splits up the audio into different files and makes keyframes from all those files

**dependencies**

```
pip install numpy
pip install loguru
pip install spleeter
pip install librosa
pip install pydub
```

# audio splitter keyframes

**splits the audio and makes keyframes of the splitted files**

```
python audio_splitter_keyframes.py --file audiofile.mp3 --fps 15 --stems 5 --speed 0.4 --zoomspeed 5 --audiostart 1,10 --audioend 2,50
```

```--file``` = the audio file
 
```--fps``` = the fps has to match the fps of the animation you will make

```--stems``` = the amount of splitting to the audio file (--stems 5 = splits your audio file into 5 audio files)

```--speed , --zoomspeed``` = the amplitude / strength / intensity of your animation **keyframes will be exported to keyframes.json**

```--audiostart``` = the start of the audio (use 1,10 for 1 minute 10 seconds)

```--audioend``` = the end of the audio (use 2,50 for 2 minutes 50 seconds)

```--use_vocals``` = only use this if you want to keyframe the vocals too (not recommended)

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

support this and other projects 

[PayPal](https://paypal.me/nicolaivernieuwe?country.x=BE&locale.x=en_US)<br/>

#

special thanks to [Zippy](https://github.com/aredden) for cleaning up this script 
