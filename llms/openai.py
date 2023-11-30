from openai import OpenAI
from llms.base import BaseLLM, LLMMetadata, Message, Response


class OpenAILLM(BaseLLM):
    def __init__(
        self,
        model_name: str,
        context_window: int,
        max_output: int,
    ) -> None:
        super().__init__()

        self.metadata = LLMMetadata(
            model_name=model_name,
            context_window=context_window,
            max_output=max_output,
        )
        self.client = OpenAI()

    def chat(self, messages: list[Message]) -> Response:
        response = self.client.chat.completions.create(
            model=self.metadata.model_name,
            messages=[{"role": m.role, "content": m.content} for m in messages],
        )
