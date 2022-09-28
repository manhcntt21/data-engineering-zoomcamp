import os

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


local_workflow = DAG(
    "example",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1)
)



with local_workflow:
    wget_task = BashOperator(
        task_id='echo',
        bash_command='echo 1',
    )

    ingest_task = BashOperator(
        task_id='pwd',
        bash_command='pwd',
    )

    wget_task >> ingest_task