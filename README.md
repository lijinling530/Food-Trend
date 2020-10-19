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
The project is set up on AWS service. 9 m4.large EC2 instance is applied.

### 2. Set Up S3 Storage
AWS S3 is served as datalake.

### 3. Set Up Spark
Spark 2.4.7 is installed.

### 4. Set Up Database
PostgreSQL relational database.

### 5. Set Up Airflow
Airflow is installed.

### 6. Set Up Frontend
Dash/Flask is served as frontend.

## Project Pipeline
The tech pipeline is:
![Image of Pipeline](https://github.com/lijinling530/KOL-Trend/blob/master/image/tech%20stack.png)

## All About Data
The end table is:
![Image of Pipeline](https://github.com/lijinling530/KOL-Trend/blob/master/image/End%20Data.png)
