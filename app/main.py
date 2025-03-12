import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Redis e Neo4j
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "minha_senha_secreta")

def main():
    # Mostra uma mensagem de boas-vindas
    print("Bem-vindo ao programa de gerenciamento de dados!")    
    # Mostrar as Configurações
    print("Configurações:")
    print("Redis Host:", REDIS_HOST)
    print("Redis Port:", REDIS_PORT)
    print("Neo4j URI:", NEO4J_URI)
    print("Neo4j User:", NEO4J_USER)
    print("Neo4j Password:", NEO4J_PASSWORD)       


# Executar o programa principal
if __name__ == "__main__":
    # Executar o programa principal
    main()
