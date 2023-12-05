import os
import csv
import time
import json
import logging

import asyncio
import aiofiles
from dataclasses import dataclass

import psycopg

import grpc
import workerserver_pb2
import workerserver_pb2_grpc

DATA_DIR = os.environ["DATA_DIR"]
DB_HOST = os.environ["DB_HOST"]
STRAT_NAME_DIR = "/data/strat_names.csv"
QUERY_DIR = "/data/query.csv"
EMBED_DIM = 768 
CONNINFO = f"dbname=vector_db host={DB_HOST} user=admin password=admin port=5432"

@dataclass
class Progress():
    output: str = "MASTER: Finished %s."
    current: int = 0
    
    def increment(self):
        self.current += 1
        if self.current % 10 == 0:
            logging.info(self.output, self.current)

async def read_file(queue: asyncio.Queue, consumer_count: int) -> None:
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        
        async with aiofiles.open(file_path, mode="r") as file:
            content = await file.read()

            await queue.put(content)
            
        await asyncio.sleep(0) # force context switch

    for _ in range(consumer_count):
        await queue.put(None)

    logging.info("MASTER: All files have been read.")


async def store_file(host: str, queue: asyncio.Queue, progress: Progress) -> None:
    async with grpc.aio.insecure_channel(f"{host}:50051") as channel:
        stub = workerserver_pb2_grpc.WorkerServerStub(channel)
        
        while True:
            item = await queue.get()
            if item == None:
                break

            response = await stub.StoreFile(
                workerserver_pb2.FileDataRequest(document_text=item)
            )

            if response.error:
                raise Exception(response.error)

            queue.task_done()
            progress.increment()

    logging.info("MASTER: Worker %s has finished storing files.", host)


async def generate_facts(host_list: list[str]) -> None:
    categories = []
    queries = []
    async with await psycopg.AsyncConnection.connect(
        conninfo=CONNINFO, autocommit=True
    ) as conn:
        with open(QUERY_DIR, mode="r") as query_file:
            query_reader = csv.reader(query_file)

            for row in query_reader:
                await conn.execute(
                    """
                        ALTER TABLE factsheets
                        ADD COLUMN {category} text,
                        ADD COLUMN {category}_context text;    
                    """.format(
                        category=row[0]
                    )
                )
                categories.append(row[0])
                queries.append(row[1])

    logging.info("Factsheets table updated")

    queue = asyncio.Queue()
    with open(STRAT_NAME_DIR, mode="r") as name_file:
        strat_names = name_file.readlines()
        for name in strat_names:
            # may want to change to async producer to save memory
            queue.put_nowait(name.strip())

    tasks = [fact_worker_task(host, queue, categories, queries) for host in host_list]

    await asyncio.gather(*tasks)

    logging.info("MASTER: Factsheet has been generated.")


async def fact_worker_task(
    host: str, queue: asyncio.Queue, categories: list[str], queries: list[str]
) -> None:
    async with grpc.aio.insecure_channel(f"{host}:50051") as channel:
        stub = workerserver_pb2_grpc.WorkerServerStub(channel)

        while not queue.empty():
            item = await queue.get()

            if item == None:
                break

            await stub.SetQueries(
                workerserver_pb2.QueryRequest(categories=categories, queries=queries)
            )

            response = await stub.GenerateFacts(
                workerserver_pb2.FactRequest(strat_name=item)
            )

            if response.error:
                raise Exception(response.error)

            queue.task_done()

    logging.info("MASTER: Worker %s has finished generating facts.", host)


async def init_db():
    async with await psycopg.AsyncConnection.connect(
        conninfo=CONNINFO, autocommit=True
    ) as conn:
        await conn.execute(
            """
                CREATE TABLE IF NOT EXISTS chunk_data (
                    chunk_id INT GENERATED ALWAYS AS IDENTITY,
                    chunk_text text NOT NULL,
                    embedding vector({embed_dim}),
                    PRIMARY KEY(chunk_id)
                );
            """.format(
                embed_dim=EMBED_DIM
            )
        )

        await conn.execute(
            """
                CREATE TABLE IF NOT EXISTS factsheets (
                    strat_name varchar(100),
                    PRIMARY KEY(strat_name)
                );
            """,
        )

async def connect_worker(server_address: str, max_attempts: int = 5) -> None:
    attempt = 1
    while True:
        try:
            async with grpc.aio.insecure_channel(f"{server_address}:50051") as channel:
                stub = workerserver_pb2_grpc.WorkerServerStub(channel)
                resp = await stub.Heartbeat(workerserver_pb2.StatusRequest())
                if resp.status:
                    logging.info("MASTER: Connected to %s successfully.", server_address)
                    return
                else:
                    logging.info("MASTER: Worker server at %s is not ready yet.", server_address)
        except grpc.RpcError:
            logging.info("MASTER: Attempt %s: Failed to connect to %s.", attempt, server_address)
            await asyncio.sleep(2)

        attempt += 1

async def connect_db() -> None:
    attempt = 1
    while True:
        try:
            async with await psycopg.AsyncConnection.connect(conninfo=CONNINFO):
                return
        except psycopg.OperationalError:
            logging.info("MASTER: Attempt %s: Failed to connect to vector database.")
            await asyncio.sleep(2)
            
        attempt += 1

async def main(worker_list: list[str]) -> None:
    await asyncio.gather(*[connect_worker(worker) for worker in worker_list], connect_db())

    await init_db()

    start = time.time()

    queue = asyncio.Queue()

    progress = Progress("MASTER: Generated embeddings for %s files.")
    read_task = read_file(queue, len(worker_list))
    store_tasks = [store_file(port, queue, progress) for port in worker_list]

    await asyncio.gather(read_task, *store_tasks)

    end = time.time()
    logging.info("MASTER: Finished storing files in %s seconds.", end - start)

    start = time.time()

    await generate_facts(worker_list)

    end = time.time()
    logging.info("MASTER: Finished generated facts in %s seconds.", end - start)


if __name__ == "__main__":
    workers = json.loads(os.environ["WORKER_NAMES"])
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(workers))
