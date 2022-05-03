FROM python:3.9

# bash pip install requests
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2


# cd /app
WORKDIR /app

# cp source dest
COPY ingest_data.py ingest_data.py

# Entrypoint before running the "FROM" clause
ENTRYPOINT [ "python", "ingest_data.py" ]
