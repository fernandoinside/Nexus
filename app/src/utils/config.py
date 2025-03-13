import os
from dotenv import load_dotenv
from src.utils.logger import logging

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Configurações do banco de dados Neo4j
    DB_CONFIG = {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD", "password"),
        "database": os.getenv("NEO4J_DATABASE", "neo4j"),
    }

    # Configurações de cache (Redis)
    CACHE_CONFIG = {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", 6379)),
        "db": int(os.getenv("REDIS_DB", 0)),
        "memory_limit": int(os.getenv("CACHE_MEMORY_LIMIT", 100)),
    }

    # Configurações gerais do sistema
    APP_PORT = int(os.getenv("APP_PORT", 5000))
    AGENT_NAME = os.getenv("AGENT_NAME", "Nexus")
    TIMEOUT_AGENT = int(os.getenv("TIMEOUT_AGENT", 10))

    # Configurações de NLP e embeddings
    SPACY_MODEL = os.getenv("SPACY_MODEL", "pt_core_news_sm")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Configurações de reconhecimento de voz e fala
    PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")
    SPEECH_ENGINE = os.getenv("SPEECH_ENGINE", "coqui")
    RECOGNITION_ENGINE = os.getenv("RECOGNITION_ENGINE", "vosk")
    RECOGNITION_VOSK_MODEL_PATH = os.getenv("RECOGNITION_VOSK_MODEL_PATH", "")

    # Configurações de APIs e serviços externos
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_KEY = os.getenv("DEEPSEEK", "")
    AZURE_KEY = os.getenv("AZURE_KEY", "")
    AZURE_REGION = os.getenv("AZURE_REGION", "brazilsouth")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

    # Configurações para Slack
    SLACK_CONFIG = {
        "app_id": os.getenv("SLACK_App_ID", ""),
        "client_id": os.getenv("SLACK_Client_ID", ""),
        "client_secret": os.getenv("SLACK_Client_Secret", ""),
        "signing_secret": os.getenv("SLACK_Signing_Secret", ""),
        "verification_token": os.getenv("SLACK_Verification_Token", ""),
        "xapp_token": os.getenv("SLACK_xapp", ""),
        "xoxb_token": os.getenv("SLACK_xoxb", ""),
    }

    # Configurações específicas do sistema
    ASK_ENGINE = os.getenv("ASK_ENGINE", "ollama")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    SEED_DATABASE = os.getenv("SEED_DATABASE", "false").lower() == "true"
    INTERACTION_MODE = os.getenv("INTERACTION_MODE", "voz")

    @staticmethod
    def log_configurations():
        """
        Lista todas as configurações e as registra no log.
        """
        logging.info("==== Configurações do Sistema ====")

        # Log das configurações do Neo4j
        logging.info(f"DB_CONFIG: {Config.DB_CONFIG}")

        # Log das configurações do cache
        logging.info(f"CACHE_CONFIG: {Config.CACHE_CONFIG}")

        # Log das configurações gerais
        logging.info(f"APP_PORT: {Config.APP_PORT}")
        logging.info(f"AGENT_NAME: {Config.AGENT_NAME}")
        logging.info(f"TIMEOUT_AGENT: {Config.TIMEOUT_AGENT}")

        # Log de NLP e embeddings
        logging.info(f"SPACY_MODEL: {Config.SPACY_MODEL}")
        logging.info(f"EMBEDDING_MODEL: {Config.EMBEDDING_MODEL}")

        # Log das configurações de reconhecimento e fala
        logging.info(f"PORCUPINE_ACCESS_KEY: {Config.PORCUPINE_ACCESS_KEY}")
        logging.info(f"SPEECH_ENGINE: {Config.SPEECH_ENGINE}")
        logging.info(f"RECOGNITION_ENGINE: {Config.RECOGNITION_ENGINE}")
        logging.info(f"VOSK_MODEL_PATH: {Config.RECOGNITION_VOSK_MODEL_PATH}")

        # Log das configurações de APIs externas
        logging.info(f"OPENAI_API_KEY: {Config.OPENAI_API_KEY}")
        logging.info(f"DEEPSEEK_KEY: {Config.DEEPSEEK_KEY}")
        logging.info(f"AZURE_KEY: {Config.AZURE_KEY}")
        logging.info(f"AZURE_REGION: {Config.AZURE_REGION}")
        logging.info(f"GOOGLE_APPLICATION_CREDENTIALS: {Config.GOOGLE_APPLICATION_CREDENTIALS}")

        # Log das configurações do Slack
        logging.info(f"SLACK_CONFIG: {Config.SLACK_CONFIG}")

        # Log de configurações específicas do sistema
        logging.info(f"ASK_ENGINE: {Config.ASK_ENGINE}")
        logging.info(f"OLLAMA_MODEL: {Config.OLLAMA_MODEL}")
        logging.info(f"SEED_DATABASE: {Config.SEED_DATABASE}")
        logging.info(f"INTERACTION_MODE: {Config.INTERACTION_MODE}")

        logging.info("==== Fim das Configurações ====")

# Acesso centralizado às configurações
config = Config()
