## 👨‍💻 Built with
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" /> 
<img src="https://airflow.apache.org/images/feature-image.png" width="100" height="27,5" />
<img src="https://www.devagroup.pl/blog/wp-content/uploads/2022/10/logo-Google-Looker-Studio.png" width="100" height="27,5" />
<img src="https://www.scitylana.com/wp-content/uploads/2019/01/Hello-BigQuery.png" width="100" height="27,5" />

##  Descripction about project

### ℹ️Project info

This project is created to capture information given from Binance API. I was interested in getting information about price of coin, quoteVolume and Volume in USDT of each coin.
I projected my airflow to launch projected DAG every 2 miniutes to get 'live' information about coin.
Selected pair of coins: coin noted on Binance to USDT.

### ℹ️About Binance API
[Binance API](https://www.binance.com/en/binance-api)

[How to get Binance API Key and Secret](https://www.binance.com/en/support/faq/how-to-download-and-set-up-binance-gift-card-api-af014f44f45845debf79b4cf81333a25)

[About library to operate with Binance API](https://python-binance.readthedocs.io/en/latest/)

To get interesting information about coin_USDT pair i used 'get_ticker()'
From recieved information formatted in DataFrame I pick columns:
```bash
'symbol', 'priceChange', 'priceChangePercent', 'lastPrice', 
'prevClosePrice', 'volume', 'quoteVolume', 'injection_time'
```
And also filtered pair of coins: all coins available on Binance to USDT.
Airflow schleduer to trigger DAG every 2 minutes.

### ℹ️Deploy airflow on Cloud Run
[Cloud Run](https://cloud.google.com/run?utm_source=google&utm_medium=cpc&utm_campaign=emea-pl-all-en-dr-bkws-all-all-trial-p-gcp-1011340&utm_content=text-ad-none-any-DEV_c-CRE_544052794495-ADGP_Hybrid%20%7C%20BKWS%20-%20PHR%20%7C%20Txt%20~%20Compute%20~%20Cloud%20Run-KWID_43700073022620957-aud-606988877974%3Akwd-1395289176175-userloc_1011531&utm_term=KW_gcp%20cloud%20run-NET_g-PLAC_&gclid=CjwKCAiAoL6eBhA3EiwAXDom5jP--KGqVFMR37Ls3SQBPuwJ1hO6eXYYWDw1Whuv1MeQtiUCgv_jTRoCO7kQAvD_BwE&gclsrc=aw.ds)

## 🔎 Looker Studio
Link to generated report in looker :

[Coin-USDT report](https://lookerstudio.google.com/reporting/314e6b79-f7d3-42fb-945c-a90ba1e9f872)

![IMG LOOKER](https://github.com/AJSTO/binance_coins_charts/blob/main/img/IMG%20LOOKER.png)

## 🗒️Database created in BIGQUERY contains tables:

#### Building permissions detailed info:
 
```bash
'symbol', 'priceChange', 'priceChangePercent', 'lastPrice', 
'prevClosePrice', 'volume', 'quoteVolume', 'injection_time'
```
Clustered by 'symbol'.

## ⏩ DAG contain tasks:
- check_table (checking if dataset and table exsists);
- get_ticker (get information from Binance API about all coins;

![IMG DAG](https://github.com/AJSTO/binance_coins_charts/blob/main/img/IMG%20DAG.png)

In this project I used PythonOperators.

## 📦This project using 6 Docker containers:
- **Container with airflow-init**
    - Created to initialize Apache Airflow;
- **Container with airflow-webserver**
    - Created GUI to use Apache Airflow;
- **Container with airflow-triggerer**
- **Container with airflow-scheduler**
    - Created to deal with DAGs;
- **Container with PosgreSQL**
    - Created for Airflow using;

## 🌲 Project tree
```bash
.
├── Dockerfile # Dockerfile to create image of airflow_extending 
├── README.md
├── dags
│   ├── binance_dag.py # Python script with DAG
│   └── BQ_KEY.json # JSON key should be here
├── docker-compose.yaml # Yaml file to create containers by Docker Compose
├── logs # Airflow logs
└──requirements.txt # Requirements to create airflow

```
## 🔑 Setup 

To run properly this project you should set variables in files: 
### ./dags/binance_dag.py:
- MY_PROJECT: # Project name in BIGQUERY
- MY_DATASET: # Dataset name in BIGQUERY
- MY_TABLE: # Table name in BIGQUERY
- API_KEY: # API Key from Binance API
- API_SECRET: # API Secret from Binance API

### ./docker-compose.yaml:
- POSTGRES_USER: 
- POSTGRES_PASSWORD:
- POSTGRES_DB:

## ⚙️ Run Locally
- Clone the project
- Go to the project directory:
Type in CLI:
```bash
  $ ls
```
You should see this:
```bash
Dockerfile logs README.md dags docker-compose.yaml requirements.txt
```
Now create image of needed airflow extension:
```bash
  $ docker build -t airflow_binance:latest .
```
When created, to initialize airflow type:
```bash
  $ docker-compose up airflow-init 
```
Next run build of all other images needed:
```bash
  $ docker-compose up -d
```
Now airflow will start working.
If you want to stop airflow:
```bash
  $ docker-compose down -v
```

## ⚙️ Open airflow
**When all containers running, get to bash into folder of git project and type:**
```bash
  localhost:8080
```
Next type password and username.
