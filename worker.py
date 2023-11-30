import asyncio
import logging
import sys
import traceback

import grpc
import workerserver_pb2
import workerserver_pb2_grpc

import psycopg
from psycopg_pool import AsyncConnectionPool
from pgvector.psycopg import register_vector_async

import torch
import aiohttp
import random
import numpy as np
from numpy.typing import NDArray

import preprocessing
from database_utils import retrieve_chunks, insert_chunk, store_facts

from embeddings.huggingface import HuggingFaceEmbedding

conninfo = "dbname=vector_db host=postgres user=admin password=admin port=5432"


class Worker(workerserver_pb2_grpc.WorkerServerServicer):
    def __init__(self):
        if torch.backends.mps.is_available():
            active_device = torch.device("mps")
        elif torch.cuda.is_available():
            active_device = torch.device("cuda", 0)
        else:
            active_device = torch.device("cpu")

        self.embedding = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en",
            device=active_device,
            context_length=512,
            instruction="Represent this sentence for searching relevant passages: ",
        )

    async def set_connection(self, conn: psycopg.AsyncConnection) -> None:
        await register_vector_async(conn)
        self.conn = conn

    async def generate_embedding(
        self, text: str, is_query: bool
    ) -> NDArray[np.float32]:
        # await asyncio.sleep(0.1)
        return np.array([0, 0, 0], dtype=np.float32)
        # return self.embedding.get_text_embedding(text, is_query)

    async def generate_response(self, query: str, context: list[str]) -> str:
        return query + str(context)

    async def StoreFile(
        self,
        request: workerserver_pb2.FileDataRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse:
        try:
            text = request.document_text
            text = preprocessing.remove_newlines(text)
            split_text = preprocessing.split_by_sentence(text)
            split_text = preprocessing.remove_short_sentences(split_text)

            token_count = [len(self.embedding.tokenizer.encode(s)) for s in split_text]

            chunk_size = self.embedding.context_length
            chunks = []
            current_chunk = []
            current_tokens = 0
            for sentence, token in zip(split_text, token_count):
                if current_tokens + token >= chunk_size:
                    chunks.append(". ".join(current_chunk) + ".")
                    current_chunk = []
                    current_tokens = 0

                if token > chunk_size:
                    continue

                current_chunk.append(sentence)
                current_tokens += token + 1

            if len(current_chunk) > 0:
                chunks.append(". ".join(chunks) + ".")

            async def compute_chunks(chunk_text: str) -> None:
                embedding = await self.generate_embedding(chunk_text, False)
                await insert_chunk(self.conn, chunk_text, embedding)

            tasks = [compute_chunks(c) for c in chunks]
            await asyncio.gather(*tasks)

            return workerserver_pb2.ErrorResponse()

        except:
            return workerserver_pb2.ErrorResponse(error=traceback.format_exc())

    async def SetQueries(
        self,
        request: workerserver_pb2.QueryRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse:
        if len(request.queries) != len(request.categories):
            return workerserver_pb2.ErrorResponse(
                error="Length of queries and categories must be equal"
            )

        self.queries = request.queries
        self.categories = request.categories

        return workerserver_pb2.ErrorResponse()

    async def GenerateFacts(
        self,
        request: workerserver_pb2.FactRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse():
        if not self.queries:
            return workerserver_pb2.ErrorResponse("Error: query list has not been set.")

        try:
            facts = []
            for query in self.queries:
                query = query.format(strat_name=request.strat_name)
                query_embedding = await self.generate_embedding(query, True)

                chunks = await retrieve_chunks(
                    self.conn,
                    query_embedding,
                    strat_name=request.strat_name,
                    must_include=True,
                    top_k=20,
                )

                logging.info("Chunks %s, query %s", chunks, query)

                facts.append(
                    await self.generate_response(query, [c[0] for c in chunks])
                )

            await store_facts(self.conn, request.strat_name, self.categories, facts)

            return workerserver_pb2.ErrorResponse()

        except:
            return workerserver_pb2.ErrorResponse(error=traceback.format_exc())


async def serve() -> None:
    server = grpc.aio.server()

    async with await psycopg.AsyncConnection.connect(
        conninfo=conninfo, autocommit=True
    ) as conn:
        worker = Worker()
        await worker.set_connection(conn)

        workerserver_pb2_grpc.add_WorkerServerServicer_to_server(worker, server)

        listen_addr = "[::]:50051"
        server.add_insecure_port(listen_addr)

        logging.info("Starting server on %s", listen_addr)
        await server.start()
        await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
