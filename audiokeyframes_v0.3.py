# dependencies
#pip install numpy
#pip install loguru
#pip install spleeter
#pip install librosa
#pip install pydub

from loguru import logger
import json, argparse, subprocess, os

# keyframes
import numpy as np
import librosa
import csv

from pydub import AudioSegment

def parse_args():
    logger.info(f"Parsing arguments...")
    desc = "Blah"

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="input audio")
    
    parser.add_argument("-s", "--fps", type=int, help="frames per second")
    
    parser.add_argument("-t","--stems",type=str,default="5",help="the amount of exported audio files, 3, 4, 5",)
    
    parser.add_argument("--speed",type=float,default="0.4",help="reactive impact of the audio on the animation",)
    
    parser.add_argument("-z","--zoomspeed",type=float,default="5",help="reactive zoom impact of the audio on the animation",)
    
    parser.add_argument("--use_vocals",type=float,help="vocals seem to have a negative effect on the animation so it's disabled by default",)
    
    args = parser.parse_args()
    return args



#
    
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
        for filepath in dirs:
            final_dict[filepath.split("/")[-1].split(".")[0]] = self._process_file(
                 f"{stems_dir}/" + filedircalc+"/"+filepath, speed=speed
            )
        final_dict["zoom"] = self._process_zoom(
            f"{stems_dir}/" + filedircalc + "/bass.wav", zoomspeed=zoomspeed
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

    def _process_zoom(self, filename, zoomspeed=4):
        logger.info(f"Processing file: {filename} with speed: {zoomspeed}")
        meta: AudioKeyframeMeta = self._get_metadata(filename)
        beat_ind = self._get_prep_values(filename, duration=meta.duration)
        frames_change_pre_beat = 0
        frames_change_post_beat = 100  # there are the amount of buffer frames before and after a beat to let value linear change
        #   If my beat is at 10.    9:(0), 10:(1), 22:(0). So between frames 10-22 they linearly scale. But look to change from linear to -exp
        post_beat_transition__value = zoomspeed
        beat_transition_value = zoomspeed * 1.4
        pre_beat_transition__value = zoomspeed / 8
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
    
        print ('bpm: {:.2f}'.format(tempo))
        data = tempo
        with open("bpm.json", "w") as fp2:
            json.dump(tempo, fp2)
            print("processing of the bpm succeeded and exported to bpm.json")


if __name__ == "__main__":
    args = parse_args()
    service = AudioKeyframeService(fps=args.fps)
    final_dict = service.process(args.stems,args.file, zoomspeed=args.zoomspeed, speed=args.speed)
    
    with open("keyframes.json", "w") as fp:
        json.dump(final_dict, fp, indent=2)
        print("")
        print("processing of the keyframes succeeded and exported to keyframes.json")
    

    AudioKeyframeService.bpmdetection()
    
    
