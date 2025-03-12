# src\assistent\recognition.py
from src.assistent.recognition.recognition_base import RecognitionBase

class Recognition(RecognitionBase):
    def __init__(self):
        """
        Inicializa o Recognition como uma extensão do RecognitionBase.
        Herda o motor de reconhecimento configurado no .env
        """
        super().__init__()
    
    def listen(self):
        """
        Método para capturar entrada de voz
        Delega para o motor de reconhecimento selecionado
        """
        return self.engine.listen()
        
    def is_microphone_available(self):
        return self.engine.is_microphone_available()