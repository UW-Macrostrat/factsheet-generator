import os
import csv
import time
import logging

import asyncio
import aiofiles
import argparse

import psycopg

import grpc
import workerserver_pb2
import workerserver_pb2_grpc

DATA_DIR = "data/dev/"
STRAT_NAME_DIR = "data/strat_names.csv"
QUERY_DIR = "data/query.csv"
EMBED_DIM = 3  # TODO change


async def read_file(queue: asyncio.Queue, consumer_count: int) -> None:
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)

        async with aiofiles.open(file_path, mode="r") as file:
            content = await file.read()

            await queue.put(content)

    for _ in range(consumer_count):
        await queue.put(None)

    logging.info("All files have been read.")


async def store_file(
    host: str, queue: asyncio.Queue, strat_names: list[str] = ["test"]
) -> None:
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

    logging.info("Worker %s has finished storing files.", host)


async def generate_facts(host_list: list[str]) -> None:
    conninfo = "dbname=vector_db host=postgres user=admin password=admin port=5432"

    categories = []
    queries = []
    with psycopg.connect(conninfo=conninfo, autocommit=True) as conn:
        with open(QUERY_DIR, mode="r") as query_file:
            query_reader = csv.reader(query_file)

            for row in query_reader:
                conn.execute(
                    """
                        ALTER TABLE factsheets
                        ADD COLUMN {category} text;    
                    """.format(
                        category=row[0]
                    )
                )
                categories.append(row[0])
                queries.append(row[1])

    queue = asyncio.Queue()
    with open(STRAT_NAME_DIR, mode="r") as name_file:
        strat_names = name_file.readlines()
        for name in strat_names:
            # may want to change to async producer to save memory
            queue.put_nowait(name.strip())

    tasks = [fact_worker_task(host, queue, categories, queries) for host in host_list]

    await asyncio.gather(*tasks)

    logging.info("Factsheet has been generated.")


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

    logging.info("Worker %s has finished generating facts.", host)


def init_db():
    conninfo = "dbname=vector_db host=postgres user=admin password=admin port=5432"
    with psycopg.connect(conninfo=conninfo, autocommit=True) as conn:
        conn.execute(
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

        conn.execute(
            """
                CREATE TABLE IF NOT EXISTS factsheets (
                    strat_name varchar(100),
                    PRIMARY KEY(strat_name)
                );
            """,
        )


async def main(worker_list: list[str]) -> None:
    time.sleep(10)  # wait for db initialize
    init_db()

    start = time.time()

    queue = asyncio.Queue()

    read_task = read_file(queue, len(worker_list))
    store_tasks = [store_file(port, queue) for port in worker_list]

    await asyncio.gather(read_task, *store_tasks)

    end = time.time()
    logging.info("Finished storing files in %s seconds.", end - start)

    start = time.time()

    await generate_facts(worker_list)

    end = time.time()
    logging.info("Finished generated facts in %s seconds.", end - start)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("worker_list", nargs="+")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(args.worker_list))
