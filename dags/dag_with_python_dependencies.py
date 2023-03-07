from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'mb',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def get_sklearn():
  import sklearn
  print(f"scikit-learn with version: {sklearn.__version__}")
with DAG(
    dag_id = 'dag_with_python_dependencies',
    default_args= default_args,
    start_date = datetime(2023, 3, 5),
    schedule_interval='@daily',
) as dag:
  get_sklearn = PythonOperator(
    task_id = 'get_sklearn',
    python_callable= get_sklearn
  )
  get_sklearn