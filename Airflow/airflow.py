# airflow related
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# other packages
from datetime import datetime
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'email': ['xxxxxxx@mail.com'],    
    'end_date': datetime(2018, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

date_str = str(datetime.year) + '-' + str(datetime.month)
filename1='RS_' + date_str + '.xz'
filename2='RS_' + date_str

dag = DAG(
  dag_id='reddit_DAG', 
  description='Insight project reddit',
  schedule_interval=timedelta(days=1),
  default_args=default_args)

preprocess_1 = BashOperator(
  task_id='download',
  bash_command='wget https://files.pushshift.io/reddit/submissions/{filename}'.format(filename=filename1),
  dag = dag)

preprocess_2 = BashOperator(
  task_id='uncompress',
  bash_command='unxz {filename}'.format(filename=filename1),
  dag = dag)

preprocess_3 = BashOperator(
  task_id='upload_to_S3',
  bash_command='s3cmd put {filename} s3://datahero'.format(filename=filename2),
  dag = dag)

spark_1 = BashOperator(
  task_id='convert_to_parquet',
  bash_command='spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 \
  --conf spark.executor.extraJavaOptions=-Dcom.amazonaws.services.s3.enableV4=true \
  --conf spark.driver.extraJavaOptions=-Dcom.amazonaws.services.s3.enableV4=true \
  --conf spark.sql.parquet.mergeSchema=false --executor-memory 6G --driver-memory 6G \
  --master spark://10.0.0.14:7077 Convert_to_Parquet.py',
  dag = dag)

spark_2 = BashOperator(
  task_id='processing',
  bash_command='spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7,org.postgresql:postgresql:42.2.16 \
  --conf spark.executor.extraJavaOptions=-Dcom.amazonaws.services.s3.enableV4=true \
  --conf spark.driver.extraJavaOptions=-Dcom.amazonaws.services.s3.enableV4=true \
  --conf spark.sql.parquet.mergeSchema=false  \
  --driver-class-path /home/ubuntu/postgresql-42.2.16.jar \
  --executor-memory 6G --driver-memory 6G \
  --master spark://10.0.0.14:7077 processing.py',
  dag = dag)

# setting dependencies
preprocess_1 >> preprocess_2
preprocess_2 >> preprocess_3
preprocess_3 >> spark_1
spark_1 >> spark_2
