from sys import argv
from llama_cpp import Llama
import asyncio

import grpc
import llm_pb2
import llm_pb2_grpc
import time

class LLM(llm_pb2_grpc.LLMServerServicer):
    def __init__(self, llm: Llama):
        self.llama = llm

    async def ChatCompletion(
        self, request: llm_pb2.ChatRequest, context: grpc.ServicerContext
    ) -> llm_pb2.ChatResponse:
        start_time = time.monotonic()
        
        messages = [
            {"role": "system", "content": request.system_text},
            {"role": "user", "content": request.user_text},
        ]

        output = self.llama.create_chat_completion(messages, temperature=0)

        elapsed_time = time.monotonic() - start_time
        time_remaining = 30 - elapsed_time
        if time_remaining > 0:
            await asyncio.sleep(time_remaining)
        
        return llm_pb2.ChatResponse(text=output["choices"][0]["message"]["content"])


async def serve(port: int) -> None:
    llama = Llama(model_path="./models/openhermes-2.5-mistral-7b.Q4_K_M.gguf")

    server = grpc.aio.server()
    llm_pb2_grpc.add_LLMServerServicer_to_server(LLM(llama), server)
    listen_addr = f"[::]:{port}"
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    port = argv[1]
    asyncio.run(serve(port))
