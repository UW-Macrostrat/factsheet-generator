import logging
import psycopg
import numpy as np
from numpy.typing import NDArray


async def retrieve_chunks(
    conn: psycopg.AsyncConnection,
    strat_name: str,
    query_vector: NDArray[np.float32],
    must_include: bool = True,
    top_k: int = 10,
) -> list[tuple]:
    data = []

    if must_include:
        data = await conn.execute(
            """
                SELECT chunk_data.chunk_text, chunk_data.embedding <=> %(query_vector)s as distance
                FROM strat_name_lookup
                INNER JOIN chunk_lookup ON strat_name_lookup.strat_name_id = chunk_lookup.strat_name_id
                INNER JOIN chunk_data ON chunk_lookup.chunk_id = chunk_data.chunk_id
                WHERE strat_name LIKE %s
                ORDER BY distance
                LIMIT %(top_k)s;
            """,
            {
                "query_vector": query_vector,
                "top_k": top_k,
                "like_pattern": f"%{strat_name}%",
            },
        ).fetchall()

    else:
        data = await conn.execute(
            """
                SELECT chunk_text, embedding <=> %(query_vector)s as distance
                FROM chunk_data
                ORDER BY distance
                LIMIT %(top_k)s;
            """,
            {"query_vector": query_vector, "top_k": top_k},
        ).fetchall()

    await conn.commit()

    return data


async def store_facts(
    conn: psycopg.AsyncConnection, strat_name: str, facts: dict
) -> None:
    strat_name_id = await conn.execute(
        """
            SELECT strat_name_id
            FROM strat_name_lookup
            WHERE strat_name = %s;
        """,
        (strat_name,),
    ).fetchone()[0]

    await conn.commit()

    query = """
                INSERT INTO factsheets (strat_name_id, {columns})
                VALUES ({strat_name_id}, {values});
            """
    columns = ",".join(facts.keys())
    values = ",".join(facts.values())

    await conn.execute(
        query.format(columns=columns, values=values, strat_name_id=strat_name_id)
    )

    await conn.commit()
