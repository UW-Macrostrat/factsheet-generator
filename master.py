import asyncio
import logging
import os
import aiofiles
import argparse

import grpc
import workerserver_pb2
import workerserver_pb2_grpc

FILE_DIR = "data/raw_text/"


async def read_file(queue: asyncio.Queue, consumer_count: int) -> None:
    for filename in os.listdir(FILE_DIR):
        file_path = os.path.join(FILE_DIR, filename)

        async with aiofiles.open(file_path, mode="r") as file:
            content = await file.read()

            await queue.put(file_path)

    for _ in range(consumer_count):
        await queue.put(None)

    logging.info("All files have been read.")


async def store_file(
    ip_address: str, queue: asyncio.Queue, strat_names: list[str] = ["test"]
) -> None:
    async with grpc.aio.insecure_channel(f"{ip_address}:50051") as channel:
        stub = workerserver_pb2_grpc.WorkerServerStub(channel)

        await stub.SetStratNames(
            workerserver_pb2.StratNameRequest(strat_names=strat_names)
        )

        while True:
            item = await queue.get()

            if item == None:
                break

            response = await stub.StoreFile(workerserver_pb2.FileDataRequest(data=item))

            if response.error:
                print(response.error)

            queue.task_done()

    logging.info(f"All {ip_address} files have been stored")


async def main(address_list: list[str]) -> None:
    queue = asyncio.Queue()

    read_task = read_file(queue, len(address_list))
    store_tasks = [store_file(port, queue) for port in address_list]

    await asyncio.gather(read_task, *store_tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("address_list", nargs="+")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(args.address_list))
