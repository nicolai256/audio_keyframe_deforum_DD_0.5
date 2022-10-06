# dependencies
#pip install numpy
#pip install loguru
#pip install spleeter
#pip install librosa
#pip install pydub

#strength schedule and noise schedule linked to zoom

from loguru import logger
import json, argparse, subprocess, os

from pydub import AudioSegment
import wave
from os import path
import soundfile

# keyframes
import numpy as np
import librosa
import csv

from pydub import AudioSegment

def parse_args():
    #logger.info(f"Parsing arguments...")
    desc = "Blah"

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="input audio")
    
    parser.add_argument("--spleeter", type=str, help="option to cut the music")
    
    parser.add_argument("--music_cut", type=str, help="option to cut the music")
    parser.add_argument("--musicstart", type=str, help="start of the music in seconds")
    parser.add_argument("--musicend", type=str, help="length of the music in seconds")
    
    parser.add_argument("-s", "--fps", type=int, help="frames per second")
    
    parser.add_argument("-t","--stems",type=str,default="5",help="the amount of exported audio files, 3, 4, 5",)
    
    #not important in this script, will fix soon
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

#def music_cut():
args = parse_args()
if args.spleeter:
    if args.music_cut:
        print('')
        print('')
        import shutil
        #filename = args.file
        
        #backup the file
        
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
        #result.append(flnm)
        file = flnm
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
        
        #fix wave.Error: file does not start with RIFF id
        """data, samplerate = soundfile.read(filename)
        soundfile.write(filename, data, samplerate)"""
              
        # file to extract the snippet from
        with wave.open(filename, "rb") as infile:
            # get file data
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            # set position in wave to start of segment
            infile.setpos(int(start * framerate))
            # extract data
            data = infile.readframes(int((int(end) - int(start)) * int(framerate)))
        
        # write the extracted data to a new file
        with wave.open(flnm, 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)
        
        length = int(int(end) - int(start))
        print('')
        print('')    
        print('your new cropped file is' , length, 'seconds')
        print('')
        print('') 
        print('the name of your new cropped file is', flnm, 'and your original non cropped file is', args.file)
        print('') 
        print('') 
    else:
        flnm = args.file
        filename = flnm
        print('') 
        print('')
        print('audio not cropped')  
        print('') 
        print('')        
        

#music_cut()
class AudioKeyframeMeta:
    def __init__(self, duration, length_of_file) -> None:
        self.duration = duration
        self.length_of_file = length_of_file


