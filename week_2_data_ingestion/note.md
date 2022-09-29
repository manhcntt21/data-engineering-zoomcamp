# Data Lake

- What is a Data Lake?
- Data Lake vs Data Warehouse
- Gotcha of Data Lake
- ETL vs ELT
- Cloud provider Data Lake

## What is a Data Lake?

- is a central repository that holds big data from many sources
- type of data:
  - structured data
  - semi-structured data
  - unstructured data
- used extensively for machine learning

## Data Lake vs Data Ware House

| Lake                                        | WareHouse       |
| :------------------------------------------ | :-------------- |
| general a data lake is an unstructured data | structured data |
|                                             |                 |

## ETL vs ELT

| ETL                                    | ELT                                         |
| :------------------------------------- | :------------------------------------------ |
| export tranform and load               | export load and transform                   |
| mainly used for a small amount of data | used for large amounts of data              |
| ...                                    | provides data lake support (schema on read) |
| data warehouse solution                | data lake solution                          |

## Gotcha of Data Lake

- converting into data swamp
- no versioning
  incompatiable schemas for same data without versioning
- no metadata associated
- joins not possible

## Cloud provider for data lake

- GCP - cloud storage
- AWS - S3
- AZURE - AZURE BLOB

# Introduction to workflow orchestration

chèn ảnh sau

## Setup Airflow environment with docker-compose

- echo -e "AIRFLOW_UID=$(id -u)" > .env
- docker compose build
- docker compose up airflow-init
- docker compose up

crontab guru để test schedule

chỉ biết dùng curl trên docker, wget, gdown chưa làm được
URL = 'https://drive.google.com/u/0/uc?id=1LAFAvyRUyf7VUXUs4H_zmu0H0Gc5ZpcT&export=download'
FILE_NAME = 'bq-results-20220927-084015-1664268030716.csv'
bash_command='curl -L "{}" > {}/{}'.format(URL, AIRFLOW_HOME, FILE_NAME)

Parameterizing URL, Jinja templating for bash command, datetime formatting for execution time

ingest_script, modifying requirements.txt and Dockerfile, integrating ingestion to DAG, Environment Variable, modifying docker compose and connecting to DAG,

kết nối 2 docker compose với nhau:
https://stackoverflow.com/questions/38088279/communication-between-multiple-docker-compose-projects

Checking DB with pgCLI, directory of db, checking the container connection

- bật lại postgres ở bài trước, thêm network cho nó rồi docker compose up.

- kiểm tra bật lại duoc chua, docker ps xem port của nó là gì rồi chạy, pgcli -h localhost -p 5431 -u root -d ny_taxi (kết với vào kiểm tra table xem có đúng là nó không)
- kết nối vào posgres trên thông qua worker của airflow

  - docker exec -it <worker container> bash
  - vào python, tao thử kết nối dùng sqlalche

    - from sqlalchemy import create_engine
    - engine = create_engine('postgresql://root:root@localhost:5431/ny_taxi')
    - engine.connect()
    - <sqlalchemy.engine.base.Connection object at 0x00000255B023D000> là thành công

    chú ý phải xác định rõ tên của host, không hiểu sao, nó lại nhận là localhost mà không phải là tên service trong docker compose của week1 (pgdatabase)

- muốn ingest data từ local lên GCS-bucket, phải thêm role cho account (storage admin)

- muốn thêm data từ bucket tới big query phải tạo dataset trước (có thể thêm quyền)
  - khi tạo dataset trên big query nhớ chú ý trên region, khác region không query được

Phải tạo region của bucket và bigquery data set giống nhau

khi chạy query nếu location khác nhau, có thể vào query setting thay đổi

## tranfer data from aws to gpc with transfer service

DE Zoomcamp 2.4.1 - Moving Files from AWS to GPC with Transfer Service
chưa có aws nên chưa làm

## config transfer service with terraform

##

backfill

docker exec -it <airflow websever> bash
airflow dags backfill <ten dag> --reset-dagruns -s 2020-01-01 -e 2021-01-01

sau khi thêm vào dữ liệu vào bucket có thể tạo table trên bigquery như sau
cretea or replace external table 'ny_taxi'
Option (
format= 'parquest'
uris = [
'gs://dtc_data_lake/yellowtrip/2019/*',
'gs://dtc_data_lake/yellowtrip/2020/*'
]
)
link cua bucket
