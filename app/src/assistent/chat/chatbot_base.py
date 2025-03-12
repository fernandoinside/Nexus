# src\assistent\chat\chatbot_base.py
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

class ChatBase:
    def __init__(self):
        """
        Inicializa o ChatBase, selecionando a engine com base no .env.
        """
        self.chatbot = self.get_chatbot()

    def get_chatbot(self):
        """
        Decide qual engine usar com base na variável 'ASK_ENGINE' no .env.
        """        

        engine = os.getenv("ASK_ENGINE", "ollama")  # Padrão: Ollama
        if engine == "ollama":
            from src.assistent.chat.chatbot_ollama import OllamaChatbot
            model_name = os.getenv("OLLAMA_MODEL", "mistral")  # Modelo padrão: mistral
            return OllamaChatbot(model_name=model_name)
        elif engine == "gpt":
            from src.assistent.chat.chatbot_gpt import GPTChatbot
            return GPTChatbot()
        else:
            raise ValueError(f"Engine desconhecida: {engine}")

    def ask(self, prompt: str) -> str:
        """
        Envia a pergunta para a engine configurada e retorna a resposta.
        """
        return self.chatbot.ask(prompt)
