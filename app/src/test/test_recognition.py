# src\test\test_recognition.py
from src.assistent.recognition.recognition import Recognition

def main():
    # Inicializa o objeto Recognition
    recognition = Recognition()

    # Teste de reconhecimento de fala
    print("Diga algo...")
    
    try:
        # Captura a entrada de voz
        voice_input = recognition.listen()
        
        # Verifica se algo foi reconhecido
        if voice_input:
            print(f"Você disse: {voice_input}")
        else:
            print("Nenhum áudio foi reconhecido.")
    
    except Exception as e:
        print(f"Erro durante o reconhecimento: {e}")

if __name__ == "__main__":
    main()
