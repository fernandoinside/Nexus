# src\assistent\chat\chatbot_gpt.py
import os
from src.utils.config import config
from openai import OpenAI
from src.assistent.chat.chatbot_base import ChatBase

class GPTChatbot(ChatBase):
    def __init__(self):
        """
        Inicializa o chatbot utilizando a API da OpenAI GPT.
        """
        print("Inicializando o chatbot GPT...")    
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"  # or "gpt-4" if you have access

    def ask(self, prompt: str) -> str:
        """
        Envia um prompt para a API do GPT e retorna a resposta.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao acessar o GPT: {e}"
