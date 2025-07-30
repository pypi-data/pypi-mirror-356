from enum import Enum

# Lazy import moved to value property below to avoid import-time side effects


class EmbeddingModelsMapper(Enum):
    """Mapper from embedding models' names and embedding models."""
    paraphrase_multilingual_mpnet = "paraphrase_multilingual_mpnet"
    all_mpnet_base = "all_mpnet_base"
    openai_ada = "openai_ada"
    legal_bert = "legal_bert"
    OrlikB_KartonBERT_USE_base_v1 = "OrlikB_KartonBERT_USE_base_v1"

    def value(self):
        if self.name == "paraphrase_multilingual_mpnet":
            from .embedders.paraphrase_multilingual_mpnet import ParaphraseMultilingualMpnet
            return ParaphraseMultilingualMpnet()
        elif self.name == "all_mpnet_base":
            from .embedders.all_mpnet_base import AllMpnetBase
            return AllMpnetBase()
        elif self.name == "openai_ada":
            from .embedders.openai_ada import OpenAIAda
            return OpenAIAda()
        elif self.name == "legal_bert":
            from .embedders.legal_bert import LegalBertBaseUncased
            return LegalBertBaseUncased()
        elif self.name == "OrlikB_KartonBERT_USE_base_v1":
            from .embedders.orlikb_kartonbert_use import OrlikBKartonBERTUSE
            return OrlikBKartonBERTUSE()
        else:
            raise ValueError(f"Unknown embedder: {self.name}")
