from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mb',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'dag_with_catchup_backfill_v0',
    default_args= default_args,
    start_date = datetime(2023, 3, 4),
    schedule_interval='@daily',
    catchup = True
) as dag:
  task_1 = BashOperator(
    task_id = 'task1',
    bash_command= 'echo This is a simple bash command'
  )
task_1