import os
from confluent_kafka import Consumer


def create_kafka_consumer():
    conf = {
        'bootstrap.servers': os.environ.get('KAFKA_SERVER', 'localhost:9094'),
        'group.id': os.environ.get('KAFKA_GROUP_ID', 'mail-producer'),
        'auto.offset.reset': 'earliest'
    }
    topic_to_subscribe = os.environ.get('KAFKA_TOPIC_TO_SUBSCRIBE', 'email-topic')
    consumer = Consumer(conf)
    consumer.subscribe([topic_to_subscribe])
    return consumer
