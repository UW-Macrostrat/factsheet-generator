from abc import abstractmethod
from numpy.typing import NDArray
import numpy as np


class BaseEmbedding:
    model_name: str
    embed_dim: int

    @abstractmethod
    def get_text_embedding(self, text: str) -> NDArray[np.float32]:
        """Embed input sequence of text."""
