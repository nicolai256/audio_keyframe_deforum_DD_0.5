import wave
import json, argparse, subprocess, os
import librosa
import cv2
import numpy as np
from os.path import isfile, join
from os import path
from pydub import AudioSegment

parser = argparse.ArgumentParser(description='Process some integers.')
#logger.info(f"Parsing arguments...")
desc = "Blah"
parser.add_argument("-f", "--file", type=str, help="input audio")
parser.add_argument("--musicstart",default="0,00", type=str, help="start of the music in seconds")
parser.add_argument("--musicend", type=str, help="length of the music in seconds")
args = parser.parse_args()

print('')
print('')
import shutil
filename = args.file

#backup the file

src = args.file
filee, _ = os.path.splitext(filename)
i = 0
flnm = filee + str(i) + "_backup.wav"
while path.exists(flnm) :
    flnm = filee + str(i) + ".wav"
    i += 1
    
shutil.copyfile(src, flnm)    

"""if ":" in args.musicstart:
    txt = args.musicstart
    minute, second = txt.split(":")
    minutes_60 = int(minute) * 60
    time = minutes_60 + second"""
if args.musicstart:
    if "," in args.musicstart:
        txt = args.musicstart
        a_minute = 60
        a_minute = int(a_minute)
        minute, second = txt.split(",")
        minute = int(minute)
        second = int(second)
        minutes_60 = minute * a_minute
        time = minutes_60 + second
        print('converting minutes to seconds')
        #print('music starts at ', args.musicstart ,' = second', time)
if args.musicend: 
    if "," in args.musicend:
        txt = args.musicend
        a_minute = 60
        a_minute = int(a_minute)
        minute, second = txt.split(",")
        minute = int(minute)
        second = int(second)
        minutes_60 = minute * a_minute
        time2 = minutes_60 + second
        #print('music ends at ', args.musicend ,' = second', time2)
    
    
# predict the length of the song
length_of_file = librosa.get_duration(filename=filename)
audio: AudioSegment = AudioSegment.from_file(filename)
audio.duration_seconds == (len(audio) / 1000.0)
minutes_duartion = int(audio.duration_seconds // 60)
minutes_duration = minutes_duartion * 60
seconds_duration = round(audio.duration_seconds % 60)
duration = minutes_duration + seconds_duration

# times between which to extract the wave from
if args.musicstart:
    if "," in args.musicstart:
        start = int(time)
         
    elif "," not in args.musicstart:
        start = int(args.musicstart)
        
else:
    start = "0" 
    
print('music starts at second', start)

if args.musicend:    
    if "," in args.musicend:
        end = int(time2)
    elif "," not in args.musicend:
        end = int(args.musicend)
else:
    end = int(duration) # seconds
print('music ends at second', end)  

      
# file to extract the snippet from
with wave.open(filename, "rb") as infile:
    # get file data
    nchannels = infile.getnchannels()
    sampwidth = infile.getsampwidth()
    framerate = infile.getframerate()
    # set position in wave to start of segment
    infile.setpos(int(start * framerate))
    # extract data
    data = infile.readframes(int((end - start) * framerate))

# write the extracted data to a new file
with wave.open(filename, 'w') as outfile:
    outfile.setnchannels(nchannels)
    outfile.setsampwidth(sampwidth)
    outfile.setframerate(framerate)
    outfile.setnframes(int(len(data) / sampwidth))
    outfile.writeframes(data)

length = int(end - start)
print('')
print('')    
print('your new cropped file is' , length, 'seconds')
print('')
print('') 
print('the name of your new cropped file is', filename, 'and your original non cropped file is', flnm)
print('') 
print('') 