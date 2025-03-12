# src\assistent\speech\speech_base.py
import os
from dotenv import load_dotenv

load_dotenv()

class SpeechBase:
    @classmethod
    def get_speech_engine(cls):
        """
        Seleciona a engine de síntese de fala com base na configuração no .env.
        """
        engine = os.getenv("SPEECH_ENGINE", "pyttsx")
        
        if engine == "coqui":
            from src.assistent.speech.speech_coqui import CoquiSpeech
            return CoquiSpeech()

        elif engine == "azure":
            from src.assistent.speech.speech_azure import SpeechAzure
            return SpeechAzure(
                subscription_key=os.getenv("AZURE_KEY"),
                region=os.getenv("AZURE_REGION"),
                voice_name="pt-BR-FranciscaNeural"
            )

        elif engine == "google":
            from src.assistent.speech.speech_google import SpeechGoogle
            return SpeechGoogle()

        elif engine == "pyttsx":
            from src.assistent.speech.speech_pyttsx import SpeechPyttsx
            return SpeechPyttsx(
                voice_name="brazil",  # Pode ajustar conforme disponibilidade
                rate=180,  # Velocidade padrão
                volume=0.8  # Volume padrão
            )
        else:
            raise ValueError(f"Engine de síntese de fala desconhecida: {engine}")
