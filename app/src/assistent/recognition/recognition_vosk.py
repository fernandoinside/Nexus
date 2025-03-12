# src\assistent\recognition\recognition_vosk.py
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from src.assistent.recognition.recognition_base import RecognitionBase

class VoskRecognition(RecognitionBase):
    def __init__(self, model_path, sample_rate=16000, frame_size=4096):
        self.model = Model(model_path)
        self.sample_rate = sample_rate
        self.frame_size = frame_size

    def listen(self) -> str:
        recognizer = KaldiRecognizer(self.model, self.sample_rate)
        mic = pyaudio.PyAudio()
        stream = mic.open(
            format=pyaudio.paInt16, 
            channels=1, 
            rate=self.sample_rate, 
            input=True, 
            frames_per_buffer=self.frame_size
        )
        stream.start_stream()

        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")

    def is_microphone_available(self):
        """
        Verifica se o microfone está disponível.
        """
        try:
            audio = pyaudio.PyAudio()
            count = audio.get_device_count()
            audio.terminate()
            return count > 0
        except Exception as e:
            # Loga se houver algum problema
            logging.error(f"Erro ao verificar microfone: {e}")
            return False