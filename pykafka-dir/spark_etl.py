from posixpath import split
from parso import split_lines
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import *




spark = SparkSession.builder.appName('new_session').getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

readin_stream = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option(
            "subscribe", "test-demand3").option("startingOffsets", "earliest").load()


readin_stream = readin_stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


split_col = split(readin_stream['value'], ',')

readin_stream = readin_stream.withColumn('Id', split_col.__getitem__(0))



final_op = readin_stream.selectExpr('Id')
 

op_stream = final_op.writeStream.outputMode("append").format("console").start()


