import numpy as np
from numpy.typing import NDArray
from transformers import AutoTokenizer, AutoModel
import torch
from embeddings.base import BaseEmbedding
import numpy as np
from numpy.typing import NDArray


class HuggingFaceEmbedding(BaseEmbedding):
    def __init__(
        self, model_name: str, device: str, context_length: int, instruction: str = ""
    ) -> None:
        super().__init__()
        self.model_name = model_name
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name, device_map=self.device)
        self.model.eval()
        self.embed_dim = self.model.config.hidden_size
        self.instruction = instruction
        self.context_length = context_length

    def get_text_embedding(
        self,
        text: str,
        is_query: bool = False,
    ) -> NDArray[np.float32]:
        if is_query:
            # for s2p(short query to long passage) retrieval task, add an instruction to query (not add instruction for passages)
            encoded_input = self.tokenizer(
                self.instruction + text,
                padding=True,
                truncation=True,
                return_tensors="pt",
            )
        else:
            encoded_input = self.tokenizer(
                text, padding=True, truncation=True, return_tensors="pt"
            )

        encoded_input.to(self.device)

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Perform pooling. In this case, cls pooling.
            sentence_embeddings = model_output[0][:, 0]

        # normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(
            sentence_embeddings, p=2, dim=1
        )

        # remove dummy dimensions
        sentence_embeddings = torch.squeeze(sentence_embeddings)

        return sentence_embeddings.cpu().numpy().astype("float32")

    def get_batch_embedding(
        self,
        texts: list[str],
        is_query: bool = False,
    ) -> NDArray[np.float32]:
        if is_query:
            # for s2p(short query to long passage) retrieval task, add an instruction to query (not add instruction for passages)
            encoded_input = self.tokenizer(
                [self.instruction + t for t in texts],
                padding=True,
                truncation=True,
                return_tensors="pt",
            )
        else:
            encoded_input = self.tokenizer(
                texts, padding=True, truncation=True, return_tensors="pt"
            )

        encoded_input.to(self.device)

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            # Perform pooling. In this case, cls pooling.
            sentence_embeddings = model_output[0][:, 0]

        # normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(
            sentence_embeddings, p=2, dim=1
        )

        return sentence_embeddings.cpu().numpy().astype("float32")
