from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine

from adapters import database, books_api, message_bus
from application import services


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)
    context = TransactionContext(bind=engine, expire_on_commit=False)
    books_repo = database.repositories.BookRepo(context=context)


class Application:
    books = services.BooksReadManager(
        books_repo=DB.books_repo,
    )


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.books)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBus.connection)


class Aspects:
    services.join_points.join(DB.context)
    books_api.join_points.join(DB.context)
