import jwt
import os

import jwt
from evraz.classic.components import component
from evraz.classic.http_auth import (
    authenticate,
    authenticator_needed,
    authorize,
)

from application import services
from .join_points import join_point


@authenticator_needed
@component
class Books:
    books_manager: services.BooksManager

    @join_point
    @authenticate
    def on_get_book_info(self, request, response):
        book = self.books_manager.get_book_by_id(**request.params)
        result = {
            'book_id': book.id,
            'book_name': book.name,
            'book_author': book.author,
            'book_available': book.available
        }
        response.media = result

    @join_point
    @authenticate
    def on_get_books(self, request, response, **kwargs):
        book = self.books_manager.get_book_by_id(**request.params)
        result = {
            'book_id': book.id,
            'book_name': book.name,
            'book_author': book.author,
            'book_available': book.available
        }
        response.media = result

    @join_point
    @authenticate
    def on_post_take_book(self, request, response):
        self.books_manager.get_book(**request.media)

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        self.books_manager.return_book(**request.media)


    @join_point
    @authenticate
    def on_post_create(self, request, response):
        self.books_manager.create(**request.media)


    @join_point
    @authenticate
    def on_post_delete(self, request, response):
        self.books_manager.delete_book(**request.media)


