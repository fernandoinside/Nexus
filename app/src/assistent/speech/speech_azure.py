# src\assistent\speech\speech_azure.py
import azure.cognitiveservices.speech as speechsdk
from src.assistent.speech.speech_base import SpeechBase

class SpeechAzure(SpeechBase):
    def __init__(self, subscription_key, region, voice_name="pt-BR-FranciscaNeural"):
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        self.speech_config.speech_synthesis_voice_name = voice_name
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def speak(self, text: str):
        self.synthesizer.speak_text_async(text).get()
