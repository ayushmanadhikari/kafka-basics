from pyspark.sql.functions import *
from pyspark.sql import SparkSession
import time
import mysql.connector


spark = SparkSession.builder.appName('test-session').getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df_read_stream = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092")\
                    .option("subscribe", "test-demand2").option("startingOffsets", "earliest").load()

df_read_stream = df_read_stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

split_col = split(df_read_stream['value'], ",")

df_read_stream = df_read_stream.withColumn('ID', split_col.__getitem__(0))
df_read_stream = df_read_stream.withColumn('name', split_col.__getitem__(1))
df_read_stream = df_read_stream.withColumn('email', split_col.__getitem__(2))
df_read_stream = df_read_stream.withColumn('age', split_col.__getitem__(3))
df_read_stream = df_read_stream.withColumn('event', split_col.__getitem__(4))
df_read_stream = df_read_stream.withColumn('coordinate', split_col.__getitem__(5))
df_read_stream = df_read_stream.withColumn('timestamp', split_col.__getitem__(6))


col_array = ['ID', 'name', 'email', 'age', 'event', 'coordinate', 'timestamp']
df_temp = df_read_stream

for col_name in col_array:
    split_temp = split(df_temp[col_name], ":")
    df_temp = df_temp.withColumn(col_name, split_temp.__getitem__(1))
    

#df_write_stream = df_read_stream.selectExpr('ID', 'name', 'email', "event", "coordinate", "timestamp")

df_temp = df_temp.selectExpr(col_array)
#df_write_stream = df_temp.writeStream.format("console").trigger(processingTime='1 second').start()
time.sleep(2)

#df_write_stream.stop()


#establish mysql connection
conn = mysql.connector.connect(user='root', database='test', password='', host='localhost', port=3306)
if conn:
    print("connection established........")
else:
    print("error in establishing connection")


df_rdbms = df_temp.select("ID", "name", "coordinate")


#writing the selected streaming dataframe into mysql rdbms
db_target_properties = {'user': 'root', 'password': ''}

def for_each_batch_function(df, epoch_id):
    df.write.option("driver", "com.mysql.jdbc.Driver").mode("append").jdbc(url='jdbc:mysql://localhost:3306/test', table='test_data', properties=db_target_properties)
    pass

query = df_rdbms.writeStream.foreachBatch(for_each_batch_function).start()
query.awaitTermination()


