#medium_geojson


from pykafka import KafkaClient

import json
import uuid
from datetime import datetime
import time


#setting up kafkaclient, kafkatopic, producer and consumer
kafka_client = KafkaClient('localhost:9092')
kafka_topic = kafka_client.topics['test']
producer = kafka_topic.get_producer()
consumer = kafka_topic.get_simple_consumer()


#reading the json corrdinates files and storing its coordinates
input_file = open('geo_json.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']


#creating empty dictionary to add key, value data and to later dump/serialize and produce message with
data = {}
data['busline'] = '000001'


#constructing our messages and prdocuing them to kafka
def generate_checkpoints(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(uuid.uuid4())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)

        #if bus reaches last coordinate, start from beginning
        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1


#calling the function with our custom coordinates
generate_checkpoints(coordinates)

        

#working with consumer to consume the previously produced data
