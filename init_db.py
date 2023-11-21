import psycopg
import time
import logging

conninfo = "dbname=vector_db host=postgres user=admin password=admin port=5432"

logging.basicConfig(level=logging.INFO)
time.sleep(10)

with psycopg.connect(conninfo=conninfo) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
                CREATE EXTENSION IF NOT EXISTS vector;
            """
        )

        cur.execute(
            """
                CREATE TABLE chunk_data (
                    chunk_id INT GENERATED ALWAYS AS IDENTITY,
                    chunk_text text NOT NULL,
                    embedding vector(3),
                    PRIMARY KEY(chunk_id)
                );
            """
        )

        # cur.execute(
        #     """
        #         CREATE TABLE strat_name_lookup (
        #             strat_name_id INT GENERATED ALWAYS AS IDENTITY,
        #             strat_name varchar(100),
        #             PRIMARY KEY(strat_name_id)
        #         );
        #     """
        # )

        # cur.execute(
        #     """
        #         CREATE TABLE chunk_lookup (
        #             strat_name_id INT,
        #             chunk_id INT,
        #             PRIMARY KEY(strat_name_id, chunk_id),
        #             FOREIGN KEY(strat_name_id) 
        #                 REFERENCES strat_name_lookup(strat_name_id),
        #             FOREIGN KEY(chunk_id) 
        #                 REFERENCES chunk_data(chunk_id)
        #         );
        #     """
        # )

        # cur.execute(
        #     """
        #         CREATE TABLE factsheets (
        #             strat_name_id INT,
        #             %s,
        #             PRIMARY KEY(strat_name_id)
        #         );
        #     """,
        # )

        conn.commit()

        logging.info("Initialized vector database.")
