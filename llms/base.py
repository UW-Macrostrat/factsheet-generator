from enum import Enum
from abc import abstractmethod
from typing import List, Optional
from dataclasses import dataclass


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    role: MessageRole
    content: str
    additional_kwargs: dict

    def __str__(self) -> str:
        return f"{self.role.value}: {self.content}"


@dataclass
class Response:
    message: Message
    additional_kwargs: dict


@dataclass
class LLMMetadata:
    context_window: int
    model_name: Optional[str] = None


class BaseLLM:
    metadata: LLMMetadata

    @abstractmethod
    def chat(self, messages: list[Message], max_tokens: int) -> Response:
        """Chat endpoint for LLM."""

    @abstractmethod
    async def async_chat(self, messages: list[Message], max_tokens: int) -> Response:
        """Asynchronous chat endpoint for LLM."""
