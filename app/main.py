import os
from dotenv import load_dotenv

from src.utils.logger import logging

from src.agent.agent import Agent

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def main():
    """
    Ponto de entrada principal para iniciar o Agent.
    """
    agent_name = os.getenv("Nexos", "default_agent")

    logging.info(f"Inicializando o {agent_name}...")

    timeout = os.getenv("TIMEOUT_AGENT", 15)  # Tempo padrão de 15 segundos

    # Inicializa o agente
    agent = Agent(timeout=timeout)

    # Inicia o modo de escuta
    agent.start_listening()

    logging.info("Agente está ativo e aguardando comandos...")

    # Loop para processar os comandos continuamente
    try:
        while True:
            if not agent.process_commands():
                logging.info("Finalizando execução do agente...")
                break
    except KeyboardInterrupt:
        logging.warning("Interrupção pelo usuário detectada. Encerrando o programa...")
    except Exception as e:
        logging.error(f"Erro inesperado durante a execução: {e}")

if __name__ == "__main__":
    main()
