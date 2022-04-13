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

    def add_instance(self, instance: Book):
        self.session.add(instance)
        self.session.flush()
        return instance

    def add_instance_package(self, instances_package: list):
        self.session.add_all(instances_package)
        self.session.flush()
        print('Добавили пакет')


    def delete_by_id(self, book_id: int):
        book = self.get_by_id(book_id)
        self.session.delete(book)


    def update_by_id(self, book: Book):
        pass


    def get_by_name_author(self, author: str, name: str):
        query = select(Book).where(and_(Book.name == name, Book.author == author))
        book = self.session.execute(query).scalars().first()
        return book

