# src\assistent\recognition\recognition_base.py
import os
from dotenv import load_dotenv

load_dotenv()

class RecognitionBase:
    def __init__(self):
        engine = os.getenv("RECOGNITION_ENGINE", "vosk")
        if engine == "vosk":
            from src.assistent.recognition.recognition_vosk import VoskRecognition
            model_path = os.getenv("VOSK_MODEL_PATH", "src/models/vosk-model-small-pt-0.3")
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
