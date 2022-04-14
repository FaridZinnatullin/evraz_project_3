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
    books_updater: services.BooksUpdaterManager

    @join_point
    def on_post_test_data(self, request, response):
        self.books_updater.get_tag_from_rabbit('rabbitmq')

    @join_point
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
    def on_get_all_books(self, request, response):
        books = self.books_manager.get_all_books(**request.params)
        result = [{
            'book_id': book.id,
            'book_title': book.title,
            'book_authors': book.authors,
            'book_rating': book.rating
        } for book in books]
        response.media = result


    @join_point
    def on_get_show_filters(self, request, response):
        books = self.books_manager.filter_books(request.params)
        response.media = [
            {
                'title': book.title,
                'subtitle': book.subtitle,
                'price': book.price,
                'rating': book.rating,
                'authors': book.authors,
                'publisher': book.publisher,
                'year': book.year,
                'pages': book.pages
            } for book in books
        ]




