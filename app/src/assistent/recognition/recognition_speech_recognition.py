# src\assistent\recognition\recognition_speech_recognition.py
import logging

import speech_recognition as sr
from src.assistent.recognition.recognition_base import RecognitionBase


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

class SpeechRecognition(RecognitionBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, timeout=None):
        """
        Captura áudio do microfone com suporte a timeout
        
        :param timeout: Tempo máximo de espera para capturar áudio
        :return: Texto reconhecido ou None
        """
        try:
            # Ajuste de ruído ambiente
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("Ajustando para ruído ambiente...")
                
                # Configurações de reconhecimento
                self.recognizer.dynamic_energy_threshold = True
                
                # Captura de áudio com timeout
                try:
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout,  # Adiciona suporte a timeout
                        phrase_time_limit=5  # Limite de tempo para frase
                    )
                    
                    # Reconhecimento de fala
                    try:
                        text = self.recognizer.recognize_google(audio, language='pt-BR')
                        logging.info(f"Texto reconhecido: {text}")
                        return text
                    
                    except sr.UnknownValueError:
                        logging.warning("Não foi possível entender o áudio")
                    except sr.RequestError as e:
                        logging.error(f"Erro na requisição de reconhecimento: {e}")
                
                except sr.WaitTimeoutError:
                    logging.warning("Tempo de espera para áudio excedido")
                
                except Exception as capture_error:
                    logging.error(f"Erro na captura de áudio: {capture_error}")
        
        except Exception as e:
            logging.error(f"Erro crítico no reconhecimento de voz: {e}")
        
        return None

    def is_microphone_available(self):
        """
        Verifica se há microfones disponíveis
        
        :return: Booleano indicando disponibilidade de microfone
        """
        try:
            devices = sr.Microphone.list_microphone_names()
            return len(devices) > 0
        except Exception as e:
            logging.error(f"Erro ao verificar microfones: {e}")
            return False