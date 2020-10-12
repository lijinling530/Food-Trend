from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *

region = 'us-west-2'
bucket = 'datahero'
key = 'processed/RS_2019-11.json'
outfile = 'parquet/RS_2019-11.parquet'

sc = SparkContext()
sc.setLogLevel('ERROR')
sc._jsc.hadoopConfiguration().set('fs.s3a.endpoint', f's3-{region}.amazonaws.com')

# release metadata from parquet
sc._jsc.hadoopConfiguration().set("parquet.enable.summary-metadata", "false")
spark = SparkSession(sc)

schema = StructType([
    StructField('author', StringType(), True),
    StructField('subreddit', StringType(), True),
    StructField('score', LongType(), True),
    StructField('num_comments', LongType(), True),
    StructField('num_crossposts', LongType(), True),
    StructField('title', StringType(), True),
    StructField('permalink', StringType(), True)])

path = f's3a://{bucket}/{key}'
df = spark.read.schema(schema).json(path).repartition(100)
df.printSchema()

path = f's3a://{bucket}/{outfile}'
df.coalesce(1).write.mode('append').save(path, format='parquet')

spark.stop()