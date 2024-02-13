import os
import json
import asyncio
from services.email_service import EmailService
from model.email_model import EmailModel
from model.person_data import PersonData
from services.pulsar_consumer import create_pulsar_consumer
from pulsar.schema import AvroSchema

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

consumer = create_pulsar_consumer()


async def listen_pulsar_events():
    schema = AvroSchema(PersonData)
    while True:
        try:
            msg = consumer.receive()
            if msg is not None:
                data_bytes = msg.data()
                data_dict = json.loads(data_bytes)
                data = PersonData(**data_dict)
                await process_message(data)
                await consumer.acknowledge(msg)
            else:
                await asyncio.sleep(1)
        except Exception as e:
            print(f'Error: {str(e)}')

