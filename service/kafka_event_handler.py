import os
import json
from confluent_kafka import KafkaError
from service.email_service import EmailService
from model.email_model import EmailModel
from model.person_data import PersonData
from service.kafka_consumer import create_kafka_consumer

email_service = EmailService()


def create_to_send_object(in_production, full_name, to_send):
    if in_production:
        return [
            {
                "name": full_name,
                "email": to_send
            }
        ]
    else:
        return [
            {
                "name": "Pablo Balseca",
                "email": "nikomont123@gmail.com"
            }
        ]


async def send_new_user_notification_mail_event_kafka(data: PersonData):
    try:
        production_mode = os.environ.get('PRODUCTION_MODE', 'False').lower() == 'true'
        email_model = EmailModel(
            "Registro Sistema Devengamiento - " + data.fullName,
            {"name": "YPS_SYSTEMS", "email": "yps_systems@outlook.com"},
            create_to_send_object(production_mode, data.fullName, data.toSend),
            "<html><body><h1>Just for test</h1></body></html>",
            {
                "fullName": data.fullName,
                "userMail": data.userMail,
                "password": data.password
            },
            data.template_id
        )
        await email_service.send_email(email_model)
    except Exception as e:
        print("Error sending: " + str(e))


async def process_message(data):
    template_id = data.template_id
    if template_id == 10:
        await send_new_user_notification_mail_event_kafka(data)
    else:
        print(f"Unhandled template_id: {template_id}")

consumer = create_kafka_consumer()


async def listen_kafka_events():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            break
        try:
            data_dictionary = json.loads(msg.value())
            data = PersonData(**data_dictionary)
            await process_message(data)
        except json.JSONDecodeError as e:
            print('Error decoding JSON:', e)
        except KeyError as e:
            print('Missing key in dictionary:', e)
