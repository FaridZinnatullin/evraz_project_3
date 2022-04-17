import os

import pytest
from components.books_service.adapters.database.tables import metadata
from sqlalchemy import create_engine

from evraz.classic.sql_storage import TransactionContext


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(f'postgresql://' \
                           f'{os.getenv("POSTGRES_USERS_USER", "barash")}:' \
                           f'{os.getenv("POSTGRES_USERS_PASSWORD", "test_password")}@' \
                           f'{os.getenv("POSTGRES_USERS_HOST", "127.0.0.1")}:' \
                           f'{os.getenv("POSTGRES_USERS_PORT", "5432")}/' \
                           f'{os.getenv("POSTGRES_USERS_DBNAME", "evraz_project_3_books_service")}')

    for key, value in metadata.tables.items():
        value.schema = None

    metadata.create_all(engine)

    return engine


@pytest.fixture(scope='session')
def transaction_context(engine):
    return TransactionContext(bind=engine)


@pytest.fixture(scope='function')
def session(transaction_context: TransactionContext):
    session = transaction_context.current_session

    if session.in_transaction():
        session.begin_nested()
    else:
        session.begin()

    yield session

    session.rollback()
