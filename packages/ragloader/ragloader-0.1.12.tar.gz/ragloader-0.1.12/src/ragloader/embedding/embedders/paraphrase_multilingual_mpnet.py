import os
from langchain_huggingface import HuggingFaceEmbeddings

from ragloader.splitting import DocumentChunk
from ragloader.embedding import ChunkEmbedder, EmbeddedChunk


class ParaphraseMultilingualMpnet(ChunkEmbedder):
    model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    vector_length: int = 768

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'token': os.environ["HUGGINGFACE_TOKEN"]}
        )

    def embed(self, chunk: DocumentChunk) -> EmbeddedChunk:
        embedding: list[float] = self.embeddings.embed_query(chunk.content)

        embedded_chunk: EmbeddedChunk = EmbeddedChunk(
            document_chunk=chunk, embedding=embedding, embedding_model=self.model_name
        )

        return embedded_chunk
