from pykafka import KafkaClient

#creating a client to work with
client = KafkaClient('localhost:9092')

#finding topics
topics = client.topics
print(topics)
#selecting 1 topic from available topics
topic = client.topics['test']


#creating producer and consumer for particular topic
producer = topics.get
