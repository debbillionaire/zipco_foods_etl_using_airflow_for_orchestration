from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from extraction import run_extraction
from transformation import run_transformation
from loading import run_loading


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 14),
    'email': 'deboraholuwaseun.os@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(
    'zipco_foods_etl_pipeline',
    default_args=default_args,
    description= 'This represents zipco foods Data Management pipeline',
)

extraction_task = PythonOperator(
    task_id='extraction_layer',
    python_callable=run_extraction,
    dag=dag,
)

transformation_task = PythonOperator(
    task_id='transformation_layer',
    python_callable=run_transformation,
    dag=dag,
)

loading_task = PythonOperator(
    task_id='loading_layer',
    python_callable=run_loading,
    dag=dag,
)

extraction_task >> transformation_task >> loading_task