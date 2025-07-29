"""Parallel model pool for concurrent inference."""

import asyncio
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import time

from ..core.config import ModelConfig
from ..consciousness.principles import ConstitutionalAI
from .language_model import LanguageModel, GenerationConfig, ModelResponse
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ModelInstance:
    """A single model instance in the pool."""
    id: int
    model: LanguageModel
    busy: bool = False
    last_used: float = 0.0


class ParallelModelPool:
    """Pool of language models for parallel processing."""
    
    def __init__(self, config: ModelConfig, constitutional_ai: Optional[ConstitutionalAI] = None, pool_size: int = 3):
        self.config = config
        self.constitutional_ai = constitutional_ai
        self.pool_size = pool_size
        self.instances: List[ModelInstance] = []
        self._initialized = False
        self._lock = asyncio.Lock()
        
    async def initialize(self) -> None:
        """Initialize the model pool."""
        if self._initialized:
            return
            
        logger.info(f"Initializing parallel model pool with {self.pool_size} instances...")
        
        # Create model instances
        initialization_tasks = []
        for i in range(self.pool_size):
            instance = ModelInstance(
                id=i,
                model=LanguageModel(self.config, self.constitutional_ai)
            )
            self.instances.append(instance)
            initialization_tasks.append(instance.model.initialize())
        
        # Initialize all models in parallel
        await asyncio.gather(*initialization_tasks)
        
        self._initialized = True
        logger.info(f"Model pool initialized with {len(self.instances)} instances")
    
    async def get_available_instance(self) -> Optional[ModelInstance]:
        """Get an available model instance."""
        async with self._lock:
            # Find least recently used available instance
            available = [inst for inst in self.instances if not inst.busy]
            if not available:
                return None
            
            # Sort by last used time
            available.sort(key=lambda x: x.last_used)
            instance = available[0]
            instance.busy = True
            instance.last_used = time.time()
            return instance
    
    async def release_instance(self, instance: ModelInstance) -> None:
        """Release a model instance back to the pool."""
        async with self._lock:
            instance.busy = False
    
    async def generate(
        self,
        prompt: str,
        generation_config: Optional[GenerationConfig] = None,
        system_prompt: Optional[str] = None,
        timeout: float = 60.0
    ) -> ModelResponse:
        """Generate text using an available model instance."""
        # Wait for an available instance
        wait_start = time.time()
        instance = None
        
        while instance is None:
            instance = await self.get_available_instance()
            if instance is None:
                if time.time() - wait_start > timeout:
                    raise TimeoutError("No model instance available within timeout")
                await asyncio.sleep(0.1)
        
        try:
            logger.info(f"Using model instance {instance.id} for generation")
            result = await instance.model.generate(prompt, generation_config, system_prompt)
            return result
        finally:
            await self.release_instance(instance)
    
    async def generate_batch(
        self,
        prompts: List[str],
        generation_config: Optional[GenerationConfig] = None,
        system_prompt: Optional[str] = None
    ) -> List[ModelResponse]:
        """Generate responses for multiple prompts in parallel."""
        tasks = []
        for prompt in prompts:
            task = self.generate(prompt, generation_config, system_prompt)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error generating response for prompt {i}: {result}")
                # Create error response
                responses.append(ModelResponse(
                    text=f"Error: {str(result)}",
                    tokens_generated=0,
                    generation_time=0.0,
                    metadata={"error": True}
                ))
            else:
                responses.append(result)
        
        return responses
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get current status of the model pool."""
        busy_count = sum(1 for inst in self.instances if inst.busy)
        return {
            "total_instances": len(self.instances),
            "busy_instances": busy_count,
            "available_instances": len(self.instances) - busy_count,
            "initialized": self._initialized
        }