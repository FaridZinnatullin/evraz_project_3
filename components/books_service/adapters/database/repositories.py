import datetime
from typing import List, Union

from sqlalchemy import asc, desc
from sqlalchemy.sql import and_, select

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from application import interfaces
from application.dataclasses import Book, Booking


@component
class BookingRepo(BaseRepository, interfaces.BookingRepo):

    def get_by_id(self, booking_id: int):
        query = select(Booking).where(Booking.id == booking_id)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_book_id(self, book_id: int):
        query = select(Booking).where(Booking.book_id == book_id
                                      ).order_by(desc(Booking.id)).limit(1)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_user_id(self, user_id: int):
        query = select(Booking).where(Booking.user_id == user_id
                                      ).order_by(desc(Booking.id)).limit(1)
        return self.session.execute(query).scalars().one_or_none()

    def check_book_available(self, book_id: int):
        if self.get_by_book_id(book_id
                               ).expiry_datetime > datetime.datetime.now():
            return True

    def add_instance(self, instance: Booking):
        self.session.add(instance)
        self.session.flush()
        return instance

    def get_all(self):
        query = select(Booking)
        return self.session.execute(query).scalars().all()

    def get_users_booking(self, user_id):
        query = select(Booking).where(Booking.user_id == user_id)
        return self.session.execute(query).scalars().all()


@component
class BookRepo(BaseRepository, interfaces.BookRepo):

    def get_by_id(self, book_id: int):
        query = select(Book).where(Book.id == book_id)
        return self.session.execute(query).scalars().one_or_none()

    def get_all(self):
        query = select(Book).where(Book.redeemed == False)
        return self.session.execute(query).scalars().all()

    def add_instance(self, instance: Book):
        self.session.add(instance)
        self.session.flush()
        return instance

    def add_instance_package(self, instances_package: list):
        for instance in instances_package:
            if not self.session.query(Book).filter(Book.id == instance.id
                                                   ).one_or_none():
                self.session.add(instance)
        self.session.flush()

    def delete_by_id(self, book_id: int):
        book = self.get_by_id(book_id)
        self.session.delete(book)

    def get_by_name_author(self, author: str, name: str):
        query = select(Book).where(
            and_(Book.title == name, Book.authors == author)
        )
        return self.session.execute(query).scalars().first()

    def get_books_with_filters(self, params: dict, sorting_key):
        query = self.session.query(Book).where(Book.redeemed == False)
        query = self.get_filter(params, query)
        query = self.sorting_book(sorting_key, query)
        return self.session.execute(query).scalars().all()

    def sorting_book(self, sorting_key: str, query):
        if sorting_key == 'price':
            return query.order_by(Book.price)
        if sorting_key == 'pages':
            return query.order_by(Book.pages)

    def get_filter(self, params: dict, query):
        if 'keyword' in params:
            query = self.get_filter_by_keyword(
                keyword=params.get('keyword'), query=query
            )
        if 'authors' in params:
            query = self.get_filter_by_authors(
                authors=params.get('authors'), query=query
            )
        if 'price' in params:
            price = params.get('price')
            # На случай, если есть верхняя и нижняя граница цен
            if isinstance(price[0], List):
                for price_border in price:
                    query = self.get_filter_by_price(
                        price_pair=price_border, query=query
                    )
            else:
                query = self.get_filter_by_price(price_pair=price, query=query)

        if 'publisher' in params:
            query = self.get_filter_by_publisher(
                publisher=params.get('publisher'), query=query
            )

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

    def get_filter_by_keyword(self, keyword: Union[str, List], query):
        if isinstance(keyword, List):
            keyword = ','.join(keyword)
        keyword = keyword.replace('_', ' ')

        query_title = query.filter(Book.title.like(f'%{keyword}%'))
        query_subtitle = query.filter(Book.subtitle.like(f'%{keyword}%'))
        query_description = query.filter(Book.desc.like(f'%{keyword}%'))

        return query_title.union(query_subtitle).union(query_description)

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

    def get_top_by_tag(self, tag: str, batch_datetime: str):
        query = select(Book).where(
            and_(
                Book.service_tag == tag, Book.batch_datetime == batch_datetime
            )
        ).order_by(desc(Book.rating), asc(Book.year)).limit(3)
        return self.session.execute(query).scalars().all()
