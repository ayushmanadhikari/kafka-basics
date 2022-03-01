from typing import final
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
import time

spark = SparkSession.builder.appName("Spark-kafka").getOrCreate()

#creating streaming dataframe
query_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", 'test-demand').option("startingOffsets", "earliest").load()
query_df = query_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


#query_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)").writeStream.format("console").start()
split_col = split(query_df['value'], ',')
query_df = query_df.withColumn('Id', split_col.__getitem__(0))
query_df = query_df.withColumn('name', split_col.__getitem__(1))
query_df = query_df.withColumn('email', split_col.__getitem__(2))
query_df = query_df.withColumn('age', split_col.__getitem__(3))
query_df = query_df.withColumn('event-type', split_col.__getitem__(4))
query_df = query_df.withColumn('coordinate', split_col.__getitem__(5))
query_df = query_df.withColumn('timestamp', split_col.__getitem__(6))

final_op_stream_df = query_df.selectExpr("Id", "age", "coordinate", "timestamp")
write_stream_df_op_query = final_op_stream_df.writeStream.format("console").trigger(processingTime='1 seconds').start()
time.sleep(10)
write_stream_df_op_query.stop()

#print("Printing Schema of query_df: ")
#query_df.printSchema()
print("output stream................")
#write_stream_df_op_query.awaitTermination()


 

#query = df.writeStream.outputMode("complete").queryName("kaf_op").format("console").start()
#query.awaitTermination()

    