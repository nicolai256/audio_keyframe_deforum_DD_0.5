# audio_keyframe_deforum_DD
a script that can convert audio to keyframes for Deforum Stable Diffusion and Disco Diffusion

dependencies

```
pip install numpy
pip install loguru
pip install spleeter
pip install librosa
pip install pydub
```

make keyframes

```
python audiokeyframes_v0.2.py --file audiofile.mp3 --fps 15 --stems 5 --speed 0.4 --zoomspeed 5
```

special thanks to Zippy for cleaning this script up 
