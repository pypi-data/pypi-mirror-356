"""Embedding models for Think AI - fallback implementation."""

import numpy as np
from typing import List, Any

class EmbeddingModel:
    """Fallback embedding model that generates random embeddings."""
    
    def __init__(self, model_name: str = "fallback"):
        self.model_name = model_name
        self.dimension = 384  # Standard small model dimension
        
    def encode(self, texts: List[str]) -> np.ndarray:
        """Generate random embeddings as fallback."""
        # Generate deterministic embeddings based on text hash
        embeddings = []
        for text in texts:
            # Use hash to generate consistent embeddings for same text
            hash_val = hash(text)
            np.random.seed(abs(hash_val) % 2**32)
            embedding = np.random.randn(self.dimension)
            # Normalize
            embedding = embedding / np.linalg.norm(embedding)
            embeddings.append(embedding)
        return np.array(embeddings)

def create_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingModel:
    """Create embedding model - returns fallback for now."""
    return EmbeddingModel(model_name)