import pyttsx3
from src.assistent.speech.speech_base import SpeechBase

class SpeechPyttsx(SpeechBase):
    def __init__(self, voice_name=None, rate=None, volume=None):
        """
        Inicializa o motor de fala usando pyttsx3
        
        :param voice_name: Nome da voz (opcional)
        :param rate: Velocidade da fala (opcional)
        :param volume: Volume da fala (0.0 a 1.0)
        """
        self.engine = pyttsx3.init()
        
        # Configurações opcionais
        if voice_name:
            self._set_voice(voice_name)
        
        if rate:
            self.engine.setProperty('rate', rate)
        
        if volume is not None:
            self.engine.setProperty('volume', volume)

    def _set_voice(self, voice_name=None):
        """
        Seleciona uma voz específica
        """
        voices = self.engine.getProperty('voices')
        
        # Tenta encontrar a voz por nome ou língua
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                return
        
        # Se não encontrar, usa a primeira voz disponível
        if voices:
            self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str):
        """
        Converte texto em fala
        
        :param text: Texto a ser falado
        """
        self.engine.say(text)
        self.engine.runAndWait()
