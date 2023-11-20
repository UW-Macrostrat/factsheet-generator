FROM jupyter/datascience-notebook

RUN pip install "psycopg[binary, pool]" pgvector --break-system-packages