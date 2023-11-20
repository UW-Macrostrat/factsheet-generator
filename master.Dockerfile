FROM ubuntu:23.10
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pandas==2.1.0 --break-system-packages
RUN pip3 install grpcio==1.58.0 grpcio-tools==1.58.0 --break-system-packages
RUN pip3 install aiofiles --break-system-packages
RUN pip3 install "psycopg[binary, pool]" pgvector --break-system-packages

COPY *.py .

# CMD ["python3", "master.py", "80"]