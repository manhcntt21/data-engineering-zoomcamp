#!/usr/bin/env python
# coding: utf-8
from ast import main
from genericpath import isfile
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = "bq-results-20220927-084015-1664268030716.csv"
    if not os.path.isfile(file_name):
        os.system('gdown --id {}'.format(url))

    df = pd.read_csv(file_name)

    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db))

    engine.connect()

    #  convert timestamp
    df.pickup_datetime = pd.to_datetime(df.pickup_datetime)
    df.dropoff_datetime = pd.to_datetime(df.dropoff_datetime)

    df_iter = pd.read_csv(file_name, iterator=True, chunksize=10000)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    while True:
        try:
            t_start = time()
            dff = next(df_iter)
            dff.pickup_datetime = pd.to_datetime(df.pickup_datetime)
            dff.dropoff_datetime = pd.to_datetime(df.dropoff_datetime)
            dff.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()
            print('inserted another chunk, took %.3f second' % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')    

    args = parser.parse_args()
    main(args)