import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from service.email_service import EmailService
from service.kafka_event_handler import listen_kafka_events

load_dotenv()
email_service = EmailService()
asyncio.create_task(listen_kafka_events())
app = FastAPI()
