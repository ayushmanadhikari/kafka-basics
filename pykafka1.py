from pykafka import KafkaClient

client = KafkaClient("localhost: 9092")


#calling a topic
topic = client.topics["new-topic"]

print(topic)
