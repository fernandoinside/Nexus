# srcc\assistent\speech\speech_google.py
from google.cloud import texttospeech
import os
from src.assistent.speech.speech_base import SpeechBase

class SpeechGoogle(SpeechBase):
    def __init__(self, language_code="pt-BR", voice_name="pt-BR-Wavenet-A", output_file="output.mp3"):
        self.language_code = language_code
        self.voice_name = voice_name
        self.output_file = output_file
        self.client = texttospeech.TextToSpeechClient()

    def speak(self, text: str):
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=self.language_code, name=self.voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = self.client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        with open(self.output_file, "wb") as out:
            out.write(response.audio_content)
        os.system(f"mpg123 {self.output_file}")