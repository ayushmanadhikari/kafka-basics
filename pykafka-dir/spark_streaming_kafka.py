import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf


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

print("Printing Schema of query_df: ")
query_df.printSchema()

 

#query = df.writeStream.outputMode("complete").queryName("kaf_op").format("console").start()
#query.awaitTermination()

    