import logging
import psycopg
import numpy as np
from numpy.typing import NDArray


async def insert_chunk(
    conn: psycopg.AsyncConnection,
    text: str,
    vector: NDArray[np.float32],
) -> None:
    await conn.execute(
        """
            INSERT INTO chunk_data(chunk_text, embedding)
            VALUES(%s, %s);
        """,
        (
            text,
            vector,
        ),
    )

    await conn.commit()


async def retrieve_chunks(
    conn: psycopg.AsyncConnection,
    query_embedding: NDArray[np.float32],
    strat_name: str = "",
    must_include: bool = True,
    top_k: int = 10,
) -> list[tuple]:
    data = []

    if must_include:
        # """
        #     SELECT chunk_data.chunk_text, chunk_data.embedding <=> %(query_vector)s as distance
        #     FROM strat_name_lookup
        #     INNER JOIN chunk_lookup ON strat_name_lookup.strat_name_id = chunk_lookup.strat_name_id
        #     INNER JOIN chunk_data ON chunk_lookup.chunk_id = chunk_data.chunk_id
        #     WHERE strat_name LIKE %(like_pattern)s
        #     ORDER BY distance
        #     LIMIT %(top_k)s;
        # """,

        data = await conn.execute(
            """
                SELECT chunk_text, embedding <=> %(query_embedding)s as distance
                FROM chunk_data
                WHERE strat_name LIKE %(like_pattern)s
                ORDER BY distance
                LIMIT %(top_k)s;
            """,
            {
                "query_embedding": query_embedding,
                "top_k": top_k,
                "like_pattern": f"%{strat_name}%",
            },
        ).fetchall()

    else:
        data = await conn.execute(
            """
                SELECT chunk_text, embedding <=> %(query_embedding)s as distance
                FROM chunk_data
                ORDER BY distance
                LIMIT %(top_k)s;
            """,
            {"query_embedding": query_embedding, "top_k": top_k},
        ).fetchall()

    await conn.commit()

    return data


async def store_facts(
    conn: psycopg.AsyncConnection,
    strat_name: str,
    categories: list[str],
    facts: list[str],
) -> None:
    # strat_name_id = await conn.execute(
    #     """
    #         SELECT strat_name_id
    #         FROM strat_name_lookup
    #         WHERE strat_name = %s;
    #     """,
    #     (strat_name,),
    # ).fetchone()[0]

    await conn.commit()

    query = """
                INSERT INTO factsheets (strat_name, {columns})
                VALUES ({parameters});
            """
    columns = ",".join(categories)
    parameters = ",".join(["%s" * (len(facts) + 1)])
    values = [strat_name] + facts
    await conn.execute(query.format(columns=columns, parameters=parameters), values)

    await conn.commit()
