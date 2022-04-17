import datetime
import threading
from typing import List, Optional

import requests
from pydantic import validate_arguments

from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import Book, Booking

join_points = PointCut()
join_point = join_points.join_point


@component
class BookingManager:
    booking_repo: interfaces.BookingRepo
    books_repo: interfaces.BookRepo
    publisher: Publisher

    @join_point
    def get_by_id(self, booking_id):
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise errors.UncorrectedParams

        return booking

    @join_point
    def get_by_book_id(self, book_id):
        booking = self.booking_repo.get_by_book_id(book_id=book_id)
        return booking

    @join_point
    def get_by_user_id(self, user_id):
        booking = self.booking_repo.get_by_user_id(user_id=user_id)
        return booking

    @join_point
    def set_booking_datetime_for_book(
        self, book_id: int, booking_datetime: datetime.datetime
    ):
        book = self.books_repo.get_by_id(book_id=book_id)
        book.booking_datetime = booking_datetime.strftime('%Y-%m-%d %H:%M:%S')
        self.books_repo.add_instance(book)

    @join_point
    def make_book_redeemed(self, book_id: int):
        book = self.books_repo.get_by_id(book_id=book_id)
        book.redeemed = True
        self.books_repo.add_instance(book)

    @join_point
    def make_book_unredeemed(self, book_id: int):
        book = self.books_repo.get_by_id(book_id=book_id)
        book.redeemed = False
        self.books_repo.add_instance(book)

    @join_point
    def get_active_booking(self, user_id):
        booking = self.get_by_user_id(user_id=user_id)
        if booking.redeemed or booking.expiry_datetime < datetime.datetime.now(
        ):
            raise errors.UserNoActiveBooking
        return booking

    @join_point
    def check_book_available(self, book_id, user_id):
        # Проверяем существование книги
        if not self.books_repo.get_by_id(book_id):
            raise errors.UncorrectedParams

        # Достаем последнюю бронь пользователя
        users_booking = self.get_by_user_id(user_id=user_id)

        if users_booking:
            # Если у него все еще есть активная бронь, кидаем ошибку
            if users_booking.expiry_datetime > datetime.datetime.now(
            ) and not users_booking.redeemed:
                raise errors.UserAlreadyHaveBooking

        # Достаем последнюю бронь по данной книге
        booking = self.get_by_book_id(book_id)

        # Если никаких заявок на книгу не было
        if booking is None:
            return True

        # Если брони есть, то смотрим, не вышел ли срок
        if booking.expiry_datetime > datetime.datetime.now():
            raise errors.BookAlreadyBooked

        return True

    @join_point
    def check_permission(self, booking_id: int, user_id: int):
        booking = self.get_by_id(booking_id)
        if booking.user_id == user_id:
            return True

    @join_point
    def booking_book(
        self, book_id: int, user_id: int, period: Optional[int] = 7
    ):
        if self.check_book_available(book_id=book_id, user_id=user_id):
            booking = Booking(
                book_id=book_id,
                user_id=user_id,
                created_datetime=datetime.datetime.now(),
                expiry_datetime=datetime.datetime.now() +
                datetime.timedelta(days=period)
            )
            self.booking_repo.add_instance(booking)

            # Ставим книге дату окончания бронирования:
            self.set_booking_datetime_for_book(
                book_id=book_id,
                booking_datetime=datetime.datetime.now() +
                datetime.timedelta(days=period)
            )

    @join_point
    def delete_booking(self, booking_id: int, user_id: int):
        if self.check_permission(booking_id=booking_id, user_id=user_id):
            booking = self.get_by_id(booking_id)
            if booking is None:
                raise errors.UncorrectedParams

            if booking.expiry_datetime < datetime.datetime.now(
            ) or booking.redeemed:
                raise errors.BookingIsUnavailable

            booking.expiry_datetime = datetime.date(1800, 10, 10)
            self.booking_repo.add_instance(booking)

    @join_point
    def redeem_booking(self, booking_id: int, user_id: int):
        if not self.check_permission(booking_id=booking_id, user_id=user_id):
            raise errors.NoPermission

        booking = self.get_by_id(booking_id)

        if booking.expiry_datetime < datetime.datetime.now(
        ) or booking.redeemed == True:
            raise errors.BookingIsUnavailable

        booking.expiry_datetime = datetime.date(2800, 10, 10)
        booking.redeemed = True

        # Делаем книгу недоступной
        self.make_book_redeemed(booking.book_id)

        self.booking_repo.add_instance(booking)

    @join_point
    def get_all_users_booking(self, user_id: int):
        return self.booking_repo.get_users_booking(user_id=user_id)


