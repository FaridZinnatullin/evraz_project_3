from pydantic import BaseSettings
import os
from dotenv import load_dotenv


class Settings(BaseSettings):

    @property
    def DB_URL(self):
        DATABASE_URL: str = f'postgresql://' \
                            f'{os.getenv("POSTGRES_BOOKS_USER", "barash")}:' \
                            f'{os.getenv("POSTGRES_BOOKS_PASSWORD", "test_password")}@' \
                            f'{os.getenv("POSTGRES_BOOKS_HOST", "127.0.0.1")}:' \
                            f'{os.getenv("POSTGRES_BOOKS_PORT", "5432")}/' \
                            f'{os.getenv("POSTGRES_BOOKS_DBNAME", "evraz_project_3_books_service")}'

        return DATABASE_URL
