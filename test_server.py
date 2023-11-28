from sys import argv
from llama_cpp import Llama
import asyncio

import grpc
import llm_pb2
import llm_pb2_grpc

from embeddings.huggingface import HuggingFaceEmbedding


class LLM(llm_pb2_grpc.LLMServerServicer):
    def __init__(self, llm: Llama):
        # self.llama = llm
        self.bge = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en",
            device="cuda:0",
            instruction="Represent this sentence for searching relevant passages: ",
        )

    async def ChatCompletion(
        self, request: llm_pb2.ChatRequest, context: grpc.ServicerContext
    ) -> llm_pb2.ChatResponse:
        messages = [
            {"role": "system", "content": request.system_text},
            {"role": "user", "content": request.user_text},
        ]

        delay = asyncio.create_task(asyncio.sleep(30))
        await asyncio.sleep(0)

        output = self.llama.create_chat_completion(messages, temperature=0)

        await delay

        return llm_pb2.ChatResponse(text=output["choices"][0]["message"]["content"])

    async def Embedding(
        self, request: llm_pb2.EmbeddingRequest, context: grpc.ServicerContext
    ) -> llm_pb2.EmbeddingResponse:
        embedding = self.bge.get_text_embedding(
            request.text, is_query=request.is_query
        )[0]
        
        return llm_pb2.EmbeddingResponse(embedding=embedding)


async def serve(port: int) -> None:
    # llama = Llama(
    #     model_path="./models/openhermes-2.5-mistral-7b.Q4_K_M.gguf", n_ctx=4000
    # )
    llama = None

    server = grpc.aio.server()
    llm_pb2_grpc.add_LLMServerServicer_to_server(LLM(llama), server)
    listen_addr = f"[::]:{port}"
    server.add_insecure_port(listen_addr)
    print("Starting server on", listen_addr)    
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    port = argv[1]
    asyncio.run(serve(port))
