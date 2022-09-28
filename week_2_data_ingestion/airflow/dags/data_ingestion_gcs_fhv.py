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

dataset_file = "bq-results-20220927-084015-1664268030716.csv"


# path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
parquet_file = dataset_file.replace('.csv', '.parquet')
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')

URL = "https://drive.google.com/uc?id=1JBQhTet0LEe3yg2guY-vWF88yhqVI8Kt&export=download"
FILE_NAME = 'bq-results-20220927-084015-1664268030716.csv'
TABLE_NAME = 'yellow_taxi_trip4'
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def download_parqeutized_upload_dag(
    dag,
    url_template,
    local_csv_path_template,
    local_parquest_path_template,
    gcs_path_template
):
    with dag:
        download_dataset_task = BashOperator(
            task_id="download_dataset_task",
            bash_command='curl -L "{}" > {}/{}'.format(url_template, AIRFLOW_HOME, local_csv_path_template)
        )

        download_dataset_task 
               



# NOTE: DAG declaration - using a Context Manager (an implicit way)
yellow_taxi_data = DAG(
    dag_id="yellow_taxi_data_v2",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2019, 1, 1),
    catchup=True,
    max_active_runs=1,
    tags=['dtc-de'],
)


download_parqeutized_upload_dag(yellow_taxi_data, URL, FILE_NAME, 'local_parquest_path_template', 'gcs_path_template')



zones_taxi_data = DAG(
    dag_id="zones_taxi_data_v1",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2019, 1, 1),
    catchup=True,
    max_active_runs=1,
    tags=['dtc-de'],
)


download_parqeutized_upload_dag(zones_taxi_data, URL, FILE_NAME, 'local_parquest_path_template', 'gcs_path_template')







# download_dataset_task = BashOperator(
#     task_id="download_dataset_task",
#     bash_command='curl -L "{}" > {}/{}'.format(URL, AIRFLOW_HOME, FILE_NAME)
# )


# format_to_parquet_task = PythonOperator(
#     task_id="format_to_parquet_task",
#     python_callable=format_to_parquet,
#     op_kwargs={
#         "src_file": f"{path_to_local_home}/{dataset_file}",
#     },
# )

# # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
# local_to_gcs_task = PythonOperator(
#     task_id="local_to_gcs_task",
#     python_callable=upload_to_gcs,
#     op_kwargs={
#         "bucket": BUCKET,
#         "object_name": f"raw/{parquet_file}",
#         "local_file": f"{path_to_local_home}/{parquet_file}",
#     },
# )

# bigquery_external_table_task = BigQueryCreateExternalTableOperator(
#     task_id="bigquery_external_table_task",
#     table_resource={
#         "tableReference": {
#             "projectId": PROJECT_ID,
#             "datasetId": BIGQUERY_DATASET,
#             "tableId": "external_table",
#         },
#         "externalDataConfiguration": {
#             "sourceFormat": "PARQUET",
#             "sourceUris": [f"gs://{BUCKET}/raw/{parquet_file}"],
#         },
#     },
# )

# download_dataset_task 
# >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task