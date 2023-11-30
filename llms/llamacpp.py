import json
import aiohttp
from llms.base import BaseLLM, LLMMetadata, Message, Response, MessageRole


class LlamaCPPLLM(BaseLLM):
    """llama.cpp server wrapper"""

    def __init__(
        self,
        server_address: str,
        context_window: int,
    ) -> None:
        super().__init__()

        self.server_address = server_address
        self.metadata = LLMMetadata(
            context_window=context_window,
        )
        self.session = aiohttp.ClientSession()

    async def async_chat(self, messages: list[Message], max_tokens: int) -> Response:
        
        messages = [m.to_json() for m in messages]
        
        async with self.session.post(
            f"http://{self.server_address}/v1/chat/completions",
            data=json.dumps(
                {
                    "messages": messages,
                    "max_tokens": max_tokens,
                }
            ),
        ) as resp:
            output = await resp.json()
            return Response(message=Message(role=MessageRole.ASSISTANT, content=output["choices"][0]["message"]["content"]))
