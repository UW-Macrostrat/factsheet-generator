FROM jupyter/datascience-notebook

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
RUN pip install "psycopg[binary]"