1 docker run
docker run -it python:3.9 (cái này thì không, chỉ chạy được lệnh python thôi)

    docker run -it entrypoint:bash python:3.9 (vào đây có thể cài thêm được thư viên khác của python)

postgres command line interface with docker:

    docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v d:/CODE/data-engineering-zoomcamp/week_1_basics_n_setup/_2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5431:5432 \
    postgres:13

    winpty pgcli -h localhost -p 5431 -u root -d ny_taxi

SQLAlchemy: thư viện trên python để thao tác với postgres

tính time insert dữ liệu:
%time df_tiny.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
Để thực hành được: - chạy container chưa image postgress - trên terminal kết nối postgres qua pgcli - chạy jupyter notebook để thao tác logic
chunksize in read_csv:
nếu dữ liệu lớn có thể đọc theo kiểu chunksize: https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5
1.2.3:Connecting pgAdmin and Postgres
docker run -it \
 -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
 -e PGADMIN_DEFAULT_PASSWORD="root" \
 -p 8080:80 \
 dpage/pgadmin4
Cần phải tạo ra một network để kết nối 2 container với nhau, vì nếu không có, nó chỉ giao tiếp trong nội bộ nó thôi

docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v d:/CODE/data-engineering-zoomcamp/week_1_basics_n_setup/\_2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5431:5432 \
--network pg-network \
--name pg-database \
postgres:13
docker run -it \
 -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
 -e PGADMIN_DEFAULT_PASSWORD="root" \
 -p 8080:80 \
 --network pg-network \
 --name pgadmin \
dpage/pgadmin4
Khi add name của server phải ghi đúng giá chị name của data đã gán ở trên

1.2.4 Dockerizing the Ingestion Script

convert ipynb to py script: jupyter nbconvert --to=sc
ript upload_data.ipynb

check pipeline truoc khi tao image
python ingest_data.py --user=root --password=root --host=localhost --port=5431 --db=ny_taxi --table_name=yellow_taxi_trips --url="http://192.168.1.4:8000/yellow_tripdata_2022-01.parquet"

buid image:
docker build -t taxi_ingest:v001 .

tao container tu image:
docker run -it --network pg-network taxi_ingest:v001 --user=root --password=root --host=pg-database --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips --url="http://192.168.1.4:8000/yellow_tripdata_2022-01.parquet"

(tao http cho viec download file)
python -m http.server

1.2.5: Running pgadmin4, postgres with dockercompose

    Viết file docker-compose.yaml
    	- docker compose up
    		docker compose up -d
    	docker compose down

1.2.6 SQL BASIC

1.3.1 Terraform
InfrastructureasCode: có thể thiết lập/quản lý những stack trước kia của hệ thống thông qua việc định nghĩa chúng trong 1 file script chẳng hạn thay vì tốn thời gian và công sức setup manual từng thứ (eg: ssh rồi cài cắm package, services, lib nọ kia)

- export GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Admin\Downloads\savvy-octagon-362900-893f0c27b16c.json"

  # Refresh token/session, and verify authentication

- gcloud auth application-default login

- terraform example with gcp: https://learn.hashicorp.com/tutorials/terraform/google-cloud-platform-build

https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

backend in terraform: https://viblo.asia/p/terraform-series-bai-6-terraform-backend-understand-backend-924lJRr6lPM

1.4.1 - ssh -i ~/.ssh/gcp manhdo@34.124.162.200
1.4.2
docker run -it
--network 2_docker_sql_default (lầy từ docker network ls)  
 --user=root
--password=root
--host=pg-database
--port=5432
--db=ny_taxi
--table_name=yellow_taxi_trips
--url="http://192.168.1.4:8000/yellow_tripdata_2022-01.parquet"
taxi_ingest:v001
homework:
ingest data to postgest

    import pandas as pd
    from sqlalchemy import create_engine

    url = "<https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv>"
    df_zones = pd.read_csv("taxi+_zone_lookup.csv")
    user = 'root'
    password = 'root'
    host = 'pgdatabase'
    port = 5432
    db = 'ny_taxi'
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db))
    df_zones.to_sql(name='zones', con=engine, if_exists='replace') # zones is a new table

host là tên của database trong docker compose
port là port của container postgres
db - database name
zones - table name

dockerfile sửa thành
FROM python:3.9

    RUN apt-get install wget
    RUN pip install pandas sqlalchemy psycopg2 pyarrow

    WORKDIR /app

    COPY ingest_data_zone.py ingest_data_zone.py
    COPY taxi+_zone_lookup.csv taxi+_zone_lookup.csv

    ENTRYPOINT ["python", "ingest_data_zone.py"]

build image - docker build -it zone_ingest:v001
run container vs image: - docker run -it zone_ingest:v001
question 1: count records
select count(\*) from yellow_taxi_trips;

question 2: largest tip for each day

    select DATE_TRUNC('day', tpep_pickup_datetime) as pickup_day, max(tip_amount) as max
    FROM yellow_taxi_trips
    group by pickup_day
    order by max desc;

Tutorial: https://cloud.google.com/docs/terraform/best-practices-for-terraform
more: https://github.com/orgs/terraform-google-modules/repositories
Một số vi dụ luyện tập với terraform từ trang chủ: https://github.com/terraform-google-modules/terraform-docs-samples

Best pratice : https://cloud.google.com/docs/terraform/best-practices-for-terraform
