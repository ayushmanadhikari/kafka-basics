
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import time
from pyspark.sql.types import *


#defining kafka constants
CONS_KAFKA_TOPIC = "test-demand3"
CONS_KAFKA_SERVER = "localhost:9092"


#starting a spark session to work with
spark = SparkSession.builder.appName("Spark_kafka").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")



#creating streaming dataframe
streaming_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", CONS_KAFKA_SERVER)\
    .option("subscribe", CONS_KAFKA_TOPIC).option("startingOffsets", "earliest").load()
#selecting the key and value components of the query_df 
streaming_df = streaming_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


#splitting the read serialized data obtained by query_df into columns with split function of pyspark.spl.functions
split_col = split(streaming_df['value'], ',')


#organizing data into columns in query_df and storing in query_df with columns for each type of key value pair 
streaming_df = streaming_df.withColumn('Id', split_col.__getitem__(0))
streaming_df = streaming_df.withColumn('name', split_col.__getitem__(1))
streaming_df = streaming_df.withColumn('email', split_col.__getitem__(2))
streaming_df = streaming_df.withColumn('age', split_col.__getitem__(3))
streaming_df = streaming_df.withColumn('event', split_col.__getitem__(4))
streaming_df = streaming_df.withColumn('latitude', split_col.__getitem__(5))
streaming_df = streaming_df.withColumn('longitude', split_col.__getitem__(6))
streaming_df = streaming_df.withColumn('timestamp', split_col.__getitem__(7))



#removing the key from the data values in each column and only keeping the corresponding values
col_array = ['Id', 'name', 'email', 'age', 'event', 'latitude', 'longitude', 'timestamp']
df_temp = streaming_df
for col in col_array:
    split_temp = split(df_temp[col], ":")
    df_temp = df_temp.withColumn(col, split_temp.__getitem__(1))


##cleaning the timestamp field by removing the prepending character "
time_split = split(df_temp['timestamp'], '"')
df_temp = df_temp.withColumn('timestamp', time_split.__getitem__(1) )



#selecting the columns to stream into console using columned-query_df
final_op_stream_df = df_temp.selectExpr("Id", "latitude", "longitude", "event", "timestamp")
#streaming the data into console 
final_op_stream_df = final_op_stream_df.writeStream.format("console").start()
time.sleep(10)
#stopping the streaming data
final_op_stream_df.stop()




#writing the streaming dataframe into mysql rdbms
selected_streaming_df = df_temp.select("Id", "event", "latitude", 'longitude', "timestamp")

db_properties = {'user': 'root', 'password': ''}
#def for_each_batch(df, id):
#    df.write.option("driver", "com.mysql.jdbc.Driver").mode('append').jdbc(url='jdbc:mysql://localhost:3306/test', table='demand_supply', properties=db_properties)
#    pass

#query = selected_streaming_df.writeStream.foreachBatch(for_each_batch).start()
#print("writing to database..............")
time.sleep(10)
#query.stop()



    