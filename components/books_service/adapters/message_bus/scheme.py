from kombu import Exchange, Queue

from evraz.classic.messaging_kombu import BrokerScheme

broker_scheme = BrokerScheme(
    Queue('BookTagsQueue', Exchange('BookTagsExchange')),
    Queue('TopBooksQueue', Exchange('TopBooksExchange')),
)
