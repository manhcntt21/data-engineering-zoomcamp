FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 gdown

WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]

# COPY ingest_data_zone.py ingest_data_zone.py
# COPY taxi+_zone_lookup.csv taxi+_zone_lookup.csv

# ENTRYPOINT ["python", "ingest_data_zone.py"]