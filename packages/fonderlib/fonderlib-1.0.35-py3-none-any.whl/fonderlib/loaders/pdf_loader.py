from langchain_community.document_loaders import PyPDFLoader
from .loader import Loader


class PDFLoader(Loader):
    def load(self, file_path: str):
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            return docs
        except Exception as e:
            raise Exception(f"Failed to load PDF file: {str(e)}")