@component
class BooksUpdaterManager:
    books_repo: interfaces.BookRepo
    publisher: Publisher
    SERVICE_SEARCH_URL = 'https://api.itbook.store/1.0/search/'
    SERVICE_BOOK_URL = 'https://api.itbook.store/1.0/books/'

    @join_point
    def create_and_get(
        self, book_id: str, service_tag: str, batch_datetime: str
    ):
        response = requests.get(f'{self.SERVICE_BOOK_URL}{book_id}')
        if response.status_code == 404:
            raise errors.DownloadError

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
            service_tag=service_tag,
            batch_datetime=batch_datetime
        )
        return book

    @join_point
    def add_books_package(self, books_package: list):
        self.books_repo.add_instance_package(books_package)

    @join_point
    def send_top_books(self, tags: list, batch_datetime: str):
        top_books = {}
        for tag in tags:
            top_books[tag] = self.books_repo.get_top_by_tag(
                tag=tag, batch_datetime=batch_datetime
            )
            top_books[tag] = [
                {
                    'title': book.title,
                    'authors': book.authors,
                    'rating': book.rating,
                    'year': book.year,
                    'price': book.price
                } for book in top_books[tag]
            ]
        if top_books:
            self.publisher.publish(
                Message('UserRegistrationExchange', {'top_books': top_books}),
            )

    @join_point
    def get_tag_from_rabbit(self, book_tags: list, batch_datetime: str):
        total_books = {}

        # Отправка первого запроса для получения количества книг:
        for book_tag in book_tags:
            response = requests.get(f'{self.SERVICE_SEARCH_URL}{book_tag}')
            response = response.json()
            total_books[book_tag] = []
            books_count = int(response.get('total'))
            pages_count = books_count // 10 + int((books_count % 10) > 0)
            pages_count = pages_count if pages_count <= 5 else 5

            # Постраничный проход
            for page_num in range(1, pages_count + 1):
                response = requests.get(
                    f'{self.SERVICE_SEARCH_URL}{book_tag}/{page_num}'
                )
                response = response.json()

                # Для каждой книги создаем dataclass
                for book in response.get('books'):
                    book_info = self.create_and_get(
                        book.get('isbn13'),
                        service_tag=book_tag,
                        batch_datetime=batch_datetime
                    )
                    total_books[book_tag].append(book_info)

        for key, value in total_books.items():
            self.add_books_package(value)

        self.send_top_books(book_tags, batch_datetime)

    @join_point
    def get_by_pages(self, page_num, book_tag, batch_datetime):
        response = requests.get(
            f'{self.SERVICE_SEARCH_URL}{book_tag}/{page_num}'
        )
        response = response.json()
        total_books = []
        # Для каждой книги создаем dataclass
        for book in response.get('books'):
            book_info = self.create_and_get(
                book.get('isbn13'),
                service_tag=book_tag,
                batch_datetime=batch_datetime
            )
            total_books.append(book_info)

        self.books_repo.add_instance_package(total_books)

    @join_point
    def get_tag_from_rabbit_async(self, book_tags: list, batch_datetime: str):
        total_books = {}

        # Отправка первого запроса для получения количества книг:
        for book_tag in book_tags:
            response = requests.get(f'{self.SERVICE_SEARCH_URL}{book_tag}')
            response = response.json()
            total_books[book_tag] = []
            # Список для тредов
            threads = []
            books_count = int(response.get('total'))
            pages_count = books_count // 10 + int((books_count % 10) > 0)
            pages_count = pages_count if pages_count <= 5 else 5

            # Постраничный проход
            for page_num in range(1, pages_count + 1):
                thread = threading.Thread(
                    target=self.get_by_pages,
                    args=(
                        page_num,
                        book_tag,
                        batch_datetime,
                    )
                )
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        self.send_top_books(book_tags, batch_datetime)


@component
class BooksManager:
    books_repo: interfaces.BookRepo
    publisher: Publisher
    SERVICE_SEARCH_URL = 'https://api.itbook.store/1.0/search/'

    @join_point
    @validate_arguments
    def get_book_by_id(self, book_id: int) -> Book:
        book = self.books_repo.get_by_id(book_id)
        if not book:
            raise errors.UncorrectedParams()
        return book

    @join_point
    def filter_books(self, filters: dict):
        filter_price = filters.get('price')
        filter_keyword = filters.get('keyword')
        filter_authors = filters.get('authors')
        filter_publisher = filters.get('publisher')
        sorting_key = filters.get('order_by', 'price')
        types = []

        if filter_price is not None:
            if isinstance(filter_price, List):
                filter_price = [price.split(':') for price in filter_price]
            else:
                filter_price = filter_price.split(':')
            types.append('price')
        if filter_keyword is not None:
            types.append('keyword')
        if filter_authors is not None:
            types.append('authors')
        if filter_publisher is not None:
            types.append('publisher')

        filters_params = filter(
            None,
            [filter_price, filter_keyword, filter_authors, filter_publisher]
        )

        return self.books_repo.get_books_with_filters(
            dict(zip(types, filters_params)), sorting_key
        )

    @join_point
    def get_all_books(self):
        books = self.books_repo.get_all()
        if not books:
            raise errors.UncorrectedParams
        return books

    @join_point
    def get_book_from_service(self, tags):
        if not tags:
            raise errors.UncorrectedParams
        # Фиксируем время "партии"
        batch_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.publisher.publish(
            Message(
                'BookTagsExchange', {
                    'book_tags': tags,
                    'batch_datetime': batch_datetime
                }
            ),
        )
