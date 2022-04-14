from typing import Tuple, Union

from evraz.classic.http_api import App
from evraz.classic.http_auth import Authenticator

from application import services
from . import auth, controllers


def create_app(books_manager: services.BooksManager,
               books_updater: services.BooksUpdaterManager,
               booking_manager: services.BookingManager) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    authenticator.set_strategies(auth.jwt_strategy)
    app = App(prefix='/api')
    app.register(controllers.Books(authenticator=authenticator,
                                   books_manager=books_manager,
                                   books_updater=books_updater,
                                   booking_manager=booking_manager))
    return app
