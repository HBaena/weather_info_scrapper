from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from os import getcwd, path


def run_scrapping():
    print("SCRAPPER IS RUNNING")
    import subprocess
    subprocess.run(['poetry', 'run', 'python', path.join(getcwd(), "weather_info_scrapping.py"), "all"])


def run_db_resume_generator():
    print("DB RESUME IS RUNNING")
    import subprocess
    subprocess.run(['poetry', 'run', 'python', path.join(getcwd(), "generate_db_resume.py")])


default_args = {
    'owner': 'hbaena',
    'start_date': days_ago(1),
    'retries': 0,
}

dag = DAG(
    dag_id='weather_info',
    default_args=default_args,
    description='Scrapp weather info using app.py every hour',
    schedule="@hourly",
    catchup=False,
)

scrapping = PythonOperator(
    task_id='scrapping_weather_info',
    python_callable=run_scrapping,
    dag=dag
)

db_resume_generator = PythonOperator(
    task_id='generate_db_resume_parquet_file',
    python_callable=run_db_resume_generator,
    dag=dag
)


scrapping >> db_resume_generator
