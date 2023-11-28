import grpc
import llm_pb2
import llm_pb2_grpc

import time
from sys import argv

import numpy as np

with grpc.insecure_channel(f"localhost:{argv[1]}") as channel:
    stub = llm_pb2_grpc.LLMServerStub(channel)
    
    start = time.perf_counter()
    
    # message = llm_pb2.ChatRequest(
    #     system_text="You are a helpful AI assistant.",
    #     user_text="Test query?",
    # )
    # response = stub.ChatCompletion(message)
    
    response = stub.Embedding(llm_pb2.EmbeddingRequest(text="test sequence"))
    
    end = time.perf_counter()
    arr = np.array(response.embedding, dtype=np.float32)
    
    print("time taken:", round(end - start, 3))
