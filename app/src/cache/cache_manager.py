# src\cache\cache_manager.py
import redis
import json
from collections import OrderedDict

class CacheManager:
    def __init__(self, host="localhost", port=6379, db=0, password=None, memory_limit=100):
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        self.memory_cache = {}
        self.memory_limit = memory_limit

    def get(self, key):
        if key in self.memory_cache:
            return self.memory_cache[key]
        value = self.client.get(key)
        if value:
            self.memory_cache[key] = value
        return value

    def set(self, key, value, ttl=3600):
        self.memory_cache[key] = value
        self.client.set(key, value, ex=ttl)

    def delete(self, key):
        if key in self.memory_cache:
            del self.memory_cache[key]
        self.client.delete(key)

    def generate_cache_key(self, question: str) -> str:
        """
        Gera uma chave única para armazenar uma pergunta no cache.
        """
        return f"cache:{hash(question)}"
