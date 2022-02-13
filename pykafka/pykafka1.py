from pykafka import KafkaClient


client = KafkaClient("localhost: 9092")


#calling a topic
topic = client.topics["new-topic"]


#creating a new topic
test_topic = client.create_topic('test_topic', partitions = 2, replicas=3)


print(topic)
