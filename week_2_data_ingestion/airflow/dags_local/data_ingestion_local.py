import os

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script import ingest_callable


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# lay gia tri tu file .env
PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')


local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1)
)


# URL = "https://drive.google.com/u/0/uc?id=1LAFAvyRUyf7VUXUs4H_zmu0H0Gc5ZpcT&export=download"
URL = "https://drive.google.com/uc?id=1JBQhTet0LEe3yg2guY-vWF88yhqVI8Kt&export=download"
FILE_NAME = 'bq-results-20220927-084015-1664268030716.csv'
TABLE_NAME = 'yellow_taxi_trip4'
# URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
# OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
# TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'

with local_workflow:
    curl_task = BashOperator(
        task_id='curl',
        bash_command='curl -L "{}" > {}/{}'.format(URL, AIRFLOW_HOME, FILE_NAME)
    )

    check = BashOperator(
        task_id="check",
        bash_command='ls {}'.format(AIRFLOW_HOME)
    )

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
           user=PG_USER,
           password=PG_PASSWORD,
           host=PG_HOST,
           port=PG_PORT,
           db=PG_DATABASE,
           table_name=TABLE_NAME,
           csv_file=AIRFLOW_HOME +'/' + FILE_NAME
        ),
    )    

    curl_task >> check >> ingest_task