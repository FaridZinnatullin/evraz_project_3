from kombu import Connection

from evraz.classic.messaging_kombu import KombuConsumer

from application import services

from .scheme import broker_scheme


def create_consumer(connection: Connection, books: services.BooksUpdaterManager) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        books.get_tag_from_rabbit,
        'BookTagsQueue',
    )

    return consumer

