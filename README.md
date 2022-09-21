# audio_keyframe_deforum_DD
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

**make keyframes**

```
python audiokeyframes_v0.2.py --file audiofile.mp3 --fps 15 --stems 5 --speed 0.4 --zoomspeed 5
```

**keyframes will be exported to keyframes.json**

#

support this and other projects 

[PayPal](https://paypal.me/nicolaivernieuwe?country.x=BE&locale.x=en_US)<br/>

#

special thanks to [Zippy](https://github.com/aredden) for cleaning up this script 
