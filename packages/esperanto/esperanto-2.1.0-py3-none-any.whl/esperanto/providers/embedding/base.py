"""Base embedding model interface."""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from esperanto.common_types import Model


@dataclass
class EmbeddingModel(ABC):
    """Base class for all embedding models."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    organization: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    _config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize configuration after dataclass initialization."""
        # Initialize config with default values
        self._config = {
            "model_name": self.model_name,
        }

        # Update with any provided config
        if hasattr(self, "config") and self.config:
            self._config.update(self.config)

            # Update instance attributes from config
            for key, value in self._config.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    @abstractmethod
    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Create embeddings for the given texts.

        Args:
            texts: List of texts to create embeddings for.
            **kwargs: Additional arguments to pass to the embedding API.

        Returns:
            List of embeddings, one for each input text.
        """
        pass

    @abstractmethod
    async def aembed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Create embeddings for the given texts asynchronously.

        Args:
            texts: List of texts to create embeddings for.
            **kwargs: Additional arguments to pass to the embedding API.

        Returns:
            List of embeddings, one for each input text.
        """
        pass

    def get_model_name(self) -> str:
        """Get the model name.

        Returns:
            str: The model name.
        """
        # First try to get from config
        model_name = self._config.get("model_name")
        if model_name:
            return model_name

        # If not in config, use default
        return self._get_default_model()

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for embedding.
        
        Based on Microsoft Azure OpenAI best practices but useful for all providers.
        Normalizes spacing, removes unwanted characters, and cleans up punctuation.
        
        Args:
            text: The text to clean and normalize.
            
        Returns:
            The cleaned and normalized text.
        """
        # Normalize spacing - replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove spaces before punctuation
        text = re.sub(r'\s+([.,])', r'\1', text)
        
        # Remove repeated punctuation (multiple dots)
        text = re.sub(r'\.{2,}', '.', text)
        
        # Replace newlines and carriage returns with spaces
        text = re.sub(r'[\n\r]+', ' ', text)
        
        # Strip to clean up after replacements
        return text.strip()

    @property
    @abstractmethod
    def provider(self) -> str:
        """Get the provider name."""
        pass

    @property
    @abstractmethod
    def models(self) -> List[Model]:
        """List all available models for this provider."""
        pass

    @abstractmethod
    def _get_default_model(self) -> str:
        """Get the default model name.

        Returns:
            str: The default model name.
        """
        pass
