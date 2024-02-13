import os
import pulsar


def create_pulsar_consumer():
    client = pulsar.Client(os.environ.get('PULSAR_SERVER', 'pulsar://localhost:6650'))
    topic_to_subscribe = os.environ.get('PULSAR_TOPIC_TO_SUBSCRIBE', 'email-topic')
    consumer = client.subscribe(topic_to_subscribe, os.environ.get('PULSAR_SUBSCRIPTION', 'email-subscription'))
    return consumer
