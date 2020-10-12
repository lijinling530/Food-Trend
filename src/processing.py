from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import functions as f
from pyspark.sql.types import *

region = 'us-west-2'
bucket = 'datahero'
key = 'parquet/RS_2018-10.parquet'
outfile = 'ingested/RS_2018-10-clean.parquet'
  
sc = SparkContext()
sc.setLogLevel('ERROR')
sc._jsc.hadoopConfiguration().set('fs.s3a.endpoint', f's3-{region}.amazonaws.com')
sc._jsc.hadoopConfiguration().set("parquet.enable.summary-metadata", "false")

spark = SparkSession(sc)

path = f's3a://{bucket}/{key}'
df = spark.read.parquet(path) 

df = df.select("author", "subreddit", "score", "num_comments", "num_crossposts", "title", "permalink")
df = df.filter(df["author"] != '[deleted]')
df = df.select(df["author"], df["subreddit"], (df["score"]+df["num_comments"]+df["num_crossposts"]).alias("score"), df["title"], df["permalink"])
df = df.withColumn('time', f.lit("2018-10"))
df.printSchema()

path = f's3a://{bucket}/{outfile}'
df.coalesce(1).write.save(path, format='parquet')


# write Data Frame to postgreSQL database

df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://private_ipv4:5432/my_db") \
    .option("dbtable", "submission") \
    .option("user", "user") \
    .option("password", "password") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()
 
spark.stop()

