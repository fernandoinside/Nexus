# src\nlp\embedding_manager.py
from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text):
        return self.model.encode(text).tolist()
