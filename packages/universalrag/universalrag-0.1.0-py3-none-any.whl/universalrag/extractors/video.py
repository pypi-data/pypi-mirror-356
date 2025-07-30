# universalrag/extractors/video_extractor.py
from moviepy.video.io.VideoFileClip import VideoFileClip
from universalrag.extractors.audio import extract_text_from_audio

def extract_text_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)
    text = extract_text_from_audio(audio_path)
    return text
