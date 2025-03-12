# src\assistent\speech\speech.py
from src.assistent.speech.speech_base import SpeechBase

class Speech(SpeechBase):
    def __init__(self):
        """
        Inicializa o Speech com o motor de fala
        """
        self.speech_engine = SpeechBase.get_speech_engine()
    
    def speak(self, text):
        """
        Converte texto em fala usando o motor selecionado
        """
        self.speech_engine.speak(text)