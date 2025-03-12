# src\assistent\chatbot.py
import os
from src.assistent.chat.chatbot_base import ChatBase
import json

class Chatbot(ChatBase):
    def __init__(self):
        """
        Inicializa o Chatbot como uma extensão do ChatBase.
        """
        super().__init__()
        # Carrega o arquivo JSON ao inicializar o chatbot
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "prompts", "context_pesquisa.json")
            with open(file_path, "r", encoding="utf-8") as f:
                self.context_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado!")
        except json.JSONDecodeError:
            raise ValueError(f"O arquivo '{file_path}' não pôde ser decodificado. Verifique a formatação JSON.")
    
    def chat(self, prompt):
        """
        Método para identificar o melhor contexto e enviar a pergunta.
        """
        try:
            # Identificar o melhor contexto para o prompt
            selected_context = self.identify_context(prompt)

            # Substituir {palavra} no contexto selecionado pelo conteúdo do prompt
            final_prompt = selected_context["context"].replace("{palavra}", prompt)

            # Enviar o prompt final para o método ask e retornar a resposta
            return self.ask(final_prompt)
        except Exception as e:
            return f"Erro ao processar o prompt: {e}"

    def identify_context(self, prompt):
        """
        Analisa o prompt e retorna o contexto mais adequado.
        """
        for item in self.context_data["ask"]:
            for keyword in item["work"]:
                if keyword.lower() in prompt.lower():
                    return item
        
        # Caso nenhum contexto seja identificado, lança uma exceção
        raise ValueError("Nenhum contexto adequado encontrado para o prompt.")