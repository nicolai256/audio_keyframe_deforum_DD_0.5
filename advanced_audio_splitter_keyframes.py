import json, argparse, subprocess, os
from pydub import AudioSegment
import wave
import os
from os import path
import datetime
import soundfile
import numpy as np
import librosa
import csv
from pydub import AudioSegment
from joblib import Memory
import logging
from scipy import fftpack
from pathlib import Path

# Initialize joblib memory cache
memory = Memory("cache_directory", verbose=0)

@memory.cache
def fft_analysis(y):
    N = len(y)
    T = 1.0 / 800.0
    yf = fftpack.fft(y)
    return np.abs(yf[0:N//2])
    
def parse_args():
    desc = "Blah"

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="input audio")
    
    parser.add_argument("--spleeter", type=str, help="option to cut the music")
    
    parser.add_argument("--music_cut", type=str, help="option to cut the music")
    parser.add_argument("--musicstart", type=str, help="start of the music in seconds")
    parser.add_argument("--musicend", type=str, help="length of the music in seconds")
    
    parser.add_argument("-s", "--fps", type=int, help="frames per second")
    
    parser.add_argument("-t","--stems",type=str,default="5",help="the amount of exported audio files, 3, 4, 5",)
    
    parser.add_argument("--speed",type=float,default="0.4",help="reactive impact of the audio on the animation",)
    parser.add_argument("-z","--zoomspeed",type=float,default="5",help="reactive zoom impact of the audio on the animation",)
       
    parser.add_argument("--use_vocals",type=float,help="vocals seem to have a negative effect on the animation so it's disabled by default",)
    
    #advanced keyframes
    parser.add_argument("--drums_drop_speed",type=float,default="0.2",help="reactive impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--drums_begin_speed",type=float,default="0.0",help="reactive impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--drums_predrop_speed",type=float,default="-0.2",help="reactive impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--other_drop_speed",type=float,default="0.4",help="reactive impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--other_begin_speed",type=float,default="0.0",help="reactive impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--other_predrop_speed",type=float,default="-0.4",help="reactive impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--piano_drop_speed",type=float,default="0.4",help="reactive impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--piano_begin_speed",type=float,default="0.0",help="reactive impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--piano_predrop_speed",type=float,default="-0.4",help="reactive impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--bass_drop_speed",type=float,default="0.4",help="reactive impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--bass_begin_speed",type=float,default="0.0",help="reactive impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--bass_predrop_speed",type=float,default="-0.4",help="reactive impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--zoom_drop_speed",type=float,default="5",help="reactive zoom impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--zoom_begin_speed",type=float,default="0",help="reactive zoom impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--zoom_predrop_speed",type=float,default="0.5",help="reactive zoom impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--noise_drop_speed",type=float,default="0.02",help="reactive noise impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--noise_begin_speed",type=float,default="0.01",help="reactive noise impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--noise_predrop_speed",type=float,default="0.00",help="reactive noise impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--contrast_drop_speed",type=float,default="1.01",help="reactive contrast impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--contrast_begin_speed",type=float,default="0.95",help="reactive contrast impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--contrast_predrop_speed",type=float,default="0.95",help="reactive contrast impact of the audio on the animation right before the audio makes a sound",)
    
    parser.add_argument("--strength_drop_speed",type=float,default="0.50",help="reactive image strength impact of the audio on the animation when the audio makes a sound",)
    parser.add_argument("--strength_begin_speed",type=float,default="0.60",help="reactive image strength impact of the audio on the animation (starting value on keyframe 1)",)
    parser.add_argument("--strength_predrop_speed",type=float,default="0.70",help="reactive image strength impact of the audio on the animation right before the audio makes a sound",)
        
    #if using --spleeter
    parser.add_argument("--zoom_sound", type=str, default='bass', choices=['drums', 'other', 'piano','bass'])
    parser.add_argument("--strength_sound", type=str, default='bass', choices=['drums', 'other', 'piano','bass'])
    parser.add_argument("--noise_sound", type=str, default='bass', choices=['drums', 'other', 'piano','bass'])
    parser.add_argument("--contrast_sound", type=str, default='bass', choices=['drums', 'other', 'piano','bass'])
    
    #if not using spleeter and input external audio files
    parser.add_argument("--drums_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--other_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--piano_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--bass_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--zoom_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--strength_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--noise_audio_path", type=str,help="path to your .wav file")
    parser.add_argument("--contrast_audio_path", type=str,help="path to your .wav file")
   
    args = parser.parse_args()
    return args

args = parse_args()
if args.spleeter:
    if args.music_cut:
        print('')
        print('')
        import shutil
        
        src = args.file
        if src.endswith('.wav'):
            filee, _ = os.path.splitext(src)
            i = 0
            flnm = filee + str(i) + "_cut.wav"
            while path.exists(flnm) :
                flnm = filee + str(i) + "_cut.wav"
                i += 1
        elif src.endswith('.mp3'):
            filee, _ = os.path.splitext(src)
            i = 0
            flnm = filee + str(i) + "_cut.wav"
            while path.exists(flnm) :
                flnm = filee + str(i) + "_cut.wav"
                i += 1
                
            src = args.file
            dst = flnm

            # convert wav to mp3                                                            
            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")   
        
        result = []
        filename = flnm
        file = flnm

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
            
        # predict the length of the song
        length_of_file = librosa.get_duration(path=filename)
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

        with wave.open(filename, "rb") as infile:
            # get file data
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            # set position in wave to start of segment
            infile.setpos(int(start * framerate))
            # extract data
            data = infile.readframes(int((int(end) - int(start)) * int(framerate)))

        with wave.open(flnm, 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)
        
        length = int(int(end) - int(start))
  
        print('your new cropped file is' , length, 'seconds')

        print('the name of your new cropped file is', flnm, 'and your original non cropped file is', args.file)

    else:
        flnm = args.file
        filename = flnm

        print('audio not cropped')  
             
class AudioKeyframeMeta:
    def __init__(self, duration, length_of_file, bpm=None) -> None:
        self.duration = duration
        self.length_of_file = length_of_file
        self.bpm = bpm

class AudioKeyframeService:
    def __init__(
        self, key_names=["bass", "drums", "other", "piano", "vocals"], fps: float = 24
    ) -> None:
        self.key_names = key_names
        self.fps = fps
            
    def bpmdetection(self, filename):
        try:
            y, sr = librosa.load(filename, sr=None)
            
            fft_result = fft_analysis(y)
            
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            
            tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
            
            if tempo <= 0:
                logging.error("Error: BPM detected as zero or negative.")
                return None
            
            print(f"BPM: {tempo:.2f}")
            
            with open("bpm.json", "w") as fp:
                json.dump(tempo, fp)
                print("Processing of the BPM succeeded and exported to bpm.json")
            
            return float(tempo)
        
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def detect_bpm(self, filename):
        tempo = self.bpmdetection(filename)
        return tempo

    def _get_metadata(self, filename):
        length_of_file = librosa.get_duration(path=filename)
        audio: AudioSegment = AudioSegment.from_file(filename)
        
        duration_seconds = len(audio) / 1000.0
        
        minutes_duartion = int(duration_seconds // 60)
        minutes_duration = minutes_duartion * 60
        seconds_duration = round(duration_seconds % 60)
        duration = minutes_duration + seconds_duration
        
        bpm = self.detect_bpm(filename)
        
        return AudioKeyframeMeta(
            duration=duration, length_of_file=length_of_file, bpm=bpm
        )

    def _spleet(self, stems_dir, file, nstem):
        args = parse_args()
        if args.spleeter:
            if not args.use_vocals:
                stemsnum = int(args.stems) - 1
            else:
                stemsnum = args.stems
            print('starting spleeter, splitting your audio into', stemsnum,'pieces')
            print('') 
            print('')
            subprocess.run(["spleeter", "separate", "-p", f"spleeter:{nstem}stems", "-o", f"{stems_dir}/", file,])

    def process(
        self,
        n_stems: int,
        file,
        stems_dir="outputs",
        use_vocals=False,
        zoomspeed=4,
        speed=4,
        args=None
    ):
        if args is None:
            args = parse_args()
            
        filedircalc = Path(file).stem
        stems_dir = Path(stems_dir)
        
        if args.spleeter:
            self._spleet(stems_dir, file, n_stems)
            
            vocals_path = stems_dir / filedircalc / "vocals.wav"
            if not use_vocals and vocals_path.exists():
                vocals_path.unlink()
        
        print("\n" * 2)
        print("Starting audio keyframe maker")
        print("\n" * 2)
        
        final_dict = {}
        basic_sound_types = ["other", "piano", "drums", "bass"]
        special_sound_types = ["zoom", "strength", "noise", "contrast"]
        
        for sound_type in basic_sound_types:
            sound_file_path = stems_dir / filedircalc / f"{sound_type}.wav"
            
            if sound_file_path.exists():
                process_function = getattr(self, f"_process_{sound_type}")
                try:
                    final_dict[sound_type] = process_function(str(sound_file_path), zoomspeed=zoomspeed)
                except Exception as e:
                    logging.error(f"Error processing {sound_type}: {e}")

        for sound_type in special_sound_types:
            sound_file_path = getattr(args, f"{sound_type}_sound", None)
            if sound_file_path:
                sound_file_path = stems_dir / filedircalc / f"{sound_file_path}.wav"
                if sound_file_path.exists():
                    process_function = getattr(self, f"_process_{sound_type}")
                    try:
                        final_dict[sound_type] = process_function(str(sound_file_path), zoomspeed=zoomspeed)
                    except Exception as e:
                        logging.error(f"Error processing {sound_type}: {e}")

        # Output the final_dict to a single JSON file
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"audio_splitter_keyframes_{current_datetime}.json"
        output_filepath = os.path.join("outputs", output_filename)
        
        with open(output_filepath, "w") as fp:
            json.dump(final_dict, fp, indent=2)
            
        print(f"Processing of the keyframes succeeded and exported to {output_filepath}")

    def _process_piano(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} for piano animation with speed: {args.piano_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.piano_begin_speed
        beat_transition_value = args.piano_drop_speed
        pre_beat_transition__value = args.piano_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )
    
    def _process_bass(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} for bass animation with speed: {args.bass_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.bass_begin_speed
        beat_transition_value = args.bass_drop_speed
        pre_beat_transition__value = args.bass_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )
    
    def _process_other(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} for other audio animation with speed: {args.other_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.other_begin_speed
        beat_transition_value = args.other_drop_speed
        pre_beat_transition__value = args.other_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )

    def _process_drums(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} for drums animation with speed: {args.drums_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.drums_begin_speed
        beat_transition_value = args.drums_drop_speed
        pre_beat_transition__value = args.drums_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )
        
    def _process_zoom(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} with zoom schedule: {args.zoom_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.zoom_begin_speed
        beat_transition_value = args.zoom_drop_speed
        pre_beat_transition__value = args.zoom_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )
    def _process_strength(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} with strength schedule: {args.strength_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.strength_begin_speed
        beat_transition_value = args.strength_drop_speed
        pre_beat_transition__value = args.strength_predrop_speed 
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )
    def _process_noise(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} with noise schedule: {args.noise_drop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.noise_begin_speed
        beat_transition_value = args.noise_drop_speed
        pre_beat_transition__value = args.noise_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )
    def _process_contrast(self, filename, zoomspeed=4):
        args = parse_args()
        logging.info(f"Processing file: {filename} with contrast schedule: {args.contrast_predrop_speed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = args.contrast_begin_speed
        beat_transition_value = args.contrast_drop_speed
        pre_beat_transition__value = args.contrast_predrop_speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )

    def _get_prep_values(self, filename, duration)-> np.ndarray:
        x, sr = librosa.load(filename)
        onset_frames = librosa.onset.onset_detect(
            y=x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1
        )
        onset_times = librosa.frames_to_time(onset_frames)
        total_lin_step = duration * self.fps
        vals, _ = np.histogram(
            onset_times, bins=total_lin_step, range=(0, duration)
        )
        beat_ind = np.argwhere(vals)
        return beat_ind
 
    def _build_string(
        self,
        beat_ind,
        key_frame_value,
        post_beat,
        post_beat_transition__value,
        pre_beat_transition__value,
        beat_transition_value,
        frames_change_post_beat,
        frames_change_pre_beat,
    ):
        for i in range(len(beat_ind)):
            # logging.info()
            if post_beat < beat_ind[i]:
                post_tup = (post_beat, post_beat_transition__value)
                key_frame_value.append(post_tup)
                # logging.info(f"{i}  beat_ind[i]: {beat_ind[i]}, post {post_tup}")
            pre = (beat_ind[i] - frames_change_pre_beat - 1)[0]
            if (
                len(key_frame_value) == 0
                or len(key_frame_value) != 0
                and key_frame_value[-1][0] != pre
            ):
                # logging.info(f"{i}  beat_ind[i]: {beat_ind[i]}, pre {pre, 0}")
                key_frame_value.append((pre, pre_beat_transition__value))
            beat = beat_ind[i][0]
            # logging.info(f"{i}  beat_ind[i]: {beat_ind[i]}, beat {beat, beat_transition_value}")
            key_frame_value.append((beat, beat_transition_value))
            post_beat = (beat_ind[i] + (frames_change_post_beat))[0]
        string_list = []
        for key_frame, val in key_frame_value:
            string = f"{key_frame}:({val}),"
            string_list.append(string)
            
        #space = f"/n"
        #string_list.append(space)
        key_frame_string = "".join(string_list)
        key_frame_string = key_frame_string[:-1]
        return key_frame_string

    def _process_file(self, filename, speed=5):
        logging.info(f"Processing file: {filename} with speed: {speed}")
        meta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 1000  # there are the amount of buffer frames before and after a beat to let value linear change
        post_beat_transition__value = speed / 2
        beat_transition_value = speed
        pre_beat_transition__value = -speed
        key_frame_value = []
        post_beat = 1
        return self._build_string(
            beat_ind,
            key_frame_value,
            post_beat,
            post_beat_transition__value,
            pre_beat_transition__value,
            beat_transition_value,
            frames_change_post_beat,
            frames_change_pre_beat,
        )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    service = AudioKeyframeService(fps=args.fps)

    if not os.path.exists("outputs"):
        os.mkdir("outputs")

    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"audio_splitter_keyframes_{current_datetime}.json"

    output_filepath = os.path.join("outputs", output_filename)

    if args.spleeter:
        if args.music_cut:
            final_dict = service.process(args.stems, args.file, zoomspeed=args.zoomspeed, speed=args.speed)
        else:
            final_dict = service.process(args.stems, args.file, zoomspeed=args.zoomspeed, speed=args.speed)
    else:

        final_dict = service.process(args.stems, file="do_not_delete.wav", zoomspeed=args.zoomspeed, speed=args.speed)

    with open(output_filepath, "w") as fp:
        json.dump(final_dict, fp, indent=2)
        print(f"Processing of the keyframes succeeded and exported to {output_filepath}")