## 1. How to write DAG

1. Instatiate a DAG object
2. The name of the DAG
3. The date at which the DAG should first start running
4. At what interval the DAG should run

---

5. Apply Bash to to download the URL response with curl
6. The name of the task

---

7. A Python function will parse the response and download all rocket pictures

---

8. Call the Python function in the DAG with a PythonOperator.

---

9. Set the order of execution of tasks.

## 2.1 Running Airflow in Python Environment

```
1. Setup the environment  (conda/virtualenv/pyenv)
2. pip install apache-airflow
3. airflow db init
4. airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email musa.hanif@gmail.com
5. cp download_rocket_launches.py~/airflow/dags/
6. airflow webserver
7. aiflow scheduler

```

## 2.2 Running Airflow in Docker containers

- NOTES:
  If you familiar with Docker, it's not desirable to run multiple in single Docker container. In production setting, Airflow webserver, scheduler and metastore should be **run in separate Docker containers.**

```
docker run  -it \
-p 8080:8080 \                                                                                  # Expose on host port 8080 to the container port 8080
-v /path/to/dag/download_rocket_launches.py:/opt/airflow/dags/download_rocket_launches.py \     # Mpunt DAG file in the container
--entrypoint=/bin/bash \
--name airflow \
apache/airflow:2.0.0-python3.8 \                                                                # Airflow Docker image
-c '(\
airflow db init && \                                                                            # Initialize the database/ metastore in the container
airflow users create --username admin --password admin --password admin \                       # Create the admin user
--firstname Anonymous --lastname Admin --role Admin --email musa.hanif@gmail.con); \
airflow webserver & \                                                                           # Start the webserver in the background
airflow scheduler'                                                                              # Start the scheduler
```
