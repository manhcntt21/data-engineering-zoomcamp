import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import argparse
import os
# user
# password
# host
# port
# database name
# table
# url of the csv
def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.parquet'
    os.system("wget {} -O {}".format(url, csv_name))
    # download csv file
    trips = pq.read_table(csv_name)
    df = trips.to_pandas()
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db))

    #  convert timestamp
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df_tiny = df.head(1000)
    df_tiny.to_sql(name=table_name, con=engine, if_exists='replace')
    print("finish")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='post for postgres')
    parser.add_argument('--db', help='databae name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the result to')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()
    main(args)

# python ingest_data.py --user=root --password=root --host=localhost --port=5431 --db=ny_taxi --table_name=yellow_taxi_trips --url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet"

