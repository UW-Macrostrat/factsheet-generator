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

conninfo = "dbname=vector_db host=postgres user=admin password=admin port=5432"


def generate_embedding(text: str):
    return np.array(random.sample(range(10), 3))  # dummy code


class Worker(workerserver_pb2_grpc.WorkerServerServicer):
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def insert_to_db(self, text: str) -> None:
        async with self.pool.connection() as conn:
            await register_vector_async(conn)

            rand_vector = generate_embedding(text)

            await conn.execute(
                """
                    INSERT INTO chunk_data(chunk_text, embedding)
                    VALUES(%s, %s);
                """,
                (
                    text,
                    rand_vector,
                ),
            )

            await conn.commit()

    async def StoreFile(
        self,
        request: workerserver_pb2.FileDataRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse:
        if not self.strat_names:
            return workerserver_pb2.ErrorResponse(
                error="Strat Names have not been set."
            )

        try:
            await asyncio.sleep(1)

            await self.insert_to_db(request.data)

            return workerserver_pb2.ErrorResponse()

        except:
            return workerserver_pb2.ErrorResponse(error=traceback.format_exc())

    async def SetStratNames(
        self,
        request: workerserver_pb2.StratNameRequest,
        context: grpc.aio.ServicerContext,
    ) -> workerserver_pb2.ErrorResponse:
        self.strat_names = request.strat_names

        return workerserver_pb2.ErrorResponse()

    # async def GenerateFacts(
    #     self,
    #     request: workerserver_pb2.FactRequest,
    #     context: grpc.aio.ServicerContext,
    # ):


async def serve() -> None:
    server = grpc.aio.server()

    async with AsyncConnectionPool(conninfo=conninfo) as pool:
        workerserver_pb2_grpc.add_WorkerServerServicer_to_server(Worker(pool), server)
        listen_addr = f"[::]:50051"
        server.add_insecure_port(listen_addr)
        logging.info("Starting server on %s", listen_addr)
        await server.start()
        await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
