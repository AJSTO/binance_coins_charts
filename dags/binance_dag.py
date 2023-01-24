# Necessary libs:
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas_gbq
from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import uuid

default_args = {
    'owner': 'adam',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}
# Bigquery project, database, table
MY_PROJECT = 'crypto-375619'
MY_DATASET = 'coins'
MY_TABLE = 'coins-usdt'
# Connecting to project
KEY_PATH = f"dags/BQ_KEY.json"
CREDENTIALS = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
CLIENT = bigquery.Client(credentials=CREDENTIALS, project=CREDENTIALS.project_id, )
# Credentials to Binance API
API_KEY = 'qw2B0xM3SZi7b7S0VPZWX5WWy5yXlMsxjGnxnsLqqv3o0nJ0EUQUJHwe1Rz102I0'
API_SECRET = 'ZCfy64sGXwGvGNn0VHUUP431wjmDnZqrGw1HG1DZooxLe8FaDatLY0Mz3d2XBPPO'
CLIENT_BINANCE = Client(API_KEY, API_SECRET)
# All columns needed
PARAMS = [
    'symbol', 'priceChange', 'priceChangePercent', 'lastPrice', 'prevClosePrice',
    'volume', 'quoteVolume', 'injection_time'
]


def check_table():
    try:
        dataset_id = f"{CLIENT.project}.{MY_DATASET}"
        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "EU"
        CLIENT.create_dataset(dataset)  # Make an API request.
        # Creating table with schema:
        table_id = f"{MY_PROJECT}.{MY_DATASET}.{MY_TABLE}"
        #  Creating schema
        schema = [
            bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("priceChange", "FLOAT"),
            bigquery.SchemaField("priceChangePercent", "FLOAT"),
            bigquery.SchemaField("lastPrice", "FLOAT"),
            bigquery.SchemaField("prevClosePrice", "FLOAT"),
            bigquery.SchemaField("volume", "FLOAT"),
            bigquery.SchemaField("quoteVolume", "FLOAT"),
            bigquery.SchemaField("injection_time", "TIMESTAMP"),
        ]
        table = bigquery.Table(table_id, schema=schema)
        # Clustering on coin name to usdt
        table.clustering_fields = ["symbol", ]
        CLIENT.create_table(table)
    except Exception as e:
        print(e)


def get_ticker():
    # Getting ticker
    ticker = CLIENT_BINANCE.get_ticker()
    ticker_df = pd.DataFrame(ticker)
    # From all record selecting only pairs with USDT
    mask = ticker_df.symbol.str.contains(r'USDT$')
    ticker_usd = ticker_df[mask]
    # Adding time of injection
    ticker_usd['injection_time'] = datetime.now()
    # Reset index
    ticker_usd = ticker_usd.reset_index().drop(columns=['index'])
    # Filtering needed columns
    ticker_usd = ticker_usd[PARAMS]
    # Change columns from string to float
    ticker_usd.priceChange = ticker_usd.priceChange.astype(float)
    ticker_usd.priceChangePercent = ticker_usd.priceChangePercent.astype(float)
    ticker_usd.lastPrice = ticker_usd.lastPrice.astype(float)
    ticker_usd.prevClosePrice = ticker_usd.prevClosePrice.astype(float)
    ticker_usd.volume = ticker_usd.volume.astype(float)
    ticker_usd.quoteVolume = ticker_usd.quoteVolume.astype(float)
    # Upload to bigquery
    pandas_gbq.to_gbq(ticker_usd, f'{MY_DATASET}.{MY_TABLE}',
                      project_id=f'{MY_PROJECT}',
                      if_exists='append',
                      credentials=CREDENTIALS,
                      )


with DAG(
        default_args=default_args,
        dag_id='Capture_coins_info_',
        description='Capture_coins_info',
        start_date=datetime(2022, 1, 24, 13, 40),
        schedule_interval='*/2 * * * *',
        catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id='check_table',
        python_callable=check_table,
    )
    task2 = PythonOperator(
        task_id='get_ticker',
        python_callable=get_ticker,
    )
    task1 >> task2
