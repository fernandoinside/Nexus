# src\nlp\nlp_processor.py
import spacy
from langdetect import detect

class NLPProcessor:
    def __init__(self, spacy_model="pt_core_news_sm"):
        self.nlp = spacy.load(spacy_model)

    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return "unknown"

    def process_text(self, text):
        doc = self.nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        return tokens
