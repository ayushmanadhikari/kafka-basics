from pyspark.sql.functions import *
from pyspark.sql import SparkSession
import time

spark = SparkSession.builder.appName('test-session').getOrCreate()

df_read_stream = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092")\
                    .option("subscribe", "test-demand").option("startingOffsets", "earliest").load()

df_read_stream = df_read_stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
df_write_stream = df_read_stream.writeStream.format("console").trigger(processingTime='1 second').start()
time.sleep(10)

df_write_stream.stop()



spark = SparkSession.builder.appName("someName").getOrCreate()

df_read_query = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092")\
                    .option("subscribe", "test-demand").option("startingOffsets", "earliest").load()

df_read_query = df_read_query.selectExpr("CAST key AS STRING", "CAST value AS STRING")

df_write_query = df_read_query.writeStream.format("console").start()
time.sleep(10)
df_write_query.stop()