# src/assistent/speech/speech_coqui.py
import os
import sounddevice as sd
import soundfile as sf
from TTS.api import TTS
from src.assistent.speech.speech_base import SpeechBase
from TTS.utils.manage import ModelManager

class CoquiSpeech(SpeechBase):
    def __init__(self):
        
        # Caminho para o modelo TTS em português brasileiro
        model_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'tts', 'tts_models--pt--cv--vits')

        if not os.path.exists(model_path):
            print("Baixando modelo TTS em português brasileiro...")            
            self.tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=True)
        else:
            print("Usando modelo TTS brasileiro existente...")
            self.tts = TTS(model_path=model_path)

        # Configurações otimizadas para português brasileiro
        self.voice_configs = {
            'speed': 0.75,
            'sample_rate': 24000,
            'pitch': 1.1
        }

    def speak(self, text: str):
        # Gera o arquivo de áudio com base no texto fornecido
        self.tts.tts_to_file(
            text=text,
            file_path="output.wav",
            speed=self.voice_configs['speed']
        )
        self._play_audio_file("output.wav")

    def _play_audio_file(self, file_path):
        # Reproduz o arquivo de áudio gerado
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate)
        sd.wait()
