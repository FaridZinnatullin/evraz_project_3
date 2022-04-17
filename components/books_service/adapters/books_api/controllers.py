from evraz.classic.components import component
from evraz.classic.http_auth import authenticate, authenticator_needed

from application import services

from .join_points import join_point


@authenticator_needed
@component
class Books:
    books_manager: services.BooksManager
    books_updater: services.BooksUpdaterManager
    booking_manager: services.BookingManager

    @join_point
    def on_get_book_info(self, request, response):
        book = self.books_manager.get_book_by_id(**request.params)
        response.media = {
            'id': book.id,
            'title': book.title,
            'subtitle': book.subtitle,
            'price': book.price,
            'rating': book.rating,
            'authors': book.authors,
            'publisher': book.publisher,
            'year': book.year,
            'pages': book.pages,
            'desc': book.desc,
            'service_tag': book.service_tag,
            'batch_datetime': book.batch_datetime,
            'redeemed': book.redeemed,
            'booking_datetime': book.booking_datetime
        }

    @join_point
    def on_get_all_books(self, request, response):
        books = self.books_manager.get_all_books()
        response.media = [
            {
                'id': book.id,
                'title': book.title,
                'subtitle': book.subtitle,
                'price': book.price,
                'rating': book.rating,
                'authors': book.authors,
                'publisher': book.publisher,
                'year': book.year,
                'pages': book.pages,
                'desc': book.desc,
                'service_tag': book.service_tag,
                'batch_datetime': book.batch_datetime,
                'redeemed': book.redeemed,
                'booking_datetime': book.booking_datetime
            } for book in books]

    @join_point
    def on_get_with_filters(self, request, response):
        books = self.books_manager.filter_books(request.params)
        response.media = [
            {
                'id': book.id,
                'title': book.title,
                'subtitle': book.subtitle,
                'price': book.price,
                'rating': book.rating,
                'authors': book.authors,
                'publisher': book.publisher,
                'year': book.year,
                'pages': book.pages,
                'desc': book.desc,
                'service_tag': book.service_tag,
                'batch_datetime': book.batch_datetime,
                'redeemed': book.redeemed,
                'booking_datetime': book.booking_datetime
            } for book in books
        ]

    @join_point
    @authenticate
    def on_post_create_booking(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.booking_manager.booking_book(**request.media)

    @join_point
    @authenticate
    def on_get_booking_info(self, request, response):
        request.params['user_id'] = request.context.client.user_id
        booking = self.booking_manager.get_by_id(**request.params)
        response.media = {
            'id': booking.id,
            'book_id': booking.book_id,
            'user_id': booking.user_id,
            'created_datetime': booking.created_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'expiry_datetime': booking.expiry_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'redeemed': booking.redeemed
        }

    @join_point
    @authenticate
    def on_get_show_all_booking(self, request, response):
        request.params['user_id'] = request.context.client.user_id
        bookings = self.booking_manager.get_all_users_booking(**request.params)
        response.media = [{
            'id': booking.id,
            'book_id': booking.book_id,
            'user_id': booking.user_id,
            'created_datetime': booking.created_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'expiry_datetime': booking.expiry_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'redeemed': booking.redeemed
        } for booking in bookings]

    @join_point
    @authenticate
    def on_post_delete_booking(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.booking_manager.delete_booking(**request.media)

    @join_point
    @authenticate
    def on_post_redeem_booking(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.booking_manager.redeem_booking(**request.media)

    @join_point
    @authenticate
    def on_get_active_booking(self, request, response):
        request.params['user_id'] = request.context.client.user_id
        booking = self.booking_manager.get_active_booking(**request.params)
        response.media = {
            'id': booking.id,
            'book_id': booking.book_id,
            'user_id': booking.user_id,
            'created_datetime': booking.created_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'expiry_datetime': booking.expiry_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'redeemed': booking.redeemed
        }
