# nlp_processor.py
import spacy
from sentence_transformers import SentenceTransformer
from src.agent.cache_manager import CacheManager
from typing import Dict, List, Tuple


class NLPProcessor:
    def __init__(self, spacy_model: str, embedding_model: str, cache: CacheManager):
        self.nlp = spacy.load(spacy_model)
        self.embedding_model = SentenceTransformer(
            embedding_model
        )  # Testar GPU .to('cuda')
        self.cache = cache

    def extract_entities(self, text: str) -> Dict:
        cached = self.cache.get(f"nlp:entities:{text}")
        if cached:
            return cached

        doc = self.nlp(text)
        entities = {
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "nouns": [token.text for token in doc if token.pos_ == "NOUN"],
        }

        self.cache.set(f"nlp:entities:{text}", entities)
        return entities

    def get_embedding(self, text: str) -> List[float]:
        cached = self.cache.get(f"embedding:{text}")
        if cached:
            return cached

        embedding = self.embedding_model.encode(text).tolist()
        self.cache.set(f"embedding:{text}", embedding)
        return embedding
