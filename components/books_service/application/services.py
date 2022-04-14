from typing import List, Union
import requests
from evraz.classic.app import DTO
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher

from . import interfaces, errors
from .dataclasses import Book

# разобрать что это и зачем
join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
    name: str
    author: str
    available: bool


@component
class BooksUpdaterManager:
    books_repo: interfaces.BookRepo
    publisher: Publisher
    SERVICE_SEARCH_URL = 'https://api.itbook.store/1.0/search/'
    SERVICE_BOOK_URL = 'https://api.itbook.store/1.0/books/'

    @join_point
    def create_and_get(self, book_id):
        response = requests.get(f'{self.SERVICE_BOOK_URL}{book_id}')
        response = response.json()
        book = Book(
            id=int(response.get('isbn13')),
            title=response.get('title'),
            subtitle=response.get('subtitle'),
            price=float(response.get('price')[1:]),
            rating=int(response.get('rating')),
            authors=response.get('authors'),
            publisher=response.get('publisher'),
            year=int(response.get('year')),
            pages=int(response.get('pages')),
            desc=response.get('desc'),
        )
        return book

    @join_point
    def add_books_package(self, books_package):
        self.books_repo.add_instance_package(books_package)


    @join_point
    def get_tag_from_rabbit(self, book_tag):
        # top_3_books = {}
        # TODO: не забыть убрать
        # book_tag = 'mongodb'
        print(f'Получен тэг {book_tag}')
        total_books = {}
        # Отправка первого запроса для получения количества книг:
        response = requests.get(f'{self.SERVICE_SEARCH_URL}{book_tag}')
        response = response.json()
        books_count = int(response.get('total'))
        pages_count = books_count // 10 + int((books_count % 10) > 0)
        if pages_count > 5:
            pages_count = 5

        print(f'Количество страниц для {book_tag}: {pages_count}')

        # Постраничный проход
        for page_num in range(pages_count):
            response = requests.get(f'{self.SERVICE_SEARCH_URL}{book_tag}/{page_num}')
            response = response.json()
            total_books[book_tag] = []

            # Для каждой книги создаем dataclass
            for book in response.get('books'):
                book_info = self.create_and_get(book.get('isbn13'))
                total_books[book_tag].append(book_info)

        for key, value in total_books.items():
            self.add_books_package(value)
            #Отпрвавка топ 3 книг по теме
            sorted_books = sorted(value, key=lambda x: (-int(x['rating']), x['year']))
            # top_3_books[key] = sorted_books[:3]

            self.publisher.publish(
                Message('BookSenderExchange', {key: sorted_books[:3]}),
            )

            print(f'Отправка топ книг по {key} в кролик')



@component
class BooksManager:
    books_repo: interfaces.BookRepo
    publisher: Publisher
    SERVICE_SEARCH_URL = 'https://api.itbook.store/1.0/search/'

    @join_point
    def filter_books(self, filters: dict):
        filter_price = filters.get('price')
        filter_title = filters.get('title')
        filter_authors = filters.get('authors')
        filter_publisher = filters.get('publisher')
        filter_order = filters.get('order_by', 'price')

        types = []

        if filter_price is not None:
            if isinstance(filter_price, List):
                filter_price = [price.split(':') for price in filter_price]
            else:
                filter_price = filter_price.split(':')
            types.append('price')
        if filter_title is not None:
            types.append('title')
        if filter_authors is not None:
            types.append('authors')
        if filter_publisher is not None:
            types.append('publisher')

        filters_params = filter(None, [filter_price, filter_title, filter_authors, filter_publisher])

        return self.books_repo.get_books(dict(zip(types, filters_params)), filter_order)


    @join_point
    def get_all_books(self):
        books = self.books_repo.get_all()
        if not books:
            raise errors.UncorrectedParams()
        return books


    @join_point
    def get_book_from_service(self, tags):
        for tag in tags:
            self.publisher.publish(
                Message('BookTagsExchange', {'book_tag': tag}),
            )
            print(f'Отправка {tag} в кролик')
