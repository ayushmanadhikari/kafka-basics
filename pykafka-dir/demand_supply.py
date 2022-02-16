import json
import random
from pykafka import KafkaClient
from datetime import datetime
import time
from faker import Faker



#creating instances of Kafka variables
kafka_client = KafkaClient('localhost:9092')
kafka_topic = kafka_client.topics['test-demand']
producer = kafka_topic.get_producer()
consumer = kafka_topic.get_simple_consumer()



#initializing necessary variables
captain_data = {}
user_data = {}
id = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
age = [21,20,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
fake = Faker()


#generates captain data and produces to the demand_supply topic every 1 minute
def gen_captain_data():
    i = 0
    while i<5:
        captain_data['capId'] = random.choice(id)
        captain_data['name'] = fake.name()
        captain_data['email'] = fake.email()
        captain_data['age'] = random.choice(age)
        captain_data['event-type'] = 'captain'
        mssg = json.dumps(captain_data)
        producer.produce(mssg.encode('ascii'))
        i += 1
        time.sleep(4)




#generates user data and produces to the demand_supply topic every 2 minutes
def gen_user_data():
    j = 0
    while j<5:
        user_data['userId'] = random.choice(id)
        user_data['name'] = fake.name()
        user_data['email'] = fake.email()
        user_data['age'] = random.choice(age)
        user_data['event-type'] = 'user'
        msg = json.dumps(user_data)
        producer.produce(msg.encode('ascii'))
        j += 1
        time.sleep(10)



if __name__ == '__main__':
    gen_captain_data()
    gen_user_data()
    
