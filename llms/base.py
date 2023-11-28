from enum import Enum
from abc import abstractmethod

from pydantic import BaseModel


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message:
    role: MessageRole
    content: str
    additional_kwargs: dict

    def __str__(self) -> str:
        return f"{self.role.value}: {self.content}"


class Response:
    message: Message
    additional_kwargs: dict


class LLMMetadata(BaseModel):
    model_name: str
    context_window: int
    max_output: int


class BaseLLM:
    metadata: LLMMetadata

    @abstractmethod
    def chat(self, messages: list[Message]) -> Response:
        """Chat endpoint for LLM."""