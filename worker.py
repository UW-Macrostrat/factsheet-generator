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

import random
import numpy as np

from database_utils import retrieve_chunks, insert_chunk

conninfo = "dbname=vector_db host=postgres user=admin password=admin port=5432"


class Worker(workerserver_pb2_grpc.WorkerServerServicer):
    async def __init__(self, conn: psycopg.AsyncConnection):
        await register_vector_async(conn)
        self.conn = conn

    async def StoreFile(
        self,
        request: workerserver_pb2.FileDataRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse:
        # if not self.strat_names:
        #     return workerserver_pb2.ErrorResponse(
        #         error="Strat Names have not been set."
        #     )

        try:
            await asyncio.sleep(1)

            text = request.data
            embedding = generate_embedding(text)
            await insert_chunk(self.conn, text, embedding)

            return workerserver_pb2.ErrorResponse()

        except:
            return workerserver_pb2.ErrorResponse(error=traceback.format_exc())

    async def SetQueries(
        self,
        request: workerserver_pb2.QueryRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse:
        self.queries = request.queries

        return workerserver_pb2.ErrorResponse()

    async def GenerateFacts(
        self,
        request: workerserver_pb2.FactRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse():
        if not self.queries:
            return workerserver_pb2.ErrorResponse("Error: query list has not been set.")

        facts = []
        for query in self.queries.values():
            query_embedding = generate_embedding(query)

            chunks = await retrieve_chunks(
                self.conn,
                query_embedding,
                strat_name=request.strat_name,
                must_include=True,
                top_k=20,
            )

            facts.append(generate_response(query, [c[0] for c in chunks]))
            
        

    # async def SetStratNames(
    #     self,
    #     request: workerserver_pb2.StratNameRequest,
    #     context: grpc.aio.ServicerContext,
    # ) -> workerserver_pb2.ErrorResponse:
    #     self.strat_names = request.strat_names

    #     return workerserver_pb2.ErrorResponse()


def generate_embedding(text: str):
    return np.array(random.sample(range(10), 3))  # dummy code


def generate_response(query: str, context: list[str]) -> str:
    return "test"


async def serve() -> None:
    server = grpc.aio.server()

    async with AsyncConnectionPool(conninfo=conninfo) as pool:
        workerserver_pb2_grpc.add_WorkerServerServicer_to_server(
            await Worker(pool), server
        )
        listen_addr = "[::]:50051"
        server.add_insecure_port(listen_addr)
        logging.info("Starting server on %s", listen_addr)
        await server.start()
        await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
