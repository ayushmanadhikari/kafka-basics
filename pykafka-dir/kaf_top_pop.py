import json 
from pykafka import KafkaClient


KAFKA_SERVER = 'localhost:9092'
KAFKA_TOPIC = 'test-demand3'

kafka_client = KafkaClient(KAFKA_SERVER)
kafka_topic = kafka_client.topics[KAFKA_TOPIC]

producer = kafka_topic.get_producer()
consumer = kafka_topic.get_simple_consumer()


def produce_msg():
    sam_dict = {'key1': 'value1', 'key2': 'value2'}
    mssg = json.dumps(sam_dict)
    producer.produce(mssg.encode('ascii'))



if __name__ == '__main__':
    produce_msg()
    for mssg in consumer:
        print(f'{mssg.offset}: {mssg.value}')
    
    