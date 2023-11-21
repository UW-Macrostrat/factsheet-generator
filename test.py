import grpc
import llm_pb2
import llm_pb2_grpc

import time
from sys import argv

with grpc.insecure_channel(f"localhost:{argv[1]}") as channel:
    stub = llm_pb2_grpc.LLMServerStub(channel)
    
    start = time.perf_counter()
    
    message = llm_pb2.ChatRequest(
        system_text="You are a helpful AI assistant.",
        user_text="How can I get a girlfriend?",
    )
    response = stub.ChatCompletion(message)
    
    end = time.perf_counter()
    
    print(response.text)
    
    print("time taken:", round(end - start, 3))
