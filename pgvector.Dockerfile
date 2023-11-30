FROM ankane/pgvector
COPY pgvector.sql /docker-entrypoint-initdb.d

ENV POSTGRES_DB=vector_db
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin