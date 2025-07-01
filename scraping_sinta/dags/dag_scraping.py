from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from include.scraping_affiliations import scrape_institutions

# Default arguments
default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'sinta_scraping_dag',
    default_args=default_args,
    description='Scrape SINTA affiliation data auto batch',
    schedule='0 * * * *',  # Setiap jam
    start_date=datetime(2024, 7, 1),
    catchup=False,
    tags=["portofolio"]
) as dag:

    # Task1: Scraping 
    scraping_task = PythonOperator(
        task_id='scrape_sinta_data',
        python_callable=scrape_institutions,
        op_kwargs={'pages_per_run': 10}  # Satu kali jalan scrape 10 halaman
    )



    scraping_task