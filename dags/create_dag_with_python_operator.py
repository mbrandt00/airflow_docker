from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
default_args = {
    'owner': 'MB',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(ti):
    age = ti.xcom_pull(task_ids = 'get_age', key = 'age')
    first_name = ti.xcom_pull(task_ids = 'get_name', key = 'first_name')
    last_name = ti.xcom_pull(task_ids = 'get_name', key = 'last_name')
    print(f"hello world! My name is {first_name} {last_name},", f" I am {age} years old")

def get_name(ti):
  ti.xcom_push(key='first_name', value='jerry')
  ti.xcom_push(key='last_name', value='brandt')

def get_age(ti):
  ti.xcom_push(key='age', value=19)
with DAG(
    default_args= default_args,
    dag_id= 'our_dag_with_python_operator_v09',
    start_date = datetime(2023, 3, 4),
    schedule_interval = '@daily'

) as dag:
  task1 = PythonOperator(
    task_id = 'greet',
    python_callable= greet,
  )
  task2 = PythonOperator(
    task_id = 'get_name',
    python_callable= get_name,
    # op_kwargs= {'name': 'Tom', 'age': 20}
  )
  task3 = PythonOperator(
    task_id='get_age',
    python_callable=get_age

  )

  [task2, task3] >> task1