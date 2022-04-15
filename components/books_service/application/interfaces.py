from abc import ABC, abstractmethod
from typing import List, Union

from .dataclasses import Book


class BookRepo(ABC):

    @abstractmethod
    def get_by_id(self, book_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add_instance(self, book_data):
        pass

    @abstractmethod
    def delete_by_id(self, book_id: int):
        pass

    @abstractmethod
    def update_by_id(self, book: Book):
        pass

    @abstractmethod
    def get_by_name_author(self, author: str, name: str):
        pass

    @abstractmethod
    def add_instance_package(self, instances_package: list):
        pass

    @abstractmethod
    def get_books(self, params: dict, order):
        pass

    @abstractmethod
    def order_book(self, order: str, query):
        pass

    @abstractmethod
    def get_filter(self, params: dict, query):
        pass

    @abstractmethod
    def get_filter_by_price(self, value: list, query):
        pass

    @abstractmethod
    def get_filter_by_title(self, title: Union[str, List], query):
        pass

    @abstractmethod
    def get_filter_by_authors(self, authors: Union[str, List], query):
        pass

    @abstractmethod
    def get_filter_by_publisher(self, publisher: Union[str, List], query):
        pass

    @abstractmethod
    def get_top_by_tag(self, tag: str, batch_datetime: str):
        pass


class BookingRepo(ABC):

    @abstractmethod
    def get_by_id(self, booking_id: int):
        pass

    @abstractmethod
    def get_by_book_id(self, book_id: int):
        pass

    @abstractmethod
    def check_book_available(self, book_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add_instance(self, booking_data):
        pass

    @abstractmethod
    def get_users_booking(self, user_id: int):
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int):
        pass
