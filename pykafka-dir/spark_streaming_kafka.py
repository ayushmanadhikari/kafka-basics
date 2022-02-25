from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf


spark = SparkSession.builder.appName("Spark-kafka").getOrCreate()

#creating streaming dataframe
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", 'test-demand').load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


query = df.writeStream.outputMode("append").format("console").start()
query.awaitTermination()

