from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime
import os


def retrain_pipeline():
    os.system(
        "python airflow/scripts/retrain_churn_model.py"
    )


with DAG(
    dag_id="retailpulse_retraining",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    retrain_task = PythonOperator(
        task_id="retrain_churn_model",
        python_callable=retrain_pipeline,
    )