from typing import List

from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import config
from app.schemas.chunk import Chunk


class DocumentChunker:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""], 
        )

    def split(self, documents: List[LCDocument]) -> List[Chunk]:
        split_docs = self.splitter.split_documents(documents)

        chunks: List[Chunk] = []

        for i, doc in enumerate(split_docs):
            chunk = Chunk(
                text=doc.page_content,
                metadata=doc.metadata  
            )
            chunks.append(chunk)

        return chunks