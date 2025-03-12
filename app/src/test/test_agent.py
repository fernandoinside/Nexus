# src/test/test_agent.py
import sys
from src.agent.agent import Agent

if __name__ == "__main__":
    agent = Agent()
    agent.start_listening()

    # Simula processamento de comandos (exemplo)
    while True:
        if not agent.process_commands():
            break