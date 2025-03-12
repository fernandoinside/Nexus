from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "uri": os.getenv("NEO4J_URI"),
    "user": os.getenv("NEO4J_USER"),
    "password": os.getenv("NEO4J_PASSWORD"),
    "database": os.getenv("NEO4J_DATABASE", "neo4j")  # Padrão: neo4j
}

CACHE_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", 6379)),
    "db": 0,
    "memory_limit": 100
}