class AudioKeyframeService:
    def __init__(
        self, key_names=["bass", "drums", "other", "piano", "vocals"], fps: float = 24
    ) -> None:
        self.key_names = key_names
        self.fps = fps

    def _get_metadata(self, filename):
        length_of_file = librosa.get_duration(filename=filename)
        audio: AudioSegment = AudioSegment.from_file(filename)
        audio.duration_seconds == (len(audio) / 1000.0)
        minutes_duartion = int(audio.duration_seconds // 60)
        minutes_duration = minutes_duartion * 60
        seconds_duration = round(audio.duration_seconds % 60)
        duration = minutes_duration + seconds_duration
        return AudioKeyframeMeta(
            **{"duration": duration, "length_of_file": length_of_file}
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
    ):
        args = parse_args()
        if args.spleeter:
            if stems_dir.endswith("/"):
                stems_dir = stems_dir[:-1]

            self._spleet(stems_dir, file, n_stems)
            if not use_vocals:
                filedircalc, _ = os.path.splitext(file)
                vocals = f"{stems_dir}/" + filedircalc + "/vocals.wav"
                if os.path.exists(vocals):
                    os.remove(vocals)
            dirs = os.listdir(f"{stems_dir}/" + filedircalc)
        final_dict = {}
        #for filepath in dirs:
        #    final_dict[filepath.split("/")[-1].split(".")[0]] = self._process_file(
        #         f"{stems_dir}/" + filedircalc+"/"+filepath, speed=speed
        #    )
        
        print('') 
        print('')
        print('starting audio keyframe maker')
        print('') 
        print('')
        if args.spleeter:
            final_dict["other"] = self._process_other(
                f"{stems_dir}/" + filedircalc + "/other.wav", zoomspeed=zoomspeed
            )
            final_dict["piano"] = self._process_piano(
                f"{stems_dir}/" + filedircalc + "/piano.wav", zoomspeed=zoomspeed
            )    
            final_dict["drums"] = self._process_drums(
                f"{stems_dir}/" + filedircalc + "/drums.wav", zoomspeed=zoomspeed
            )
            final_dict["bass"] = self._process_bass(
                f"{stems_dir}/" + filedircalc + "/bass.wav", zoomspeed=zoomspeed
            )

            final_dict["zoom"] = self._process_zoom(
                f"{stems_dir}/" + filedircalc + "/" + args.zoom_sound + ".wav", zoomspeed=zoomspeed
            )
            final_dict["strength"] = self._process_strength(
                f"{stems_dir}/" + filedircalc + "/" + args.strength_sound + ".wav", zoomspeed=zoomspeed
            )
            final_dict["noise"] = self._process_noise(
                f"{stems_dir}/" + filedircalc + "/" + args.noise_sound + ".wav", zoomspeed=zoomspeed
            )
            final_dict["contrast"] = self._process_contrast(
                f"{stems_dir}/" + filedircalc + "/" + args.contrast_sound + ".wav", zoomspeed=zoomspeed
            )
        else:
            if args.other_audio_path:
                final_dict["other"] = self._process_other(
                    args.other_audio_path, zoomspeed=zoomspeed
                )
            if args.piano_audio_path:
                final_dict["piano"] = self._process_piano(
                    args.piano_audio_path, zoomspeed=zoomspeed
                )
            if args.drums_audio_path:            
                final_dict["drums"] = self._process_drums(
                    args.drums_audio_path, zoomspeed=zoomspeed
                )
            if args.bass_audio_path:
                final_dict["bass"] = self._process_bass(
                    args.bass_audio_path, zoomspeed=zoomspeed
                )
            if args.zoom_audio_path:
                final_dict["zoom"] = self._process_zoom(
                    args.zoom_audio_path, zoomspeed=zoomspeed
                )
            if args.strength_audio_path:
                final_dict["strength"] = self._process_strength(
                    args.strength_audio_path, zoomspeed=zoomspeed
                )
            if args.noise_audio_path:
                final_dict["noise"] = self._process_noise(
                    args.noise_audio_path, zoomspeed=zoomspeed
                )
            if args.contrast_audio_path:
                final_dict["contrast"] = self._process_contrast(
                    args.contrast_audio_path, zoomspeed=zoomspeed
                )
        return final_dict

    def _get_prep_values(self, filename, duration)-> np.ndarray:
        x, sr = librosa.load(filename)
        onset_frames = librosa.onset.onset_detect(
            x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1
        )
        onset_times = librosa.frames_to_time(onset_frames)
        total_lin_step = duration * self.fps
        vals, _ = np.histogram(
            onset_times, bins=total_lin_step, range=(0, duration)
        )
        beat_ind = np.argwhere(vals)
        return beat_ind
    
    def _process_piano(self, filename, zoomspeed=4):
        args = parse_args()
        logger.info(f"Processing file: {filename} for piano animation with speed: {args.piano_drop_speed}")
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
        logger.info(f"Processing file: {filename} for bass animation with speed: {args.bass_drop_speed}")
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
        logger.info(f"Processing file: {filename} for other audio animation with speed: {args.other_drop_speed}")
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
        logger.info(f"Processing file: {filename} for drums animation with speed: {args.drums_drop_speed}")
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
        logger.info(f"Processing file: {filename} with zoom schedule: {args.zoom_drop_speed}")
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
        logger.info(f"Processing file: {filename} with strength schedule: {args.strength_drop_speed}")
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
        logger.info(f"Processing file: {filename} with noise schedule: {args.noise_drop_speed}")
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
        logger.info(f"Processing file: {filename} with contrast schedule: {args.contrast_predrop_speed}")
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
            # logger.info()
            if post_beat < beat_ind[i]:
                post_tup = (post_beat, post_beat_transition__value)
                key_frame_value.append(post_tup)
                # logger.info(f"{i}  beat_ind[i]: {beat_ind[i]}, post {post_tup}")
            pre = (beat_ind[i] - frames_change_pre_beat - 1)[0]
            if (
                len(key_frame_value) == 0
                or len(key_frame_value) != 0
                and key_frame_value[-1][0] != pre
            ):
                # logger.info(f"{i}  beat_ind[i]: {beat_ind[i]}, pre {pre, 0}")
                key_frame_value.append((pre, pre_beat_transition__value))
            beat = beat_ind[i][0]
            # logger.info(f"{i}  beat_ind[i]: {beat_ind[i]}, beat {beat, beat_transition_value}")
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
        logger.info(f"Processing file: {filename} with speed: {speed}")
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
        
    def bpmdetection():
        filename = args.file
    
        y, sr = librosa.load(filename)
    
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
        print("")
        print("")
        print ('bpm: {:.2f}'.format(tempo))
        data = tempo
        with open("bpm.json", "w") as fp2:
            json.dump(tempo, fp2)
            print("processing of the bpm succeeded and exported to bpm.json")


if __name__ == "__main__":
    args = parse_args()
    """if args.musicstart and not args.musicend:
        subprocess.run(["python", "length.py", "--file", args.file, "--musicstart", args.musicstart])#, "--musicend",args.musicend])
    elif args.musicstart and args.musicend:
        subprocess.run(["python", "length.py", "--file", args.file, "--musicstart", args.musicstart, "--musicend",args.musicend])
    elif args.musicend and not args.musicstart:
        subprocess.run(["python", "length.py", "--file", args.file, "--musicend",args.musicend])
    else:
        print('audio not cropped')"""
    
    service = AudioKeyframeService(fps=args.fps)
    if args.spleeter:
        if args.music_cut:
            final_dict = service.process(args.stems,flnm, zoomspeed=args.zoomspeed, speed=args.speed)
        else:
            final_dict = service.process(args.stems,args.file, zoomspeed=args.zoomspeed, speed=args.speed)
    else:
        #not important, just to dodge an error
        print("")
        print("")
        print('put your original audio in the source folder and always pass --file original_file.wav/mp3 , gives bugs otherwise, will fix later')
        print("")
        print("")
        #important
        final_dict = service.process(args.stems,file="do_not_delete.wav", zoomspeed=args.zoomspeed, speed=args.speed)
    with open("audio_splitter_keyframes.json", "w") as fp:
        json.dump(final_dict, fp, indent=2)
        print("")
        print("")
        print("processing of the keyframes succeeded and exported to audio_splitter_keyframes.json")
    

    #AudioKeyframeService.bpmdetection()
    
    
