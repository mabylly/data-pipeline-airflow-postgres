from airflow import DAG
from airflow.operators.python_operator import PythonOperator    
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import timedelta,datetime
import pandas as pd
import os


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def extract_csv_file(ds):

    # Read CSV file
    df = pd.read_csv('/opt/airflow/data/transacoes.csv', header=0, delimiter=',')

    # Create directory if it doesn't exist
    dest_csv_dir = f"/opt/airflow/datalake/{ds}/csv/"
    if not os.path.exists(dest_csv_dir):
        os.makedirs(dest_csv_dir)

    # Save to datalake
    dest_file = f"{dest_csv_dir}/transacoes.csv"
    if not os.path.exists(dest_file):
        df.to_csv(dest_file, index=False)
    else:
        df_csv_exists = pd.read_csv(dest_file, header=0, delimiter=',')
        if not df.equals(df_csv_exists):
            df.to_csv(dest_file, index=False)

def extract_database_file(ds):

    # Create directory if it doesn't exist
    dest_database_dir = f"/opt/airflow/datalake/{ds}/postgreSQL/"
    if not os.path.exists(dest_database_dir):
        os.makedirs(dest_database_dir)
    
    #connection with postgree
    try:
        hook = PostgresHook(postgres_conn_id='postgres_source')
        engine = hook.get_sqlalchemy_engine()

        tables = ['agencias','clientes','colaborador_agencia','colaboradores','contas','propostas_credito']

        for table in tables:
            df = pd.read_sql_query(f"SELECT * FROM {table};",con =engine)

            dest_path = f"{dest_database_dir}/{table}.csv"
            if not os.path.exists(dest_path):
                df.to_csv(dest_path, index =False)
            else:
                df_db_exists = pd.read_csv(dest_path, header=0, delimiter=',')
                if not df.equals(df_db_exists):
                    df.to_csv(dest_path, index =False)
    
    except Exception as e:
        raise e

def load_data(ds):
    try:
        hook = PostgresHook(postgres_conn_id='postgres_dw')
        engine = hook.get_sqlalchemy_engine()

        #load csv
        csv_file = f"/opt/airflow/datalake/{ds}/csv/transacoes.csv"
        df_csv = pd.read_csv(csv_file, header = 0, delimiter=",")
        df_csv.to_sql("transacoes", con =engine, if_exists="replace",index = False)

        #load database
        postgres_dir = f"/opt/airflow/datalake/{ds}/postgreSQL/"
        tables = ['agencias','clientes','colaborador_agencia','colaboradores','contas','propostas_credito']

        for table in tables:
            file_path = f"{postgres_dir}/{table}.csv"
            if os.path.exists(file_path):
                df_table = pd.read_csv(file_path, header = 0, delimiter=",")
                df_table.to_sql(table,con =engine, if_exists="replace",index = False)
    
    except Exception as e:
        raise e

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="35 4 * * *", # At 04:35 AM every day
    default_args=default_args,
    catchup=False,
    template_searchpath = "/opt/airflow/data"
) as dag:
    
    extract_csv_task = PythonOperator(
        task_id='extract_csv_file',
        python_callable=extract_csv_file,
        op_kwargs={'ds': '{{ ds }}'}
    )

    extract_postgree_task = PythonOperator(
        task_id='extract_database_file',
        python_callable=extract_database_file,
        op_kwargs={'ds': '{{ ds }}'}
    )

    create_table_task = PostgresOperator(
        task_id = "create_tables",
        postgres_conn_id = "postgres_dw",
        sql = "datawarehouse.sql"
    ) 

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={'ds': '{{ ds }}'}
    )

#task sequences
[extract_csv_task , extract_postgree_task] >> create_table_task >> load_data_task