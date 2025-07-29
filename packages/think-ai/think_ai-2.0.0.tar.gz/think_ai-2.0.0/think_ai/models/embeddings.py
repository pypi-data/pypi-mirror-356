"""Embedding models for vector generation."""

from abc import ABC, abstractmethod
from typing import List, Union, Optional
import numpy as np
import asyncio
from functools import lru_cache

from ..core.config import ModelConfig
from ..utils.logging import get_logger


logger = get_logger(__name__)


class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the embedding model."""
        pass
    
    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for a list of texts."""
        pass
    
    @abstractmethod
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of embeddings."""
        pass


class TransformerEmbeddings(EmbeddingModel):
    """Transformer-based embedding model using sentence-transformers."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.dimension = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the transformer model."""
        if self._initialized:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            
            # Load model in executor to avoid blocking
            self.model = await asyncio.get_event_loop().run_in_executor(
                None,
                SentenceTransformer,
                self.model_name
            )
            
            # Get embedding dimension
            self.dimension = self.model.get_sentence_embedding_dimension()
            
            self._initialized = True
            logger.info(f"Initialized embedding model: {self.model_name} (dim={self.dimension})")
            
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {e}")
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts."""
        if not self._initialized:
            await self.initialize()
        
        # Encode in executor to avoid blocking
        embeddings = await asyncio.get_event_loop().run_in_executor(
            None,
            self.model.encode,
            texts,
            None,  # prompts
            32,    # batch_size
            True,  # show_progress_bar
            None,  # output_value
            True,  # convert_to_numpy
            True,  # convert_to_tensor
            "cpu", # device
            True   # normalize_embeddings
        )
        
        return [embedding for embedding in embeddings]
    
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        embeddings = await self.embed_texts([text])
        return embeddings[0]
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.dimension or 384  # Default for MiniLM


class LocalEmbeddings(EmbeddingModel):
    """Local embedding model using smaller, quantized models."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize local embedding model."""
        if self._initialized:
            return
        
        try:
            import torch
            from transformers import AutoTokenizer, AutoModel
            
            # Load tokenizer
            self.tokenizer = await asyncio.get_event_loop().run_in_executor(
                None,
                AutoTokenizer.from_pretrained,
                self.config.model_name
            )
            
            # Load model with quantization if specified
            if self.config.quantization == "int4":
                from transformers import BitsAndBytesConfig
                
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True
                )
                
                self.model = await asyncio.get_event_loop().run_in_executor(
                    None,
                    AutoModel.from_pretrained,
                    self.config.model_name,
                    quantization_config,
                    torch.device(self.config.device)
                )
            else:
                self.model = await asyncio.get_event_loop().run_in_executor(
                    None,
                    AutoModel.from_pretrained,
                    self.config.model_name
                )
                self.model.to(self.config.device)
            
            self.model.eval()
            self._initialized = True
            logger.info(f"Initialized local embedding model: {self.config.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize local embedding model: {e}")
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts."""
        if not self._initialized:
            await self.initialize()
        
        import torch
        
        embeddings = []
        
        # Process in batches
        batch_size = 32
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            # Tokenize
            inputs = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.config.device)
            
            # Generate embeddings
            with torch.no_grad():
                outputs = await asyncio.get_event_loop().run_in_executor(
                    None,
                    self.model,
                    **inputs
                )
                
                # Mean pooling
                attention_mask = inputs['attention_mask']
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
                
                batch_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                
                # Normalize
                batch_embeddings = torch.nn.functional.normalize(batch_embeddings, p=2, dim=1)
                
                embeddings.extend(batch_embeddings.cpu().numpy())
        
        return embeddings
    
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        embeddings = await self.embed_texts([text])
        return embeddings[0]
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        # Common dimensions for popular models
        model_dimensions = {
            "sentence-transformers/all-MiniLM-L6-v2": 384,
            "sentence-transformers/all-mpnet-base-v2": 768,
            "BAAI/bge-small-en-v1.5": 384,
            "BAAI/bge-base-en-v1.5": 768,
            "BAAI/bge-large-en-v1.5": 1024,
        }
        
        return model_dimensions.get(self.config.model_name, 768)


class CachedEmbeddings(EmbeddingModel):
    """Embedding model with caching for efficiency."""
    
    def __init__(self, base_model: EmbeddingModel, cache_size: int = 10000):
        self.base_model = base_model
        self.cache_size = cache_size
        self._cache = {}
    
    async def initialize(self) -> None:
        """Initialize the base model."""
        await self.base_model.initialize()
    
    @lru_cache(maxsize=10000)
    def _hash_text(self, text: str) -> str:
        """Create a hash for caching."""
        import hashlib
        return hashlib.md5(text.encode()).hexdigest()
    
    async def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding with caching."""
        text_hash = self._hash_text(text)
        
        if text_hash in self._cache:
            return self._cache[text_hash]
        
        embedding = await self.base_model.embed_text(text)
        
        # Add to cache with size limit
        if len(self._cache) >= self.cache_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[text_hash] = embedding
        return embedding
    
    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings with caching."""
        embeddings = []
        uncached_texts = []
        uncached_indices = []
        
        # Check cache
        for i, text in enumerate(texts):
            text_hash = self._hash_text(text)
            if text_hash in self._cache:
                embeddings.append(self._cache[text_hash])
            else:
                embeddings.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # Generate embeddings for uncached texts
        if uncached_texts:
            new_embeddings = await self.base_model.embed_texts(uncached_texts)
            
            # Update results and cache
            for i, (idx, text) in enumerate(zip(uncached_indices, uncached_texts)):
                embeddings[idx] = new_embeddings[i]
                text_hash = self._hash_text(text)
                
                if len(self._cache) >= self.cache_size:
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                
                self._cache[text_hash] = new_embeddings[i]
        
        return embeddings
    
    def get_dimension(self) -> int:
        """Get embedding dimension from base model."""
        return self.base_model.get_dimension()


def create_embedding_model(
    model_type: str = "transformer",
    model_name: Optional[str] = None,
    config: Optional[ModelConfig] = None,
    use_cache: bool = True
) -> EmbeddingModel:
    """Factory function to create embedding models."""
    
    if model_type == "transformer":
        base_model = TransformerEmbeddings(model_name or "sentence-transformers/all-MiniLM-L6-v2")
    elif model_type == "local":
        if not config:
            raise ValueError("Config required for local embeddings")
        base_model = LocalEmbeddings(config)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    if use_cache:
        return CachedEmbeddings(base_model)
    
    return base_model