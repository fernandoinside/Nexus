# src\assistent\recognition\recognition_vosk.py
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from src.assistent.recognition.recognition_base import RecognitionBase
from src.utils.logger import logging
import os
import requests
from zipfile import ZipFile
from pathlib import Path

class VoskRecognition(RecognitionBase):
    def __init__(self, model_path, sample_rate=16000, frame_size=4096):
        # Verifica se o modelo existe no caminho especificado
        logging.info(f"Verificando se o modelo Vosk existe em {model_path}")
        if not os.path.exists(model_path):
            model_path = self.download_vosk_model()        
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
        
    def download_vosk_model(self):    
        if not os.path.exists("app/src/models/vosk/vosk-model-small-pt-0.3"):            
            logging.DEBUG("Downloading Vosk model...")
            url = "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip"
            zip_path = "app/src/models/vosk/vosk-model-small-pt-0.3.zip"
            
            # Create directories if they don't exist
            os.makedirs("app/src/models/vosk", exist_ok=True)
            
            # Download the model
            response = requests.get(url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)
                
            # Extract the model
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("app/src/models/vosk")
                
            # Clean up zip file
            os.remove(zip_path)
            logging.DEBUG("Model downloaded and extracted successfully!")
        return "app/src/models/vosk/vosk-model-small-pt-0.3"