from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from sqlalchemy.sql import select, and_

from application import interfaces
from application.dataclasses import Book


@component
class BookRepo(BaseRepository, interfaces.BookRepo):

    def get_by_id(self, book_id: int):
        query = select(Book).where(Book.id == book_id)
        book = self.session.execute(query).scalars().one_or_none()
        return book

    def get_all(self):
        query = select(Book)
        books = self.session.execute(query).scalars().all()
        return books

    def add_instance(self, book: Book):
        self.session.add(book)
        self.session.flush()
        return book

    def delete_by_id(self, book_id: int):
        book = self.get_by_id(book_id)
        self.session.delete(book)

    def update_by_id(self, book: Book):
        pass

    def get_by_name_author(self, author: str, name: str):
        query = select(Book).where(and_(Book.name == name, Book.author == author))
        book = self.session.execute(query).scalars().first()
        return book

