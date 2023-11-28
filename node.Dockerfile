FROM python:3.11

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY embeddings ./embeddings
COPY llms ./llms

CMD sleep infinity