from typing import List

from app.embeddings.embedder import Embedder
from app.vectorstore.pinecone_store import PineconeStore
from app.schemas.chunk import Chunk
from app.config import config


class Retriever:

    def __init__(self):
        self.embedder = Embedder()
        self.vectorstore = PineconeStore()

    def retrieve(self, query: str, top_k: int = None) -> List[Chunk]:

        query_embedding = self.embedder.embed_text(query)

        
        top_k = top_k or config.TOP_K

        results = self.vectorstore.query(
            embedding=query_embedding,
            top_k=top_k
        )


        chunks: List[Chunk] = []

        for match in results["matches"]:
            metadata = match["metadata"]

            chunk = Chunk(
                text=metadata.get("text", ""),
                metadata={
                    k: v for k, v in metadata.items() if k != "text"
                }
            )

            chunks.append(chunk)

        return chunks