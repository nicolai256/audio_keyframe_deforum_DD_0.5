import argparse
import json
import librosa
import cv2
import numpy as np
import os
from os.path import isfile, join
import os.path as pth

parser = argparse.ArgumentParser(description='Feature Extraction From MP3')

parser.add_argument('--file', type=str,help='your audio file')
parser.add_argument("-s", "--fps", type=str, help="frames per second")
parser.add_argument("--intensity", type=str, help="intensity of the keyframe")

args = parser.parse_args()


filename = args.file
    
y, sr = librosa.load(filename)
    
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
print ('bpm: {:.5f}'.format(tempo))

tempo1 = '{:.5f}'.format(tempo)
#tempo.dtypes.head()
#data = tempo
#with open("bpm.json", "w") as fp2:
#    json.dump(tempo, fp2)
#    print("processing of the bpm succeeded and exported to bpm.json")


fps = args.fps
bpm = tempo1

x = int(fps) * 60 / int(float(bpm))
value = args.intensity
export = '0:('+str(value)+'*sin(2*3.14*t/'+str(x)+'))'


from os import path
import os

i = 0
flnm = "conditional_maths_bpm_" + str(i) + ".json"
while path.exists(flnm) :
    flnm = "conditional_maths_bpm_" + str(i) + ".json"
    i += 1

with open(flnm , "w") as fp:
        
        json.dump(export, fp)
        
        print(export)
        print("processing of the keyframes succeeded and exported to " "conditional_maths_bpm_" + str(i) + ".json")
