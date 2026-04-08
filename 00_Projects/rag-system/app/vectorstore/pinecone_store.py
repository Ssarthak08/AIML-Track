from typing import List

from pinecone import Pinecone, ServerlessSpec

from app.config import config
from app.schemas.chunk import Chunk


class PineconeStore:

    def __init__(self):
        self.pc = Pinecone(api_key=config.PINECONE_API_KEY)

        self.index_name = config.PINECONE_INDEX_NAME

        self._create_index_if_not_exists()

        self.index = self.pc.Index(self.index_name)

    def _create_index_if_not_exists(self):
        existing_indexes = [idx["name"] for idx in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

    def upsert(self, chunks: List[Chunk], embeddings: List[List[float]]):
        vectors = []

        for chunk, embedding in zip(chunks, embeddings):
            vectors.append({
                "id": chunk.id,
                "values": embedding,
                "metadata": {
                    "text": chunk.text,  # 🔥 store text for retrieval
                    **chunk.metadata     # 🔥 preserve metadata
                }
            })

        self.index.upsert(vectors=vectors)

    def query(self, embedding: List[float], top_k: int = 5):
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )

        return results