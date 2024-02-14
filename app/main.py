import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from service.kafka_event_handler import listen_kafka_events

load_dotenv()
app = FastAPI()


async def startup_event_handler():
    await asyncio.create_task(listen_kafka_events())


@app.on_event("startup")
async def startup_event():
    await startup_event_handler()
