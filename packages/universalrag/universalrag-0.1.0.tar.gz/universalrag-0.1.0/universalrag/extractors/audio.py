# universalrag/extractors/audio_extractor.py
import whisper

model = whisper.load_model("base")

def extract_text_from_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]