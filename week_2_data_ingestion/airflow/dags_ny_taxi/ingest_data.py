from asyncio import Task
import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
FILE_NAME =  '{{ execution_date.strftime(\'%Y-%m\') }}'
YEAR = '{{ execution_date.strftime(\'%Y\') }}'
URL_TEMPLATE = URL_PREFIX + 'yellow_tripdata_'+ FILE_NAME +'.parquet'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_'+ FILE_NAME +'.parquet'
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')


# def format_to_parquet(src_file):
#     if not src_file.endswith('.csv'):
#         logging.error("Can only accept source files in CSV format, for the moment")
#         return
#     table = pv.read_csv(src_file)
#     pq.write_table(table, src_file.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)




# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="ny_taxi",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2020, 1, 1),
) as dag:
    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command='curl -sSL {} > {}'.format(URL_TEMPLATE, OUTPUT_FILE_TEMPLATE)
    )

    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": "raw/{{execution_date.strftime(\'%Y')}}/yellow_tripdata_"+ FILE_NAME +".parquet",
            "local_file": "{}".format(OUTPUT_FILE_TEMPLATE),
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "yellow_taxi_{{execution_date.strftime(\'%Y_%m\')}}",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{YEAR}/yellow_tripdata_{FILE_NAME}.parquet"],
            },
        },
    )

    rm_task = BashOperator(
        task_id="rm_task",
        bash_command="rm {}".format(OUTPUT_FILE_TEMPLATE)
    )
    download_dataset_task >> local_to_gcs_task >> bigquery_external_table_task >> rm_task
    # >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task

