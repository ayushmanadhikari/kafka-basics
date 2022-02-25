from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.functions import explode, split


spark = SparkSession.builder.appName('localhost[3]').getOrCreate()

#creating a streaming data frame that listens to words on localhost some port
lines = spark.readStream.format("socket").option("host", 'localhost').option("port", '9999').load()

#split the lines into words
words = lines.select(explode(split(lines.value, " ")).alias("word"))

#generate running word count
wordCounts = words.groupBy("word").count()

#query to print the running counts to the console
query = wordCounts.writeStream.outputMode("complete").format("console").start()

#runs the query
query.awaitTermination()