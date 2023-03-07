from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
default_args = {
  'owner': 'mb',
  'retries': 5,
  'retry_delay': timedelta(minutes=2)
}
with DAG(
  dag_id= 'our_first_dag_v5',
  default_args = default_args,
  description= 'This is our first dag that we write',
  start_date= datetime(2023, 3, 5, 2), # YYYY M DD
  schedule_interval = '@daily'
) as dag:
  task1 = BashOperator(
    task_id = 'first_task',
    bash_command = "echo hello world, this is the first task!"
  )
  task2 = BashOperator(
    task_id= 'second_task',
    bash_command= "echo I am the secnod task. I run after task 2"
  )
  task3 = BashOperator(
    task_id='third_task',
    bash_command = "echo I run after one at the same time as two!"

  )

task1 >> [task2, task3]