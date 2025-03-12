# test_speech.py
from src.assistent.speech.speech import Speech

def main():
    # Inicializa o objeto Speech
    speech = Speech()

    # Teste de fala com diferentes textos
    texts_to_speak = [
        "Olá, bem-vindo ao assistente virtual! Este é um teste de conversão de texto para fala. Estas configurações otimizam a voz para soar mais natural em português brasileiro, com velocidade e entonação ajustadas para melhor compreensão."
    ]

    for text in texts_to_speak:
        print(f"Tentando falar: {text}")
        try:
            speech.speak(text)
        except Exception as e:
            print(f"Erro ao falar: {e}")

if __name__ == "__main__":
    main()