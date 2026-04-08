from pathlib import Path
from typing import List

from langchain_core.documents import Document as LCDocument
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    @staticmethod
    def load(file_path: str) -> List[LCDocument]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        if path.suffix != ".pdf":
            raise ValueError("Only PDF files are supported")

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        return documents