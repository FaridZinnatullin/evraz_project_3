import click
from composites.api import Application as app
from threading import Thread

def create_cli():

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def get_books(tags):
        app.books_manager.get_book_from_service(tags=tags)

    # @cli.command()
    # def consumer():
    #     MessageBus.declare_scheme()
    #     consumer = Thread(target=MessageBus.consumer.run, daemon=True)
    #     consumer.start()
    #     print('Типа запустили консьюмера')

    return cli

# books_service get-books mongodb python sharp