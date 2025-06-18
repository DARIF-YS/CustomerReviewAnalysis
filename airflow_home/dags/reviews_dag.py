from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipeline')))

from extract_reviews import extract
from enrich_data import enrich_reviews
from load_to_staging import load

# Définition des arguments par défaut
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG
dag = DAG(
    dag_id = 'reviews_dag',
    default_args=default_args,
    description="DAG de data warehouse pour effectuer l'extraction et le chargement des données.",
    schedule_interval=None,
    catchup=False,
    #schedule_interval=timedelta(days=1), 
)

# Tache de l'extraction
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract,
    dag=dag,
)

# Tache de stockage
load_task = PythonOperator(
    task_id='load_data',
    python_callable=load,
    dag=dag,
)

# Tache pour enrichir la data transformer
enrich_task = PythonOperator(
        task_id="enrich_reviews",
        python_callable=enrich_reviews,
        dag=dag,
    )

# Data Transformation (DBT & SQL)
data_trans_task = BashOperator(
    task_id='data_trans_task',
    bash_command='cd ~//CustomerReviewAnalysis/bank_reviews_dbt && dbt run --select reviews',
    dag=dag
)

# Data Modeling (PostgreSQL - Star Schema)
data_modeling_task = BashOperator(
    task_id='data_modeling_task',
    bash_command='cd ~//CustomerReviewAnalysis/bank_reviews_dbt && dbt run --select marts',
    dag=dag
)

extract_task >> load_task >> data_trans_task >> enrich_task >> data_modeling_task 