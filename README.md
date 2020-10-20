# KOL-Trend

## Motivation
Do you feel lost in a sea of information when you are exploring social media, let's say, Reddit?
Key Opinion Leaders (KOL) are those who you may want to follow and check in. Those influencers will help you find out what the hottest topics are.
Not an Option for Reddit users!
Using batching Reddit's data, design an algorithm which can output the KOL’s influences. The algorithm is to find out who are the KOLs, and then their rankings will be listed by searching results.


## Engineering Challenge
1. High latency - Solution: Choose DataFrame over RDD, tune spark-submit flags
2. Data shuffling - Solution: Specify Schema, Repartition, reduce join(), groupBy()
3. Storage Cost - Solution: Convert JSON to Parquet
4. Processing Time - Solution: Optimize SQL query, garbage collection

- Spark Performance Tuning is the goal!

## Dataset
Download from: https://files.pushshift.io/reddit/
- JSON files, 500 GB in total

## Quickstart Guide
### 1. Set Up AWS Cluster
The project is set up on AWS service. Total 9 (m4.large) EC2 instances are applied.

### 2. Set Up S3 Storage
Create a datalake in AWS S3.

### 3. Set Up Spark
Install Spark 2.4.7, install pyspark.

### 4. Set Up Database
Install PostgreSQL relational database, create user/database, configurate JDBC.

### 5. Set Up Airflow
Install Airflow, configurate Airflow PATH, define DAG, and run airflow.py.

### 6. Set Up Frontend
Install Dash/Flask, run app.py

### 7. Start Pipeline
Start Airflow webserver and scheduler.
1. download the compressed dataset from website, 
2. uncompress the dataset, 
3. upload the dataset to S3, 
4. submit first spark job, spark will read JSON files from S3 into dataframe, convert into Parquet, upload back to S3, 
5. submit second spark job, spark will read Parquet files from S3 into dataframe, transform and upload back to S3, meanwhile, write dataframe to PostgreSQL. 
Airflow job finished.

Run dash, or set it up in a domain webserver. Surf through the website, and get the information you want.

## Project Pipeline
The tech pipeline is:
![Image of Pipeline](https://github.com/lijinling530/KOL-Trend/blob/master/image/tech%20stack.png)

## All About Data
The end table is:
![Image of Demo](https://github.com/lijinling530/KOL-Trend/blob/master/image/demo.png)
