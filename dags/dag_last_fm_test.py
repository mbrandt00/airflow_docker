from airflow import DAG, task
from datetime import datetime, timedelta
from airflow.operators.python import get_current_context
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3Hook
from airflow.macros import ds_add
default_args = {
    'owner': 'mb',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def get_pylast(ti, ds):
  import pylast
  import calendar
  print(f"pylast version: {pylast.__version__}")
  lastfm_network = pylast.LastFMNetwork(
    api_key='817b23876279930e6d658814ffc5d9e8',
    api_secret='0fa0f1214ad46af35f844c9e80879032',
  )
  user = lastfm_network.get_user('mballa000')
  start = datetime.strptime(ds, "%Y-%m-%d")
  end = datetime.strptime(ds_add(ds, 1), "%Y-%m-%d")
  utc_start = calendar.timegm(start.utctimetuple())
  utc_end = calendar.timegm(end.utctimetuple())
  daily_tracks = user.get_recent_tracks(time_from= utc_start, time_to= utc_end, limit= 999)
def upload_to_s3(filename: str, key: str, bucket_name: str) -> None:
    hook = S3Hook('last-fm')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)

with DAG(
    dag_id = 'dag_last_fm_test_v11',
    default_args= default_args,
    start_date = datetime(2023, 2, 25),
    schedule = '@daily'
) as dag:

  task_upload_to_s3 = PythonOperator(
          task_id='upload_to_s3',
          python_callable=upload_to_s3,
          op_kwargs={
              # 'filename': 'email.csv',
              'key': 'email.csv',
              'bucket_name': 'last-fm'
          }
  )
  # get_pylast = PythonOperator(
  #   task_id = 'get_pylast',
  #   python_callable= get_pylast
  # )

upload_to_s3