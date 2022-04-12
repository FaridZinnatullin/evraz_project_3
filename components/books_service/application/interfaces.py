from abc import ABC, abstractmethod
from typing import List, Optional

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

