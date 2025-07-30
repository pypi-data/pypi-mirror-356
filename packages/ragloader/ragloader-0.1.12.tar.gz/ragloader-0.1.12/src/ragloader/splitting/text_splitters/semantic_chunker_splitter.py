from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents.base import Document as LangchainDocument
from ragloader.splitting import BaseTextSplitter
class SemanticChunkerSplitter(BaseTextSplitter):
    """
    Semantic chunker using LangChain's SemanticChunker.
    """
    def __init__(self, embedding_model: str = "OrlikB/KartonBERT-USE-base-v1", min_chunk_size: int = 800):
        self.embedding_model = embedding_model
        self.min_chunk_size = min_chunk_size
        self.splitter = None

    def split(self, text: str) -> list[str]:
        if not self.splitter:
            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
            self.splitter = SemanticChunker(
                embeddings,
                breakpoint_threshold_type="percentile",
                breakpoint_threshold_amount=95,
                min_chunk_size=self.min_chunk_size,
            )
        split_documents: list[LangchainDocument] = self.splitter.split_text(text)
        #return [doc.page_content for doc in split_documents]
        return [doc for doc in split_documents]