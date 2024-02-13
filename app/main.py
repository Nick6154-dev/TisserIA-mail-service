import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from services.pulsar_event_handler import listen_pulsar_events

load_dotenv()
asyncio.create_task(listen_pulsar_events())
app = FastAPI()
