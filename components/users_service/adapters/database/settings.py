import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    @property
    def DB_URL(self):

        DATABASE_URL: str = f'postgresql://' \
                            f'{os.getenv("POSTGRES_USERS_USER", "barash")}:' \
                            f'{os.getenv("POSTGRES_USERS_PASSWORD", "test_password")}@' \
                            f'{os.getenv("POSTGRES_USERS_HOST", "127.0.0.1")}:' \
                            f'{os.getenv("POSTGRES_USERS_PORT", "5432")}/' \
                            f'{os.getenv("POSTGRES_USERS_DBNAME", "evraz_project_3_users_service")}'

        return DATABASE_URL
