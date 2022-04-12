from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine

from adapters import database, users_api, message_bus
from application import services


class Settings:
    db_settings = database.Settings()
    message_bus_settings = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db_settings.DB_URL, echo=True)
    # database.metadata.drop_all(engine)
    database.metadata.create_all(engine)
    context = TransactionContext(bind=engine)

    users_repo = database.repositories.UsersRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus_settings.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
    )


class Application:
    users_manager = services.UsersManager(
        users_repo=DB.users_repo,
        publisher=MessageBus.publisher,
    )


class Aspects:
    services.join_points.join(DB.context)
    users_api.join_points.join(MessageBus.publisher, DB.context)


app = users_api.create_app(
    users_manager=Application.users_manager,
)
