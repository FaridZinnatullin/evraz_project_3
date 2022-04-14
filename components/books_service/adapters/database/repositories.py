from typing import List, Union

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

    def get_books(self, params: dict, order):
        query = self.session.query(Book)
        query = self.get_filter(params, query)
        query = self.order_book(order, query)
        books = self.session.execute(query).scalars().all()
        return books

    def order_book(self, order: str, query):
        if order == 'price':
            return query.order_by(Book.price)
        if order == 'pages':
            return query.order_by(Book.pages)


    def get_filter(self, params: dict, query):
        if 'title' in params:
            query = self.get_filter_by_title(title=params.get('title'), query=query)
        if 'authors' in params:
            query = self.get_filter_by_authors(authors=params.get('authors'), query=query)
        if 'price' in params:
            price = params.get('price')
            # На случай, если есть верхняя и нижняя граница цен
            if isinstance(price[0], List):
                for price_border in price:
                    query = self.get_filter_by_price(price_pair=price_border, query=query)
            else:
                query = self.get_filter_by_price(price_pair=price, query=query)

        if 'publisher' in params:
            query = self.get_filter_by_publisher(publisher=params.get('publisher'), query=query)

        return query

    def get_filter_by_price(self, price_pair: list, query):
        operation, value = price_pair[0], price_pair[1]
        results = {
            'gt': query.filter(Book.price > value),
            'lt': query.filter(Book.price < value),
            'gte': query.filter(Book.price >= value),
            'lte': query.filter(Book.price <= value),
            'eq': query.filter(Book.price == value)
        }

        return results[operation]

    def get_filter_by_title(self, title: Union[str, List], query):
        if isinstance(title, List):
            title = ','.join(title)
        title = title.replace('_', ' ')

        query_title = query.filter(Book.title.like(f'%{title}%'))
        # query_subtitle = query.filter(Book.subtitle.like(f'%{title}%'))
        # query_description = query.filter(Book.desc.like(f'%{title}%'))

        return query_title

    def get_filter_by_authors(self, authors: Union[str, List], query):
        if isinstance(authors, List):
            authors = ','.join(authors)
        authors = authors.replace('_', ' ')
        return query.filter(Book.authors.like(f'%{authors}%'))

    def get_filter_by_publisher(self, publisher: Union[str, List], query):
        if isinstance(publisher, List):
            publisher = ','.join(publisher)
        publisher = publisher.replace('_', ' ')
        return query.filter(Book.publisher.like(f'%{publisher}%'))
