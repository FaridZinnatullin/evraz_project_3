import requests
from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher
from pydantic import validate_arguments

from . import errors, interfaces
from .dataclasses import Book

# разобрать что это и зачем
join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
    name: str
    author: str
    available: bool

@component
class BooksReadManager:
    books_repo: interfaces.BookRepo




@component
class BooksManager:
    books_repo: interfaces.BookRepo
    publisher: Publisher

    @join_point
    @validate_with_dto
    def create(self, book_data: BookInfo):

        book = Book(name=book_data.name,
                    author=book_data.author,
                    available=book_data.available)

        if not self.books_repo.get_by_name_author(author=book_data.author, name=book_data.name):
            book = self.books_repo.add_instance(book)

            self.publisher.plan(
                Message('LogsExchange', {'action': 'create',
                                         'object_type': 'book',
                                         'object_id': book.id
                                         })
            )
        else:
            raise errors.BookAlreadyExist

    @join_point
    @validate_arguments
    def get_book_by_id(self, book_id: int) -> Book:
        book = self.books_repo.get_by_id(book_id)
        if not book:
            raise errors.UncorrectedParams()
        return book

    @join_point
    @validate_arguments
    def get_all_books(self):
        return self.books_repo.get_all()

    @join_point
    @validate_arguments
    def delete_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        if book:
            self.books_repo.delete_by_id(book_id)
        else:
            raise errors.UncorrectedParams()

        self.publisher.plan(
            Message('LogsExchange', {'action': 'delete',
                                     'object_type': 'book',
                                     'object_id': book.id
                                     })
        )

    @join_point
    @validate_arguments
    def get_book(self, book_id: int, user_id: int):
        book = self.get_book_by_id(book_id)
        if book:
            if book.available:
                book.available = False
                self.books_repo.add_instance(book)
                self.publisher.plan(
                    Message('LogsExchange', {'action': 'get book',
                                             'object_type': 'book',
                                             'object_id': book_id
                                             }),

                    Message('LogsExchange', {'action': 'user get book',
                                             'object_type': 'user',
                                             'object_id': user_id
                                             })
                )
            else:
                raise errors.BookIsUnavailable
        else:
            raise errors.UncorrectedParams

    @join_point
    @validate_arguments
    def return_book(self, book_id: int, user_id: int):
        book = self.get_book_by_id(book_id)
        if book:
            book.available = True
            self.books_repo.add_instance(book)
            self.publisher.plan(
                Message('LogsExchange', {'action': 'return book',
                                         'object_type': 'book',
                                         'object_id': book_id
                                         }),

                Message('LogsExchange', {'action': 'user return book',
                                         'object_type': 'user',
                                         'object_id': user_id
                                         })
            )

    # @join_point
    # def send_book_to_rabbit(self, book_id: int, book_tag: str):
    #

    @join_point
    def get_books_from_tag(self, book_tag: str, pages_total: int):
        SERVICE_SEARCH_URL = 'https://api.itbook.store/1.0/search/'

        for page_num in range(pages_total):
            response = requests.get(f'{SERVICE_SEARCH_URL}{book_tag}/{page_num}')
            response = response.json()
            for book in response.get('books'):
                pass

    @join_point
    def get_from_rabbit(self, book_tag):
        print(f'Получен тэг {book_tag}')


    @join_point
    def get_book_from_service(self, tags):
        self.publisher.publish(
            Message('BookTagsExchange', {'book_tag': 12344}),
        )
        for tag in tags:
            self.publisher.publish(
                Message('BookTagsExchange', {'book_tag': tag}),
            )
            print(f'Отправка {tag} в кролик')
            # response = requests.get(f'{SERVICE_SEARCH_URL}{tag}')
            # response = response.json()
            # total = int(response.get('total'))
            # requests_for_book = total // 10 + int((total % 10) > 0)
            # print(requests_for_book)
            # self.publisher.plan(
            #
            #         )
            # self.get_books_from_tag(tag, requests_for_book)

            # for book in response.get('books'):
            #     self.send_book_to_rabbit(book_id=book.get('idbn13'),
            #                              book_tag=tag)
            #
            # print(response)
            # print(f'Количество страниц: {requests_for_book}')

    # @join_point
    # def get_books_from_tag(self, tags):
