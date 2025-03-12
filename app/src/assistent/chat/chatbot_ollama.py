# src\assistent\chat\chat_ollama.py
import requests
from src.assistent.chat.chat_base import ChatBase

class OllamaChatbot(ChatBase):
    def __init__(self, model_name="mistral"):
        """
        Inicializa o chatbot utilizando o Ollama e define o modelo.
        """
        self.base_url = "http://localhost:11434"  # Endpoint da API do Ollama
        self.model_name = model_name  # Define o modelo (ex.: mistral, llama2:7b)

    def ask(self, prompt: str) -> str:
        """
        Envia um prompt para o modelo configurado no Ollama e retorna a resposta.
        """
        url = f"{self.base_url}/completion"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": 200,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get("choices", [{}])[0].get("text", "").strip()
        except requests.exceptions.ConnectionError:
            return "Erro: Não foi possível conectar ao servidor do Ollama. Certifique-se de que ele está rodando."
        except requests.exceptions.HTTPError as http_err:
            return f"Erro HTTP ao comunicar-se com o Ollama: {http_err}"
        except Exception as e:
            return f"Erro inesperado: {e}"
