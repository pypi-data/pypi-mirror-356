from langchain_huggingface import HuggingFaceEmbeddings
from ragloader.splitting import DocumentChunk
from ragloader.embedding import ChunkEmbedder, EmbeddedChunk

class OrlikBKartonBERTUSE(ChunkEmbedder):
    model_name: str = "OrlikB/KartonBERT-USE-base-v1"
    vector_length: int = 768

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    def embed(self, chunk: DocumentChunk) -> EmbeddedChunk:
        embedding = self.embeddings.embed_query(chunk.content)
        embedded_chunk = EmbeddedChunk(
            document_chunk=chunk, embedding=embedding, embedding_model=self.model_name
        )
        return embedded_chunk
