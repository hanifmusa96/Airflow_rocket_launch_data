import json
import pathlib

import library
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(                                                                                      # The DAG class takes two required arguments
    dag_id="download_rocket_launches",                                                          # The name of the DAG displayed in Airflow user interface (UI)
    start_date=airflow.utils.dates.days_ago(14),                                                # The start date of the DAG at which the workflow should first start running
    schedule_interval=None
)

download_launches = BashOperator(                                                               # BashOperator is a subclass of BaseOperator
    task_id='download_launches',                                                                # The name of the task
    bash_command='curl -o /temp/lanuches.json \
        -L "https://ll.thespacedevs.com/2.0.0/launch/upcoming"',                                # The bash command to be executed
    dag=dag                                                                                     # The DAG to which the task belongs
    )


def _get_pictures():                                                                            # The function is called by the PythonOperator

    # Ensure directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exists_ok=True)                             # The pathlib.Path class is used to create directories if it doesn't exist

    # Download all pictures in launches.json
    with open('/tmp/launches.json') as f:                                                       # Open the rocket launches json file 
        launches = json.load(f)                                                                 # Load the json file into dictionary
        image_urls = [launch['image'] for launch in launches['results']]                        # For every launch, fetch the element 'image' from the dictionary
        for image_url in image_urls:                                                            # Loop over all image urls
            try:
                response = requests.get(image_url)                                              # Try to fetch the image
                image_filename = image_url.split('/')[-1]                                       # Extract the filename from the url at last index    
                target_file = f'/temp/images/{image_filename}'                                  # Create the target file path
                with open(target_file, 'wb') as f:                                              # Open the target file in binary mode
                    f.write(response.content)                                                   # Write the image (from response) to the target file path
                print(f"Downloaded {image_url} to {target_file}")
            except requests.exceptions.MissingSchema:                                           # If the url is invalid, skip it : error catch
                print(f"{image_url} appears to be an invalid URL.")
            except requests.exceptions.ConnectionError:                                         # If the url is invalid, skip it : error catch
                print(f" Could not connect to {image_url}")


get_pictures = PythonOperator(
    task_id='get_pictures',
    python_callable=_get_pictures,                                                              # Call the function _get_pictures
    dag=dag
    )

notify = BashOperator(
    task_id='notify',
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag
)

download_launches >> get_pictures >> notify                                                     # Arrow set the order execution of tasks
#download_launches.set_downstream(get_pictures)                                                 ## This is the same as the line above
#get_pictures.set_downstream(notify)                                                            ## This is the same as the line above
