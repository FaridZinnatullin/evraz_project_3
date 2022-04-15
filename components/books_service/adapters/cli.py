import click
from composites.api import Application as app


def create_cli():

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def get_books(tags):
        app.books_manager.get_book_from_service(tags=tags)

    return cli
