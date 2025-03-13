# src\assistent\recognition\recognition_base.py
import os
from src.utils.config import config

class RecognitionBase:
    def __init__(self):
        
        engine = config.RECOGNITION_ENGINE

        if engine == "vosk":
            from src.assistent.recognition.recognition_vosk import VoskRecognition
            model_path = config.RECOGNITION_VOSK_MODEL_PATH
            self.engine = VoskRecognition(
                model_path=model_path,
            )
        elif engine == "speech_recognition":
            from src.assistent.recognition.recognition_speech_recognition import SpeechRecognition
            self.engine = SpeechRecognition()
        else:
            raise ValueError(f"Engine de reconhecimento desconhecida: {engine}")

    def listen(self) -> str:
        return self.engine.listen()
