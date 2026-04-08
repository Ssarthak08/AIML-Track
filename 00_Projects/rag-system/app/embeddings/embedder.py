from typing import List
from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self):
        # 🔥 Strong lightweight model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()    