import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BROKER_URL: str = f'amqp://' \
                      f'{os.getenv("RABBITMQ_USER", "user")}:' \
                      f'{os.getenv("RABBITMQ_PASSWORD", "password")}@' \
                      f'{os.getenv("RABBITMQ_HOST", "127.0.0.1")}:' \
                      f'{os.getenv("RABBITMQ_PORT", "5672")}'

