from threading import Thread

from kombu import Connection
from sqlalchemy import create_engine

from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext

from adapters import books_api, database, message_bus
from application import services


class Settings:
    db = database.Settings()
    books_api = books_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)
    # database.metadata.drop_all(engine)
    database.metadata.create_all(engine)
    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BookRepo(context=context)
    booking_repo = database.repositories.BookingRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:
    books_manager = services.BooksManager(
        books_repo=DB.books_repo,
        publisher=MessageBus.publisher,
    )

    books_updater = services.BooksUpdaterManager(
        books_repo=DB.books_repo,
        publisher=MessageBus.publisher,
    )

    booking_manager = services.BookingManager(
        books_repo=DB.books_repo,
        booking_repo=DB.booking_repo,
        publisher=MessageBus.publisher,
    )



class Aspects:
    services.join_points.join(DB.context)
    books_api.join_points.join(MessageBus.publisher, DB.context)


app = books_api.create_app(
    books_manager=Application.books_manager,
    books_updater=Application.books_updater,
    booking_manager=Application.booking_manager
)

